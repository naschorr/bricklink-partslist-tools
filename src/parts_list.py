import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import List

from part import Part

class PartsList:
    def __init__(self, path: Path = None):
        self.path = path
        self.parts = {} # bricklink id -> Part instance
        self._header: List[str] = None

        if (self.path != None):
            self._import_list(self.path)

    ## Magic Methods

    def __eq__(self, other: "PartsList") -> bool:
        if (other is None or not isinstance(other, PartsList)):
            return False

        if (self.path != other.path):
            return False

        if (len(self._header) != len(other._header) or any(s != o for s, o in zip(self._header, other._header))):
            return False

        if (len(self.parts) != len(other.parts) or any(s != o for s, o in zip(self.parts, other.parts))):
            return False

        return True


    ## Methods

    def _import_list(self, path: Path, csv_delimiter = ','):
        ## Safe assumptions prior to loading the .csv
        if (not isinstance(path, Path)):
            raise RuntimeError('Unable to import non Path object.')
        if (not path.exists()):
            raise RuntimeError('Provided path doesn\'t exit.')
        if (path.is_dir()):
            raise RuntimeError('Provided path represents a directory, and cannot be imported.')
        if (path.suffix != '.csv'):
            raise RuntimeError('Provided path doesn\'t resolve to a .csv file.')

        ## Clean slate
        self.path = path
        self.parts = {}

        ## Perform the import
        with open(path) as csv_file:
            reader = csv.reader(csv_file)
            self._header = reader.__next__()

            for row in reader:
                ## Ignore any rows with a falsy bricklink id (ex: the summary lines at the bottom), and anything that comes after
                if (row[0] == None or row[0] == ''):
                    return

                part = Part(row)

                ## Index the part based on its Bricklink ID and its color, so we don't have accidental collisions
                self.parts[part.id] = part


    def set_any_color(self, colors: List[str]):
        part: Part
        for part in self.parts.values():
            ## There's definitely a way to cache colors upon init, but premature optimization is bad. Also this doesn't
            ## have to be a super performant script, so I'm not very worried at the moment.
            for color in colors:
                if (part.is_color_match(color)):
                    del self.parts[part.id]

                    part.enable_any_color()

                    self.parts[part.id] = part


    def clone(self) -> "PartsList":
        return deepcopy(self)

    ## Export Methods

    def export_csv(self, target: Path):
        '''
        Exports a full-fat CSV with the same fields it was generated with, just using the updated values
        '''

        print('Exporting CSV to {}'.format(target))
        with open(target, 'w+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self._header)

            part: Part
            for part in self.parts.values():
                writer.writerow(part.to_csv())


    def export_simple_csv(self, target: Path):
        '''
        Builds an exports the bare minimum CSV for describing a collection of parts.
        There are 'part', 'color', and 'quantity' fields, and the whole thing is ready for Rebrickable integration
        '''

        print('Exporting simple CSV to {}'.format(target))
        with open(target, 'w+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['part', 'color', 'quantity'])

            part: Part
            for part in self.parts.values():
                writer.writerow(part.to_simple_csv())
