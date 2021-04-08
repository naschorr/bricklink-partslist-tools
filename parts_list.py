import csv
import json
from pathlib import Path

from part import Part

class PartsList:
    def __init__(self, path: Path):
        self.path = path
        self.parts = {} # bricklink id -> Part instance
        self._header = None

        self._import_list(self.path)


    def _import_list(self, path: Path, csv_delimiter = ','):
        ## Safe assumptions prior to loading the .csv
        assert(path.exists())
        assert(not path.is_dir())
        assert(path.suffix == '.csv')

        with open(path) as csv_file:
            reader = csv.reader(csv_file)
            self._header = reader.__next__()

            for row in reader:
                ## Ignore any rows with a falsy bricklink id (ex: the summary lines at the bottom), and anything that comes after
                if (row[0] == None or row[0] == ''):
                    return

                part = Part(row, delimiter = csv_delimiter)

                ## Index the part based on its Bricklink ID and its color, so we don't have accidental collisions
                self.parts[part.id] = part


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


    def convert_to_json(self) -> {}:
        '''
        Simple json export of the Parts contained in this PartsList
        '''

        parts = []

        part: Part
        for part in self.parts.values():
            part_id = part.bl_item_no
            color = part.color_name
            quantity = part.qty

            parts.append(
                {
                    'part': part_id,
                    'color': color,
                    'quantity': quantity
                }
            )

        return json.dumps(parts)
