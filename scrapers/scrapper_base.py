from collections.abc import Callable
from typing import NamedTuple, Optional
from enum import Enum
import bs4


class Text_Type(Enum):
    MAIN_CATEGORY = 1
    DESCRIPTION = 2
    SUBCATEGORY = 3
    SUBCATEGORY_DESCRIPTION = 4


class Text:

    __slots__ = ('main_text', 'sub_text', 'depth',
                 'expected_depth', 'parent', 'category', 'marker')

    def __init__(self, main_text: str, depth: int, expected_depth: int, category: int = None, marker: str = '', parent=None) -> None:
        self.main_text: str = main_text
        self.depth: int = depth
        self.expected_depth: int = expected_depth
        self.parent: Optional[Text] = parent
        self.category: Text_Type = category
        self.sub_text: list[Text] = []
        self.marker: str = marker

    def print_list_of_sub_text(self):
        text = ''
        for sub_text in self.sub_text:
            text += str(sub_text)
        return text

    def __repr__(self) -> str:
        return f"{' '*(2*self.depth)}{self.marker}{self.main_text}\n{self.print_list_of_sub_text()}"

    def have_parent(self):
        if self.parent is None:
            return False
        return True


def get_element(l: list[Text], position_map: list[int]) -> Text:
    if len(position_map) == 0:
        raise IndexError("The position_level must have at least one index")
    for (index, pos) in enumerate(position_map[0:-1]):
        if pos >= len(l):
            raise IndexError(
                f'The index number {index} of the position_map is out of bounds')
        l = l[pos].sub_text
    return l[position_map[-1]]


class Hierarchy_Identifier(NamedTuple):
    expected_depth: int
    check: Callable[[bs4.Tag], bool]
    marker: str
    text_type: Text_Type
    should_ignore_children_text: bool
    should_check_all_children: bool


class Scrapper:

    def __init__(self) -> None:
        self.identifiers: list[Callable[[bs4.Tag], bool]] = []
        self.hierarchy_table: list[Hierarchy_Identifier] = []

    def get_text_from_just_this_tag(self, tag: bs4.Tag) -> str:
        text = ''
        for tg in tag.contents:
            if tg.name is None:
                text += tg.text
        return text

    def add_to_hierarchy(self, depth: int, identifier: Callable[[bs4.Tag], bool], text_type: Text_Type, should_ignore_children_text: bool = False, should_check_all_children: bool = False, marker: str = ''):
        self.hierarchy_table.append(Hierarchy_Identifier(
            depth, identifier, marker, text_type, should_ignore_children_text, should_check_all_children))

    def add_identifier(self, *identifier: list[Callable[[bs4.Tag], bool]]):
        self.identifiers.extend(identifier)

    def parse_element_and_add_to_a_list(self, xml_element: bs4.Tag, current_depth: int, current_index: list[int], parsed_location: list[Text]) -> int:
        for (expected_depth, check, marker, text_type, should_ignore_children_text, should_check_all_children) in self.hierarchy_table:
            if check(xml_element):
                cleaned_text = ''
                if should_ignore_children_text:
                    cleaned_text = self.get_text_from_just_this_tag(
                        xml_element)
                else:
                    cleaned_text = xml_element.text.replace('\n', '')
                if expected_depth == 0:
                    current_depth = 0
                    current_index.clear()
                    current_index.append(len(parsed_location))
                    parsed_location.append(
                        Text(cleaned_text, 0, 0, text_type, marker))
                elif expected_depth > current_depth:
                    current_depth = expected_depth
                    if not current_index:
                        current_sub_text_parent_sub_text_len = 0
                        current_index.append(0)
                        parsed_location.append(
                            Text(cleaned_text, 0, expected_depth, text_type, marker))
                    else:
                        parent = get_element(parsed_location, current_index)
                        current_sub_text_parent_sub_text_len = len(
                            parent.sub_text)
                        if current_sub_text_parent_sub_text_len == 0:
                            current_index.append(0)
                        else:
                            current_index[-1] = current_sub_text_parent_sub_text_len
                        parent.sub_text.append(
                            Text(cleaned_text, parent.depth + 1, expected_depth, text_type, marker, parent))
                elif expected_depth <= current_depth:
                    child = get_element(parsed_location, current_index)
                    parent = child
                    for went_back in range(1, child.depth + 1):
                        current_parent = parent.parent
                        if expected_depth > current_parent.expected_depth:
                            current_index = current_index[:-went_back]
                            current_sub_text_parent_sub_text_len = len(
                                current_parent.sub_text)
                            current_index.append(
                                current_sub_text_parent_sub_text_len)
                            current_parent.sub_text.append(
                                Text(cleaned_text, current_parent.depth + 1, expected_depth, text_type, marker, current_parent))
                    current_depth = expected_depth

                if should_check_all_children:
                    for xml_child in xml_element.contents:
                        if not xml_child.name is None:
                            current_depth = self.parse_element_and_add_to_a_list(
                                xml_child, current_depth, current_index, parsed_location)
        return current_depth

    def parse_string(self, page: str, skipped: int) -> list[Text]:
        parsed_text: list[Text] = []

        xml_tree = bs4.BeautifulSoup(page, features='html.parser')

        current_depth = 0
        current_index: list[int] = []

        identifiers = self.identifiers

        def all_identifier(tag: bs4.Tag):
            for identifier in identifiers:
                if identifier(tag):
                    return True
            return False

        for xml_element in xml_tree.find_all(all_identifier)[skipped:]:
            current_depth = self.parse_element_and_add_to_a_list(
                xml_element, current_depth, current_index, parsed_text)

        return parsed_text


# def is_p(tag: bs4.Tag):
#     return tag.name == 'p'


# def is_h1(tag: bs4.Tag):
#     return tag.name == 'h1'


# def is_h2(tag: bs4.Tag):
#     return tag.name == 'h2'


# def general(tag: bs4.Tag):
#     return is_p(tag) or is_h1(tag)


# test = """<h1>test6<h2>test7</h2></h1>
# <p>test</p>
# <h1>test2</h1>
# <h1>test3</h1>
# <h1>test8</h1>
# <p>test4</p>
# <h1>test5</p>
# """


# def tst(text: str):
#     hierarchy = [is_p, is_h1, is_h2]

#     def gn(tag: bs4.Tag):
#         last = False
#         for i in hierarchy:
#             last = last or i(tag)
#         return last

#     xml_tree = bs4.BeautifulSoup(text, features='html.parser')

#     return xml_tree.find_all(gn)


# s = Scrapper()
# s.add_identifier(is_p)
# s.add_identifier(is_h1)
# s.add_to_hierarchy(0, is_p, Text_Type.MAIN_CATEGORY)
# s.add_to_hierarchy(1, is_h1, Text_Type.DESCRIPTION, True, True, '<->')
# s.add_to_hierarchy(
#     2, is_h2, Text_Type.SUBCATEGORY_DESCRIPTION, True, marker='->')

# k = s.parse_string(test, 0)
# print(get_element(k, [1, 0]).depth)

# for i in k:
#     print(i)


# add_identifiers(is_p)
# parse_string('http://dnd5e.wikidot.com/lineage:aasimar', 2)
