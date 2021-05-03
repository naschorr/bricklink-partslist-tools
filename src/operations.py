from typing import List

from part import Part
from parts_list import PartsList

class Operations:

    @staticmethod
    def difference(parts_list_a: PartsList, parts_list_b: PartsList) -> PartsList:
        '''
        Performs the difference operation, subtracting the Parts in parts_list_b from parts_list_a, and returning the
        result.

        parts_list_a - parts_list_b

        Note that this isn't a true difference operation in the SQL sense of the word, as Parts within each PartsList
        are subtracted from each other. For example, let's say parts_list_a contained three red 2x4 bricks, and
        parts_list_b contained a single red 2x4 brick. This difference operation, after being performed, would result
        in a new PartsList containing two red 2x4 bricks.

        Parameters:
        parts_list_a (PartsList): The PartsList to subtract from (ex: A in A - B)
        parts_list_b (PartsList): The PartsList to subtract with (ex: B in A - B)

        Returns:
        PartsList: A newly created PartsList instance with all of the Parts from parts_list_a that don't exist inside
            parts_list_b
        '''

        difference = parts_list_a.clone()

        part: Part
        for part_id, part in parts_list_b.parts:
            if part_id in difference.parts:
                updated_part = difference.parts[part_id] - part

                if not updated_part:
                    del difference.parts[part_id]
                else:
                    difference.parts[part_id] = updated_part

        return difference


    @staticmethod
    def union(*parts_lists: List[PartsList]) -> PartsList:
        '''
        Performs the union operation upon all of the provided PartsLists.

        parts_lists[i] ∪ parts_lists[i + 1] ∪ ... ∪ parts_lists[n]

        Note that this isn't a true union operation in the SQL sense of the word, as Parts within each PartsList are
        merged together. For example, let's say you had a PartsList containing a single red 2x4 brick, and another
        with two red 2x4 bricks. This union operation will return a PartsList containing three red 2x4 bricks, as the
        traditional method isn't super useful within this context (and not obvious what the result should be).

        Parameters:
        parts_lists (PartsList): One more more PartList instances to be unioned together

        Returns:
        PartsList: A newly created PartsList instance with all of the input PartsLists' parts added to it
        '''

        if len(parts_lists) == 0:
            raise RuntimeError('Unable to union zero parts lists together!')
        elif len(parts_lists) == 1:
            return parts_lists[0]

        union = PartsList()

        parts_list: PartsList
        for parts_list in parts_lists:
            part: Part
            for part_id, part in parts_list.parts.items():
                if part_id in union.parts:
                    merged_part = union.parts[part_id] + part
                else:
                    merged_part = part
                
                union.parts[part_id] = merged_part
        
        return union


    @staticmethod
    def intersection(*parts_lists: List[PartsList]) -> PartsList:
        '''
        Performs the intersection operation, finding the common parts between all of the provided PartsLists.

        parts_lists[i] ∩ parts_lists[i + 1] ∩ ... ∩ parts_lists[n]

        Note that this isn't a true intersectopm operation in the SQL sense of the word, as Parts within each PartsList
        are compared with the other PartsLists.
        
        For example, let's say you had a PartsList containing five red 2x4 bricks, and two blue 1x1 bricks. Let's also
        say that there's another PartsList containing four red 1x3 bricks, and one blue 1x1 brick. After the
        intersection operation has completed, the result would be a new PartsList containing a single blue 1x1 brick.

        Parameters:
        parts_lists (PartsList): One more more PartList instances to be intersected together

        Returns:
        PartsList: A newly created PartsList instance containing the intersection of all the provided PartsLists
        '''

        if len(parts_lists) == 0:
            raise RuntimeError('Unable to intersect zero parts lists together!')
        elif len(parts_lists) == 1:
            return parts_lists[0]

        intersection: PartsList = parts_lists[0].clone()

        parts_list: PartsList
        for parts_list in parts_lists[1:]:
            part: Part
            for part_id, part in parts_list.parts.items():
                if part_id in intersection.parts:
                    if intersection.parts[part_id].qty > part.qty:
                        intersection.parts[part_id] = part

        return intersection
