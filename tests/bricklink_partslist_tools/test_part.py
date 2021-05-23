import pytest
import sys
from pathlib import Path
from typing import Callable, List

## Lazily access classes inside the src directory (and suppress pylint errors when it can't resolve the import)
sys.path.append(str(Path('src').absolute()))
# pylint: disable=import-error
from part import Part
# pylint: enable=import-error


class TestPart:
    ## Fixtures

    @pytest.fixture
    def one_red_2x4_brick_factory(self) -> Callable:
        def _init_bricks():
            return Part(['3001', '300121', '3001', 'Brick 2 x 4', '5', '4', 'Red', 'Solid Colors', '1', '2.32'])
        
        return _init_bricks


    @pytest.fixture
    def five_red_2x4_bricks_factory(self) -> Callable:
        def _init_bricks():
            return Part(['3001', '300121', '3001', 'Brick 2 x 4', '5', '4', 'Red', 'Solid Colors', '5', '11.6'])

        return _init_bricks

    ## Tests

    def test_sub_five_minus_one(self, five_red_2x4_bricks_factory, one_red_2x4_brick_factory):
        five_bricks: Part = five_red_2x4_bricks_factory()
        one_brick: Part = one_red_2x4_brick_factory()

        result: Part = five_bricks - one_brick

        assert result.qty == five_bricks.qty - one_brick.qty
        assert result.weight == five_bricks.weight - one_brick.weight


    def test_sub_one_minus_one(self, one_red_2x4_brick_factory):
        result: Part = one_red_2x4_brick_factory() - one_red_2x4_brick_factory()

        assert result == None


    def test_sub_one_minus_five(self, one_red_2x4_brick_factory, five_red_2x4_bricks_factory):
        result: Part = one_red_2x4_brick_factory() - five_red_2x4_bricks_factory()

        assert result == None


    def test_add_five_plus_one(self, five_red_2x4_bricks_factory, one_red_2x4_brick_factory):
        five_bricks: Part = five_red_2x4_bricks_factory()
        one_brick: Part = one_red_2x4_brick_factory()

        result: Part = five_bricks + one_brick

        assert result.qty == five_bricks.qty + one_brick.qty
        assert result.weight == five_bricks.weight + one_brick.weight


    def test_equal(self, one_red_2x4_brick_factory, five_red_2x4_bricks_factory):
        one_brick_a: Part = one_red_2x4_brick_factory()
        one_brick_b: Part = one_red_2x4_brick_factory()

        assert one_brick_a == one_brick_b

        five_bricks: Part = five_red_2x4_bricks_factory()
        one_brick: Part = one_red_2x4_brick_factory()

        assert five_bricks != one_brick


    def test_enable_any_color(self, one_red_2x4_brick_factory):
        part: Part = one_red_2x4_brick_factory();

        assert part.bl_color_id == '5'
        assert part.l_draw_color_id == '4'
        assert part.color_name == 'Red'

        part.enable_any_color();

        assert part.bl_color_id == '0'
        assert part.l_draw_color_id == '9999'
        assert part.color_name == '(Not Applicable)'
        ## Does part.color_category really matter?


    def test_is_any_color(self, one_red_2x4_brick_factory):
        part: Part = one_red_2x4_brick_factory();

        assert not part.is_any_color()

        part.enable_any_color();

        assert part.is_any_color()


    def test_is_color_match(self, one_red_2x4_brick_factory):
        part: Part = one_red_2x4_brick_factory();

        assert part.is_color_match('Red')
        assert part.is_color_match('red')

        assert not part.is_color_match('Vintage Red')
        assert not part.is_color_match('Trans-Medium Reddish Violet Opal')
        assert not part.is_color_match('Blue')


    def test_clone(self, one_red_2x4_brick_factory):
        one_brick: Part = one_red_2x4_brick_factory()
        clone: Part = one_brick.clone()

        assert clone == one_brick
