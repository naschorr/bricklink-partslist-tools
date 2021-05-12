import pytest
import sys
from pathlib import Path
from typing import Callable, List

## Lazily access classes inside the src directory (and suppress pylint errors when it can't resolve the import)
sys.path.append(str(Path('src').absolute()))
# pylint: disable=import-error
from part import Part
from parts_list import PartsList
from operations import Operations
# pylint: enable=import-error


class TestIntersection:

    def check_parts_list_length_equality(self, *parts_lists: List[PartsList]) -> bool:
        if (len(parts_lists) <= 1):
            return True

        length = len(parts_lists[0].parts)

        return all(len(parts_list.parts) == length for parts_list in parts_lists[1:])

    ## Tests

    def test_simple_intersection(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_lists: List[PartsList] = []
        parts_lists.append(red_2x2_and_2x4_brick_parts_list_factory())
        parts_lists.append(red_2x2_and_2x4_brick_parts_list_factory())

        result: PartsList = Operations.intersection(*parts_lists)

        assert isinstance(result, PartsList)
        assert self.check_parts_list_length_equality(result, *parts_lists)


    def test_complex_intersection(self, complex_parts_list_factory):
        parts_lists: List[PartsList] = []
        parts_lists.append(complex_parts_list_factory())
        parts_lists.append(complex_parts_list_factory())

        result: PartsList = Operations.intersection(*parts_lists)

        assert isinstance(result, PartsList)
        assert self.check_parts_list_length_equality(result, *parts_lists)

    
    def test_empty_intersection(self, empty_parts_list_factory):
        parts_lists: List[PartsList] = []
        parts_lists.append(empty_parts_list_factory())
        parts_lists.append(empty_parts_list_factory())

        result: PartsList = Operations.intersection(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 0


    def test_no_intersection(self):
        runtime_error_encountered = False

        try:
            Operations.intersection()
        except RuntimeError:
            runtime_error_encountered = True

        assert runtime_error_encountered


    def test_single_intersection(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_lists: List[PartsList] = [red_2x2_and_2x4_brick_parts_list_factory()]

        result: PartsList = Operations.intersection(*parts_lists)

        assert isinstance(result, PartsList)
        assert result is parts_lists[0]
        assert self.check_parts_list_length_equality(result, *parts_lists)

        assert result.parts.get('3001:Red').qty == 1
        assert result.parts.get('3003:Red').qty == 1
    

    def test_half_empty_intersection(self, empty_parts_list_factory, red_2x2_and_2x4_brick_parts_list_factory):
        parts_lists: List[PartsList] = []
        parts_lists.append(empty_parts_list_factory())
        parts_lists.append(red_2x2_and_2x4_brick_parts_list_factory())

        result: PartsList = Operations.intersection(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 0


    def test_simple_complex_intersection(self, red_2x2_and_2x4_brick_parts_list_factory, complex_parts_list_factory):
        parts_lists: List[PartsList] = []
        parts_lists.append(red_2x2_and_2x4_brick_parts_list_factory())
        parts_lists.append(complex_parts_list_factory())

        result: PartsList = Operations.intersection(*parts_lists)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 2
        assert result.parts.get('3003:Red').qty == 1


    def test_large_intersection(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_list_count = 25
        parts_lists: List[PartsList] = [red_2x2_and_2x4_brick_parts_list_factory()] * parts_list_count

        result: PartsList = Operations.intersection(*parts_lists)

        assert isinstance(result, PartsList)
        assert self.check_parts_list_length_equality(result, *parts_lists)

        assert result.parts.get('3001:Red').qty == 1
        assert result.parts.get('3003:Red').qty == 1
