import click
from pathlib import Path
from typing import List

from enums import SaveFormat
from part import Part
from parts_list import PartsList


def _find_missing_parts(owned_parts_lists: List[PartsList], unowned_parts_list: PartsList) -> PartsList:
    '''
    Searches through a PartList of potentially unowned parts, and attempts to see if you've already got those parts
        available in the owned parts lists. If they're available, then remove them from the unowned parts list. Think
        of it like a right excluding join in SQL land.

    Parameters:
    owned_parts_lists (List[PartsList]): A list of PartsList instances representing all of the parts you'd like to
        search over
    unowned_parts_list (PartsList): A single PartsList instance that represents all of the parts that you need

    Returns:
    PartsList: The unowned_parts_list with all owned parts removed from it
    '''

    ## Don't mutate the unowned_parts_list
    missing_parts = unowned_parts_list.clone()

    for parts_list in owned_parts_lists:
        part: Part
        for part_id, part in parts_list.parts.items():
            if (part_id in missing_parts.parts):
                needed_part = missing_parts.parts[part_id] - part

                if (needed_part == None):
                    del missing_parts.parts[part_id]
                else:
                    missing_parts.parts[part_id] = needed_part

    return missing_parts


def _merge_parts_lists(*parts_lists: PartsList) -> PartsList:
    '''
    Combines all of the provided PartsList objects into a single one, containing all of the other's parts

    Parameters:
    parts_lists (PartsList): One more more PartList instances to be merged

    Returns:
    PartsList: A newly created PartsList instance with all of the input's parts added to it
    '''

    if len(parts_lists) == 0:
        raise RuntimeError('Unable to merge missing parts lists!')
    elif len(parts_lists) == 1:
        return parts_lists[0]

    merged_parts_list = PartsList()

    parts_list: PartsList
    for parts_list in parts_lists:
        part: Part
        for part_id, part in parts_list.parts.items():
            if part_id in merged_parts_list.parts:
                merged_part = merged_parts_list.parts[part_id] + part
            else:
                merged_part = part
            
            merged_parts_list.parts[part_id] = merged_part
    
    return merged_parts_list


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
@click.option('--missing-parts', is_flag = True, help = 'Choose to perform a check for missing parts, wherein a single unowned-parts-list is compared to one or more owned-parts-lists to find missing pieces.')
@click.option('--merge', is_flag = True, help = 'Choose to perform merge operation, merging all given (owned and unowned) parts lists together, and saving the result as a singular PartsList .csv file.')
@click.option('--owned-parts-list-path', '-o', type = click.Path(), multiple = True, help = 'A path to a Bricklink parts list .csv file representing parts that you own')
@click.option('--unowned-parts-list-path', '-u', type = click.Path(), multiple = True, help = 'A path to a Bricklink parts list .csv file representing parts that you do not own')
@click.option('--save-path', '-s', type = click.Path(), help = 'The path to export manipulated parts list data to')
@click.option('--save-format', '-f', type = click.Choice([save_format.value for save_format in SaveFormat], case_sensitive = False), help = 'The format to export manipulated parts list data in')
def main(
    missing_parts: bool,
    merge: bool,
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
        output_parts_list = _find_missing_parts(owned_parts_lists, unowned_parts_lists[0])
    elif merge:
        if (len(unowned_parts_lists) + len(owned_parts_lists) == 0):
            raise RuntimeError('No parts lists provided, thus the \'merge\' would be pointless.')

        print('Performing parts list merge using unowned parts lists at: {}, and owned parts lists at: {}'.format(
            ', '.join([str(parts_list.path) for parts_list in unowned_parts_lists]),
            ', '.join([str(parts_list.path) for parts_list in owned_parts_lists])
        ))
        output_parts_list = _merge_parts_lists(*unowned_parts_lists, *owned_parts_lists)
    ## elif as new commands are implemented
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
