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


class TestDifference:

    def check_parts_list_length_equality(self, *parts_lists: List[PartsList]) -> bool:
        if (len(parts_lists) <= 1):
            return True

        length = len(parts_lists[0].parts)

        return all(len(parts_list.parts) == length for parts_list in parts_lists[1:])

    ## Tests

    def test_simple_difference(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_list_a = red_2x2_and_2x4_brick_parts_list_factory()
        parts_list_b = red_2x2_and_2x4_brick_parts_list_factory()

        result: PartsList = Operations.difference(parts_list_a, parts_list_b)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 0


    def test_complex_difference(self, complex_parts_list_factory):
        parts_list_a = complex_parts_list_factory()
        parts_list_b = complex_parts_list_factory()

        result: PartsList = Operations.difference(parts_list_a, parts_list_b)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 0


    def test_simple_complex_difference(self, red_2x2_and_2x4_brick_parts_list_factory, complex_parts_list_factory):
        parts_list_a = red_2x2_and_2x4_brick_parts_list_factory()
        parts_list_b = complex_parts_list_factory()

        result: PartsList = Operations.difference(parts_list_a, parts_list_b)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 1

        assert result.parts.get('3001:Red').qty == 1
        assert result.parts.get('3003:Red') == None


    def test_complex_simple_difference(self, complex_parts_list_factory, red_2x2_and_2x4_brick_parts_list_factory):
        parts_list_a = complex_parts_list_factory()
        parts_list_b = red_2x2_and_2x4_brick_parts_list_factory()

        result: PartsList = Operations.difference(parts_list_a, parts_list_b)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 83

        assert result.parts.get('3001:Red') == None
        assert result.parts.get('3003:Red').qty == 31


    def test_empty_difference(self, empty_parts_list_factory):
        parts_list_a = empty_parts_list_factory()
        parts_list_b = empty_parts_list_factory()

        result: PartsList = Operations.difference(parts_list_a, parts_list_b)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 0


    def test_simple_empty_difference(self, red_2x2_and_2x4_brick_parts_list_factory, empty_parts_list_factory):
        parts_list_a = red_2x2_and_2x4_brick_parts_list_factory()
        parts_list_b = empty_parts_list_factory()

        result: PartsList = Operations.difference(parts_list_a, parts_list_b)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 2

        assert result.parts.get('3001:Red').qty == 1
        assert result.parts.get('3003:Red').qty == 1


    def test_empty_simple_difference(self, empty_parts_list_factory, red_2x2_and_2x4_brick_parts_list_factory):
        parts_list_a = empty_parts_list_factory()
        parts_list_b = red_2x2_and_2x4_brick_parts_list_factory()

        result: PartsList = Operations.difference(parts_list_a, parts_list_b)

        assert isinstance(result, PartsList)
        assert len(result.parts) == 0


    def test_none_difference(self):
        runtime_error_encountered = False

        try:
            Operations.difference(None, None)
        except RuntimeError:
            runtime_error_encountered = True

        assert runtime_error_encountered


    def test_simple_none_difference(self, red_2x2_and_2x4_brick_parts_list_factory):
        runtime_error_encountered = False

        try:
            Operations.difference(red_2x2_and_2x4_brick_parts_list_factory(), None)
        except RuntimeError:
            runtime_error_encountered = True

        assert runtime_error_encountered


    def test_none_simple_difference(self, red_2x2_and_2x4_brick_parts_list_factory):
        runtime_error_encountered = False

        try:
            Operations.difference(None, red_2x2_and_2x4_brick_parts_list_factory())
        except RuntimeError:
            runtime_error_encountered = True

        assert runtime_error_encountered
