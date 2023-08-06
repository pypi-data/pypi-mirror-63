from dataclasses import asdict
from dataclasses import is_dataclass
from logging import getLogger
from typing import Callable
from typing import Dict
from typing import Generator
from typing import List
from typing import Mapping
from typing import NoReturn
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from typing import get_type_hints

from botox import Injector

from watermill.message_brokers.message_broker import EndOfStreamError
from watermill.message_brokers.message_broker import MessageBroker
from watermill.message_brokers.message_broker import RightJoinedStreamRanAhead
from watermill.message_brokers.message_broker import StreamTimeoutError
from watermill.message_brokers.message_broker import StreamsShift
from watermill.stream_join import JoinTree
from watermill.stream_join import JoinTreeNode
from watermill.stream_join import compare_streams
from watermill.stream_join import get_injected_kwargs
from watermill.stream_join import get_join_data_mapping
from watermill.stream_join import get_tree_pairs
from watermill.stream_types import JoinedStreamType
from watermill.stream_types import ResultStreamType
from watermill.stream_types import StreamType
from watermill.windows import Window

logger = getLogger(__name__)


def _default_serializer(dataclass_value) -> dict:
    assert is_dataclass(dataclass_value)
    return asdict(dataclass_value)


def _default_deserializer(cls):
    def wrapped_de(value: dict):
        return cls(**value)
    return wrapped_de


class WaterMill:
    def __init__(
            self,
            broker: MessageBroker,
            process_func: Callable[[StreamType, List[Mapping[StreamType, JoinedStreamType]]], Union[ResultStreamType, None]],
            stream_cls: Union[Type[StreamType], Window] = None,
            join_tree: JoinTree = None,
            serializers: Mapping[Type, Callable] = None,
            deserializers: Mapping[Type, Callable] = None,
            injector: Injector = None,
            output_broker: Optional[MessageBroker] = None,
    ):
        assert stream_cls or join_tree

        self._injector = injector
        self._broker = broker
        self._output_broker = output_broker or broker
        self._window_func = None
        type_hints = get_type_hints(process_func)
        self._return_type = type_hints.get('return')
        if self._return_type == NoReturn:
            self._return_type = None
        elif str(self._return_type).startswith('typing.Union'):
            for return_type_item in self._return_type.__reduce__()[1][1]:
                if return_type_item != NoReturn:
                    self._return_type = return_type_item
                    break

        if stream_cls:
            if isinstance(stream_cls, Window):
                self._join_tree = JoinTree(
                    root_node=JoinTreeNode(
                        user_type=stream_cls.cls,
                    )
                )
                self._window_func = stream_cls.window_func
            else:
                self._join_tree = JoinTree(
                    root_node=JoinTreeNode(
                        user_type=stream_cls,
                    )
                )
        else:
            self._join_tree = join_tree

        self._process_func = process_func
        self._serializers: Mapping[Type, Callable] = serializers or {}
        self._deserializers: Mapping[Type, Callable] = deserializers or {}

    def run(self):
        if self._join_tree is None:
            return

        join_tree = self._join_tree
        serializer = self._serializers.get(self._return_type, _default_serializer) if self._return_type else None
        deserializer = self._deserializers.get(join_tree.root_node.user_type, _default_deserializer(join_tree.root_node.user_type))
        processing_func_type_hints = get_type_hints(self._process_func)
        injected_kwargs = get_injected_kwargs(processing_func_type_hints, self._injector)
        window_key = None
        root_elements = []
        join_data_mappings = []
        process_results = []
        window_func = self._window_func
        if join_tree.root_node.window_func:
            window_func = join_tree.root_node.window_func

        window_comparator = lambda next_element: StreamsShift.Equal if (window_key is None or window_key == window_func(next_element)) else StreamsShift.Less

        while True:
            root_element_data = None
            eos = False
            try:
                root_element_data = next(self._broker.get_elements(join_tree.root_node.user_type, comparator=window_comparator))
            except RightJoinedStreamRanAhead:
                process_result = self._process_func(root_elements, *join_data_mappings, **injected_kwargs)
                process_results, eos = _handle_result(process_result, process_results, eos)
                root_elements.clear()
                join_data_mappings.clear()
                window_key = None
            except StreamTimeoutError:
                new_window_key = window_func(None)

                assert new_window_key is not None
                if not window_key or window_key == new_window_key:
                    window_key = new_window_key
                    continue
                else:
                    if not root_elements:
                        continue

                    process_result = self._process_func(root_elements, *join_data_mappings, **injected_kwargs)
                    process_results, eos = _handle_result(process_result, process_results, eos)
                    root_elements.clear()
                    join_data_mappings.clear()
                    window_key = new_window_key
            except EndOfStreamError:
                if self._return_type:
                    self._output_broker.send_eos(self._return_type)
                return

            join_data_mapping = []
            if root_element_data:
                root_user_element = deserializer(root_element_data)
                if join_tree.pairs:
                    parent_children_map: Dict[StreamType, List[JoinedStreamType]] = {}
                    try:
                        self._get_joined_elements(join_tree.root_node, join_tree, root_element_data, root_user_element, parent_children_map)
                    except RightJoinedStreamRanAhead as exc:
                        if not window_func:
                            logger.warning(f'Joined right stream {exc.stream_type} ran ahead. Skipping root element')
                            continue
                    except EndOfStreamError:
                        if parent_children_map:
                            eos = True
                        elif self._return_type:
                            self._output_broker.send_eos(self._return_type)
                            self._broker.commit()
                            return

                    join_data_mapping = get_join_data_mapping(processing_func_type_hints, parent_children_map)

                if window_func:
                    new_window_key = window_func(root_element_data)
                    assert new_window_key is not None
                    root_elements.append(root_user_element)
                    if not join_data_mappings:
                        join_data_mappings = join_data_mapping
                    else:
                        assert len(join_data_mapping) == len(join_data_mappings)
                        temp_join_data_mappings = []
                        for old, new in zip(join_data_mappings, join_data_mapping):
                            old.update(new)
                            temp_join_data_mappings.append(old)
                        join_data_mappings = temp_join_data_mappings

                    if eos:
                        process_result = self._process_func(root_elements, *join_data_mappings, **injected_kwargs)
                        process_results, eos = _handle_result(process_result, process_results, eos)
                    else:
                        window_key = new_window_key
                        continue
                else:
                    process_result = self._process_func(root_user_element, *join_data_mapping, **injected_kwargs)
                    process_results, eos = _handle_result(process_result, process_results, eos)

            assert process_results or not self._return_type

            if self._return_type:
                for result in process_results:
                    self._output_broker.send(self._return_type, serializer(result))
                process_results.clear()
                self._broker.commit()
            if eos:
                if self._return_type:
                    self._output_broker.send_eos(self._return_type)
                    self._broker.commit()
                return

    def _get_joined_elements(
            self,
            join_node: JoinTreeNode,
            join_tree: JoinTree,
            left_element: dict,
            left_deserialized_element: StreamType,
            parent_children_map: Dict[StreamType, List[JoinedStreamType]],
    ):
        eos = False
        eos_exc = None
        for join_pair in get_tree_pairs(join_tree, join_node):
            right_join_node = join_pair.right_node
            left_expression = join_pair.left_expression
            right_expression = join_pair.right_expression

            try:
                for element_data in self._broker.get_elements(
                        right_join_node.user_type,
                        comparator=lambda right_element: compare_streams(left_expression(left_element), right_expression(right_element))
                ):
                    assert element_data is not None
                    deserialized_element = self._deserializers.get(right_join_node.user_type, _default_deserializer(right_join_node.user_type))(element_data)
                    parent_children_map.setdefault(left_deserialized_element, []).append(deserialized_element)

                    self._get_joined_elements(right_join_node, join_tree, element_data, deserialized_element, parent_children_map)
            except EndOfStreamError as exc:
                eos = True
                eos_exc = exc
                continue

        if eos:
            raise eos_exc


def _handle_result(process_result: Union[StreamType, StopIteration, None], process_results: list, eos: bool) -> Tuple[list, bool]:
    if not process_result or process_result is None:
        return process_results, eos

    if isinstance(process_result, StopIteration):
        return process_results, True

    if isinstance(process_result, Generator):
        for element in process_result:
            assert element
            if isinstance(element, StopIteration):
                return process_results, True
            process_results.append(element)
    else:
        process_results.append(process_result)
    return process_results, eos
