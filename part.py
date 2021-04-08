from typing import List

class Part:
    CSV_FIELDS = ['bl_item_no', 'element_id', 'l_draw_id', 'part_name', 'bl_color_id', 'l_draw_color_id', 'color_name', 'color_category', 'qty', 'weight']

    def __init__(self, csv_line: List[str], delimiter = ','):
        self._source = csv_line

        ## csv_line looks like: BLItemNo,ElementId,LdrawId,PartName,BLColorId,LDrawColorId,ColorName,ColorCategory,Qty,Weight
        self.bl_item_no = csv_line[0]
        self.element_id = csv_line[1]
        self.l_draw_id = csv_line[2]
        self.part_name = csv_line[3]
        self.bl_color_id = csv_line[4]
        self.l_draw_color_id = csv_line[5]
        self.color_name = csv_line[6]
        self.color_category = csv_line[7]
        self.qty = int(csv_line[8])
        self.weight = float(csv_line[9])

        self.id = str(self.bl_item_no) + ':' + str(self.color_name)


    def __sub__(self, other):
        part = self.clone()
        part.qty -= other.qty
        part.weight -= other.weight

        ## Don't worry about tracking parts with quanity 0
        return part if part.qty > 0 else None


    def to_csv(self) -> List[str]:
        return [str(getattr(self, field)) for field in self.CSV_FIELDS]


    def to_simple_csv(self) -> List[str]:
        return [self.bl_item_no, self.color_name, self.qty]


    def clone(self):
        return Part(self._source)
