import click
from pathlib import Path
from typing import List

from enums import SaveFormat
from part import Part
from parts_list import PartsList
from operations import Operations


def _build_parts_lists(*paths: List[Path]) -> List[PartsList]:
    parts_lists: List[PartsList] = []
    for path in paths:
        try:
            parts_list = PartsList(path)
        except AssertionError:
            print('Unable to generate parts list for file at {}'.format(path))
            continue
    
        parts_lists.append(parts_list)

    return parts_lists


def _dump_parts_list(parts_list: PartsList):
    total_parts = 0
    parts = parts_list.parts

    print('Dumping parts list:')

    part: Part
    for part_id in sorted(parts.keys()):
        part = parts[part_id]
        total_parts += part.qty
        print('{} \t\t({}) \t{}'.format(part.bl_item_no, part.qty, part.color_name))
    
    print('Unique parts: {}, total parts: {}'.format(len(parts.keys()), total_parts))


@click.command()
@click.option('--missing-parts', is_flag = True, help = 'Compares the owned and unowned parts lists, returning a single list of all unowned parts.')
@click.option('--merge', is_flag = True, help = 'Merges together all provided parts lists into a single one, regardless of them being owned or unowned.')
@click.option('--intersection', is_flag = True, help = 'Intersects all provided parts lists into a single one, finding the common parts between them, regardless of them being owned or unowned.')
@click.option('--owned-parts-list-path', '-o', type = click.Path(exists = True), multiple = True, help = 'A path to a Bricklink parts list .csv file representing parts that you own')
@click.option('--unowned-parts-list-path', '-u', type = click.Path(exists = True), multiple = True, help = 'A path to a Bricklink parts list .csv file representing parts that you do not own')
@click.option('--save-path', '-s', type = click.Path(), help = 'The path to export manipulated parts list data to')
@click.option('--save-format', '-f', type = click.Choice([save_format.value for save_format in SaveFormat], case_sensitive = False), help = 'The format to export manipulated parts list data in')
def main(
    missing_parts: bool,
    merge: bool,
    intersection: bool,
    owned_parts_list_path: List[Path],
    unowned_parts_list_path: List[Path],
    save_path: Path,
    save_format: str
):
    ## Enforce plurality correctness for multi-options & ensure we're working with pathlib Paths (click.Path() isn't pathlib.Path for Python 2 compatibility reasons)
    owned_parts_list_paths = [Path(path) for path in owned_parts_list_path]
    del owned_parts_list_path
    unowned_parts_list_paths = [Path(path) for path in unowned_parts_list_path]
    del unowned_parts_list_path
    save_path = Path(save_path) if save_path else None

    ## Ensure valid saving can happen (if desired)
    if (save_path == None and save_format != None):
        raise RuntimeError('Unable to save output with a \'save-format\', but without a \'save-path\' defined.')
    elif (save_path != None and save_format == None):
        raise RuntimeError('Unable to save output with a \'save_path\', but without a \'save_format\' defined.')

    ## Build the PartsList lists
    owned_parts_lists: List[PartsList] = _build_parts_lists(*owned_parts_list_paths)
    unowned_parts_lists: List[PartsList] = _build_parts_lists(*unowned_parts_list_paths)

    ## Build the output PartsList
    output_parts_list: PartsList = None
    if missing_parts:
        if (len(unowned_parts_lists) > 1):
            print('\'missing-parts\' command only supports a single unowned PartsList, so only the first one (at: {}) will be used.'.format(unowned_parts_lists[0].path))

        print('Performing search for missing parts at: {}, from the owned parts lists at: {}.'.format(
            unowned_parts_lists[0],
            ', '.join([str(parts_list.path) for parts_list in owned_parts_lists])
        ))

        owned_parts_list = Operations.union(*owned_parts_lists)
        unowned_parts_list = Operations.union(*unowned_parts_lists)

        output_parts_list = Operations.difference(unowned_parts_list, owned_parts_list)
    elif merge:
        if (len(unowned_parts_lists) + len(owned_parts_lists) == 0):
            raise RuntimeError('No parts lists provided, thus the \'merge\' would be pointless.')

        print('Performing parts list merge using unowned parts lists at: {}, and owned parts lists at: {}'.format(
            ', '.join([str(parts_list.path) for parts_list in unowned_parts_lists]),
            ', '.join([str(parts_list.path) for parts_list in owned_parts_lists])
        ))

        output_parts_list = Operations.union(*unowned_parts_lists, *owned_parts_lists)
    elif intersection:
        if (len(unowned_parts_lists) + len(owned_parts_lists) == 0):
            raise RuntimeError('No parts lists provided, thus the \'intersection\' would be pointless.')

        print('Performing parts list intersection using unowned parts lists at: {}, and owned parts lists at: {}'.format(
            ', '.join([str(parts_list.path) for parts_list in unowned_parts_lists]),
            ', '.join([str(parts_list.path) for parts_list in owned_parts_lists])
        ))

        output_parts_list = Operations.intersection(*unowned_parts_lists, *owned_parts_lists)
    else:
        raise RuntimeError('No valid command was supplied.')

    ## (Semi)gracefully handle weird failure edge cases
    if output_parts_list == None:
        raise RuntimeError('Unable to proceed with a None \'output_parts_list\' variable.')

    _dump_parts_list(output_parts_list)

    ## Save the output PartsList for future use
    if save_format == SaveFormat.CSV.value:
        output_parts_list.export_csv(save_path)
    elif save_format == SaveFormat.SIMPLE_CSV.value:
        output_parts_list.export_simple_csv(save_path)
    ## elif as new formats are implemented


if __name__ == '__main__':
    ## Disable specific pylint error that arises due to using Click for the CLI
    ## pylint:disable=no-value-for-parameter
    main()
