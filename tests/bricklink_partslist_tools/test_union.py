import pytest
import sys
from pathlib import Path
from typing import Callable, List
from functools import reduce

## Lazily access classes inside the src directory (and suppress pylint errors when it can't resolve the import)
sys.path.append(str(Path('src').absolute()))
# pylint: disable=import-error
from part import Part
from parts_list import PartsList
from operations import Operations
# pylint: enable=import-error


class TestUnion:

    ## Fixtures

    @pytest.fixture
    def red_2x2_and_2x4_brick_parts_list_factory(self, one_red_2x4_and_2x2_brick_csv_path_factory) -> Callable:
        def _init():
            return PartsList(one_red_2x4_and_2x2_brick_csv_path_factory())

        return _init


    @pytest.fixture
    def complex_parts_list_factory(self, complex_csv_path_factory) -> Callable:
        def _init():
            return PartsList(complex_csv_path_factory())
    
        return _init


    @pytest.fixture
    def empty_parts_list_factory(self) -> Callable:
        def _init():
            return PartsList()

        return _init

    ## Methods

    def get_unique_part_count(self, *parts_lists: List[PartsList]) -> int:
        parts = set()

        parts_list: PartsList
        for parts_list in parts_lists:
            part: Part
            for part in parts_list.parts.values():
                parts.add(part.id)

        return len(parts)


    def get_total_part_count(self, *parts_lists: List[PartsList]) -> int:
        count = 0

        parts_list: PartsList
        for parts_list in parts_lists:
            part: Part
            for part in parts_list.parts.values():
                count += part.qty

        return count

    ## Tests

    def test_simple_union(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_lists: List[PartsList] = []
        parts_lists.append(red_2x2_and_2x4_brick_parts_list_factory())
        parts_lists.append(red_2x2_and_2x4_brick_parts_list_factory())

        result: PartsList = Operations.union(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == self.get_unique_part_count(*parts_lists)
        assert self.get_total_part_count(result) == self.get_total_part_count(*parts_lists)

        assert result.parts.get('3001:Red').qty == 2
        assert result.parts.get('3003:Red').qty == 2


    def test_complex_union(self, complex_parts_list_factory):
        parts_lists: List[PartsList] = [complex_parts_list_factory()] * 2

        result: PartsList = Operations.union(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == self.get_unique_part_count(*parts_lists)
        assert self.get_total_part_count(result) == self.get_total_part_count(*parts_lists)

    
    def test_empty_union(self, empty_parts_list_factory):
        parts_lists: List[PartsList] = [empty_parts_list_factory()] * 2

        result: PartsList = Operations.union(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 0


    def test_no_union(self):
        runtime_error_encountered = False

        try:
            Operations.union()
        except RuntimeError:
            runtime_error_encountered = True

        assert runtime_error_encountered


    def test_single_union(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_lists: List[PartsList] = [red_2x2_and_2x4_brick_parts_list_factory()]

        result: PartsList = Operations.union(*parts_lists)

        assert isinstance(result, PartsList)
        assert result is parts_lists[0]
        assert len(result.parts) == self.get_unique_part_count(*parts_lists)
        assert self.get_total_part_count(result) == self.get_total_part_count(*parts_lists)

        assert result.parts.get('3001:Red').qty == 1
        assert result.parts.get('3003:Red').qty == 1
    

    def test_half_empty_union(self, empty_parts_list_factory, red_2x2_and_2x4_brick_parts_list_factory):
        parts_lists: List[PartsList] = []
        parts_lists.append(empty_parts_list_factory())
        parts_lists.append(red_2x2_and_2x4_brick_parts_list_factory())

        result: PartsList = Operations.union(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == self.get_unique_part_count(*parts_lists)
        assert self.get_total_part_count(result) == self.get_total_part_count(*parts_lists)

        assert result.parts.get('3001:Red').qty == 1
        assert result.parts.get('3003:Red').qty == 1


    def test_simple_complex_union(self, red_2x2_and_2x4_brick_parts_list_factory, complex_parts_list_factory):
        parts_lists: List[PartsList] = []
        parts_lists.append(red_2x2_and_2x4_brick_parts_list_factory())
        parts_lists.append(complex_parts_list_factory())

        result: PartsList = Operations.union(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == self.get_unique_part_count(*parts_lists)
        assert self.get_total_part_count(result) == self.get_total_part_count(*parts_lists)

        assert result.parts.get('3001:Red').qty == 1
        assert result.parts.get('3003:Red').qty == 33


    def test_large_union(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_list_count = 25
        parts_lists: List[PartsList] = [red_2x2_and_2x4_brick_parts_list_factory()] * parts_list_count

        result: PartsList = Operations.union(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == self.get_unique_part_count(*parts_lists)
        assert self.get_total_part_count(result) == self.get_total_part_count(*parts_lists)

        assert result.parts.get('3001:Red').qty == parts_list_count
        assert result.parts.get('3003:Red').qty == parts_list_count
