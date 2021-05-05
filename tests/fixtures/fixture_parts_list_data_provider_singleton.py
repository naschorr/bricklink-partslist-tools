import pytest
from typing import Callable, Dict, List
from pathlib import Path

class FixturePartsListDataProviderSingleton:
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
    def _get_parts_list_paths(name: str) -> List[str]:
        if FixturePartsListDataProviderSingleton._parts_list_paths == None:
            parts_list_dir_path = Path('tests/data/parts_lists')
            FixturePartsListDataProviderSingleton._parts_list_paths = FixturePartsListDataProviderSingleton._discover_parts_list_paths(parts_list_dir_path)

        if name in dict(FixturePartsListDataProviderSingleton._parts_list_paths):
            return FixturePartsListDataProviderSingleton._parts_list_paths.get(name)
        else:
            raise RuntimeError('Invalid parts list name provided')


    @staticmethod
    @pytest.fixture
    def one_red_2x2_brick_csv_path_factory() -> Callable:
        def _get_path():
            return FixturePartsListDataProviderSingleton._get_parts_list_paths('one_red_2x2_brick.csv')

        return _get_path


    @staticmethod
    @pytest.fixture
    def one_red_2x4_and_2x2_brick_csv_path_factory() -> Callable:
        def _get_path():
            return FixturePartsListDataProviderSingleton._get_parts_list_paths('one_red_2x4_2x2_bricks.csv')

        return _get_path


    @staticmethod
    @pytest.fixture
    def one_red_2x4_brick_csv_path_factory() -> Callable:
        def _get_path():
            return FixturePartsListDataProviderSingleton._get_parts_list_paths('one_red_2x4_brick.csv')

        return _get_path


    @staticmethod
    @pytest.fixture
    def complex_csv_path_factory() -> Callable:
        def _get_path():
            return FixturePartsListDataProviderSingleton._get_parts_list_paths('complex_parts_list.csv')

        return _get_path