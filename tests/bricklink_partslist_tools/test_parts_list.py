import pytest
import sys
from pathlib import Path
from typing import Callable, List

## Lazily access classes inside the src directory (and suppress pylint errors when it can't resolve the import)
sys.path.append(str(Path('src').absolute()))
# pylint: disable=import-error
from part import Part
from parts_list import PartsList
# pylint: enable=import-error


class TestPartsList:
    ## Fixtures

    @pytest.fixture
    def red_2x2_and_2x4_brick_parts_list_factory(self, one_red_2x4_and_2x2_brick_csv_path_factory) -> Callable:
        def _init():
            return PartsList(one_red_2x4_and_2x2_brick_csv_path_factory())

        return _init


    @pytest.fixture
    def empty_parts_list_factory(self) -> Callable:
        def _init():
            return PartsList()

        return _init

    ## Tests

    def test_empty_init(self, empty_parts_list_factory):
        partsList: PartsList = empty_parts_list_factory()
        assert partsList.path == None
        assert not partsList.parts


    def test_import_list(self, empty_parts_list_factory, one_red_2x2_brick_csv_path_factory):
        partsList: PartsList = empty_parts_list_factory()

        path = one_red_2x2_brick_csv_path_factory()
        partsList._import_list(path)
        assert partsList.path == path
        assert len(partsList.parts) == 1    # unique parts, not total parts
        
        imported_part: Part = list(partsList.parts.values())[0]
        assert imported_part.bl_item_no == '3003'
        assert imported_part.color_name == 'Red'
        assert imported_part.qty == 1

    
    def test_import_list_complex(self, empty_parts_list_factory, complex_csv_path_factory):
        partsList: PartsList = empty_parts_list_factory()

        path = complex_csv_path_factory()
        partsList._import_list(path)
        assert partsList.path == path
        assert len(partsList.parts) == 83    # unique parts, not total parts


    def test_init(self, one_red_2x4_and_2x2_brick_csv_path_factory):
        path = one_red_2x4_and_2x2_brick_csv_path_factory()
        partsList: PartsList = PartsList(path)

        assert partsList.path == path
        assert len(partsList.parts) == 2    # unique parts, not total parts


    def test_clone(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_list: PartsList = red_2x2_and_2x4_brick_parts_list_factory()
        clone: PartsList = parts_list.clone()

        assert clone == parts_list
    

    def test_export_csv(self, tmp_path, red_2x2_and_2x4_brick_parts_list_factory, empty_parts_list_factory):
        path: Path = tmp_path / 'test-csv.csv'
        parts_list: PartsList = red_2x2_and_2x4_brick_parts_list_factory()

        assert not path.exists()

        parts_list.export_csv(path)

        assert path.exists()

        exported_parts_list: PartsList = empty_parts_list_factory()
        exported_parts_list._import_list(path)
        exported_parts_list.path = parts_list.path  # Update the path to point to the original path, as otherwise the == check will fail

        assert parts_list == exported_parts_list
