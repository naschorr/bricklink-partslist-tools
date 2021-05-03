from typing import List

class Part:
    CSV_FIELDS = ['bl_item_no', 'element_id', 'l_draw_id', 'part_name', 'bl_color_id', 'l_draw_color_id', 'color_name', 'color_category', 'qty', 'weight']

    def __init__(self, csv_line: List[str], delimiter = ','):
        ## csv_line looks like: BLItemNo,ElementId,LdrawId,PartName,BLColorId,LDrawColorId,ColorName,ColorCategory,Qty,Weight
        self._bl_item_no = csv_line[0]
        self.element_id = csv_line[1]
        self.l_draw_id = csv_line[2]
        self.part_name = csv_line[3]
        self.bl_color_id = csv_line[4]
        self.l_draw_color_id = csv_line[5]
        self._color_name = csv_line[6]
        self.color_category = csv_line[7]
        self.qty = int(csv_line[8])
        self.weight = float(csv_line[9])

    ## Magic Methods

    def __sub__(self, other: "Part"):
        part = self.clone()
        part.qty -= other.qty
        part.weight -= other.weight

        ## Don't worry about tracking parts with quantity 0
        return part if part.qty > 0 else None


    def __add__(self, other: "Part"):
        part = self.clone()
        part.qty += other.qty
        part.weight += other.weight

        return part


    def __eq__(self, other: "Part") -> bool:
        ## Compare the relevant properties, and see if their values match up
        return not any(getattr(self, key) != getattr(other, key) for key in self.CSV_FIELDS)

    ## Properties

    @property
    def id(self) -> str:
        '''
        Build something unique enough to index the part on, collisions are fine since parts are interchangable
        '''

        return str(self.bl_item_no) + ':' + str(self.color_name)


    @property
    def bl_item_no(self) -> str:
        return self._bl_item_no


    @bl_item_no.setter
    def bl_item_no(self, value: str):
        self._bl_item_no = value


    @property
    def color_name(self) -> str:
        return self._color_name


    @color_name.setter
    def color_name(self, value: str):
        self._color_name = value

    ## Methods

    def to_csv(self) -> List[str]:
        return [str(getattr(self, field)) for field in self.CSV_FIELDS]


    def to_simple_csv(self) -> List[str]:
        return [self.bl_item_no, self.color_name, self.qty]


    def clone(self) -> "Part":
        return Part(self.to_csv())
