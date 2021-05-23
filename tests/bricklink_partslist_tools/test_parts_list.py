import pytest
import sys
from pathlib import Path
from typing import List

## Lazily access classes inside the src directory (and suppress pylint errors when it can't resolve the import)
sys.path.append(str(Path('src').absolute()))
# pylint: disable=import-error
from part import Part
from parts_list import PartsList
# pylint: enable=import-error


class TestPartsList:
    ## Tests

    def test_empty_init(self, empty_parts_list_factory):
        parts_list: PartsList = empty_parts_list_factory()
        assert parts_list.path == None
        assert not parts_list.parts


    def test_import_list(self, empty_parts_list_factory, one_red_2x2_brick_csv_path_factory):
        parts_list: PartsList = empty_parts_list_factory()

        path = one_red_2x2_brick_csv_path_factory()
        parts_list._import_list(path)
        assert parts_list.path == path
        assert len(parts_list.parts) == 1    # unique parts, not total parts
        
        imported_part: Part = list(parts_list.parts.values())[0]
        assert imported_part.bl_item_no == '3003'
        assert imported_part.color_name == 'Red'
        assert imported_part.qty == 1

    
    def test_import_nonexistant_list(self, empty_parts_list_factory):
        parts_list: PartsList = empty_parts_list_factory()

        runtime_error_encountered = False
        try:
            parts_list._import_list('/some/path/that/doesnt/exist')
        except RuntimeError:
            runtime_error_encountered = True
        
        assert runtime_error_encountered


    def test_import_list_complex(self, empty_parts_list_factory, complex_csv_path_factory):
        parts_list: PartsList = empty_parts_list_factory()

        path = complex_csv_path_factory()
        parts_list._import_list(path)
        assert parts_list.path == path
        assert len(parts_list.parts) == 83    # unique parts, not total parts


    def test_init(self, one_red_2x4_and_2x2_brick_csv_path_factory):
        path = one_red_2x4_and_2x2_brick_csv_path_factory()
        parts_list: PartsList = PartsList(path)

        assert parts_list.path == path
        assert len(parts_list.parts) == 2    # unique parts, not total parts


    def test_set_any_color_simple(self, red_2x2_and_2x4_brick_parts_list_factory):
        parts_list: PartsList = red_2x2_and_2x4_brick_parts_list_factory();

        parts = {}
        part: Part
        for part_id, part in parts_list.parts.items():
            parts[part_id] = part

        parts_list.set_any_color(['Red'])

        for part in parts_list.parts.values():
            ## All parts are red, so this is safe
            assert part.is_any_color()

        ## Make sure the parts mapping has been updated
        for part_id, part in parts.items():
            assert part_id not in parts_list.parts
            assert part.id in parts_list.parts


    def test_set_any_color_complex(self, complex_parts_list_factory):
        parts_list: PartsList = complex_parts_list_factory();

        red_parts = {}
        part: Part
        for part in filter(lambda part: part.color_name == 'Red', parts_list.parts.values()):
            red_parts[part.id] = part

        parts_list.set_any_color(['Red'])

        for part in red_parts.values():
            assert part.is_any_color()

        ## Make sure the parts mapping has been updated
        for part_id, part in red_parts.items():
            assert part_id not in parts_list.parts
            assert part.id in parts_list.parts


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
