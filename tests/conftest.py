import pytest
import sys

from typing import Callable, Dict, List
from pathlib import Path

## Lazily access classes inside the src directory (and suppress pylint errors when it can't resolve the import)
sys.path.append(str(Path('src').absolute()))
# pylint: disable=import-error
from parts_list import PartsList
# pylint: enable=import-error

class PartsListPathProvider:
    _parts_list_paths: Dict = None

    @staticmethod
    def _discover_parts_list_paths(directory: Path) -> List[Path]:
        if (not directory.is_dir()):
            raise RuntimeError('Unable to walk {}, not a directory'.format(str(directory)))
        
        parts_lists_paths = {}
        for item in directory.iterdir():
            if item.is_file():
                parts_lists_paths[item.name] = item
        
        return parts_lists_paths


    @staticmethod
    def get_parts_list_paths(name: str) -> List[str]:
        if PartsListPathProvider._parts_list_paths == None:
            parts_list_dir_path = Path('tests/data/parts_lists')
            PartsListPathProvider._parts_list_paths = PartsListPathProvider._discover_parts_list_paths(parts_list_dir_path)

        if name in dict(PartsListPathProvider._parts_list_paths):
            return PartsListPathProvider._parts_list_paths.get(name)
        else:
            raise RuntimeError('Invalid parts list name provided')

## Path Factory Fixtures

@pytest.fixture
def one_red_2x2_brick_csv_path_factory() -> Callable:
    def _get_path():
        return PartsListPathProvider.get_parts_list_paths('one_red_2x2_brick.csv')

    return _get_path


@pytest.fixture
def one_red_2x4_and_2x2_brick_csv_path_factory() -> Callable:
    def _get_path():
        return PartsListPathProvider.get_parts_list_paths('one_red_2x4_2x2_bricks.csv')

    return _get_path


@pytest.fixture
def one_red_2x4_brick_csv_path_factory() -> Callable:
    def _get_path():
        return PartsListPathProvider.get_parts_list_paths('one_red_2x4_brick.csv')

    return _get_path


@pytest.fixture
def complex_csv_path_factory() -> Callable:
    def _get_path():
        return PartsListPathProvider.get_parts_list_paths('complex_parts_list.csv')

    return _get_path

## PartsList Factory Fixtures

@pytest.fixture
def red_2x2_and_2x4_brick_parts_list_factory(one_red_2x4_and_2x2_brick_csv_path_factory) -> Callable:
    def _init():
        return PartsList(one_red_2x4_and_2x2_brick_csv_path_factory())

    return _init


@pytest.fixture
def complex_parts_list_factory(complex_csv_path_factory) -> Callable:
    def _init():
        return PartsList(complex_csv_path_factory())

    return _init


@pytest.fixture
def empty_parts_list_factory() -> Callable:
    def _init():
        return PartsList()

    return _init
