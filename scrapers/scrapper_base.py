from collections.abc import Callable
from typing import NamedTuple, Optional
from enum import Enum
import bs4


class Text_Type(Enum):
    CAMPAIGN = 1
    SUBRACE = 2
    DESCRIPTION = 3
    SUBCATEGORY = 4
    SUBCATEGORY_DESCRIPTION = 5
    SUBCATEGORY_EXPANSION = 6


class Text:

    __slots__ = ('main_text', 'sub_text', 'depth',
                 'expected_depth', 'parent', 'category', 'marker', 'is_single_text')

    def __init__(self, main_text: str, depth: int, expected_depth: int, category: int = None, marker: str = '', parent=None, is_single_text: bool = False) -> None:
        self.main_text: str = main_text
        self.depth: int = depth
        self.expected_depth: int = expected_depth
        self.parent: Optional[Text] = parent
        self.category: Text_Type = category
        self.sub_text: list[Text] = []
        self.marker: str = marker
        self.is_single_text: bool = is_single_text

    def append(self, text):
        self.sub_text.append(text)

    def add_to_main_text(self, text: str):
        self.main_text += text

    def print_list_of_sub_text(self):
        text = ''
        for sub_text in self.sub_text:
            text += str(sub_text)
        return text

    def __repr__(self) -> str:
        return f"{' '*(2*self.depth)}{self.marker}{self.main_text}\n{self.print_list_of_sub_text()}"


def get_element(l: list[Text], position_map: list[int]) -> Text:
    if len(position_map) == 0:
        raise IndexError("The position_level must have at least one index")
    for (index, pos) in enumerate(position_map[0:-1]):
        if pos >= len(l):
            raise IndexError(
                f'The index number {index} of the position_map is out of bounds')
        l = l[pos].sub_text
    return l[position_map[-1]]


def get_last_element(text_sequence: Text) -> Text:
    if len(text_sequence.sub_text) == 0:
        return text_sequence[-1]
    return get_last_element(text_sequence.sub_text[-1])


def _get_last_element_with_index(text_sequence: Text, index: list[int]) -> tuple[Text, list[int]]:
    if len(text_sequence.sub_text) == 0:
        return (text_sequence, index)
    index.append(len(text_sequence.sub_text) - 1)
    return _get_last_element_with_index(text_sequence.sub_text[-1], index)


def get_last_element_with_index(text_sequence: Text) -> tuple[Text, list[int]]:
    index: list[int] = []
    return _get_last_element_with_index(text_sequence, index)


class Hierarchy_Identifier(NamedTuple):
    expected_depth: int
    check: Callable[[bs4.Tag], bool]
    marker: str
    text_type: Text_Type


class Scrapper:

    def __init__(self) -> None:
        self.identifiers: list[Callable[[bs4.Tag], bool]] = []
        self.hierarchy_table: list[Hierarchy_Identifier] = []
        self.should_be_parsed: list[Callable[[bs4.Tag], bool]] = []
        self.should_be_treated_as_text: list[Callable[[bs4.Tag], bool]] = []
        self.single_text_category: Text_Type = None
        self.TEXT_EXPECTED_DEPTH = 100
        self._current_index: list[int] = []

    def get_text_from_just_this_tag(self, tag: bs4.Tag, ignore: Callable[[bs4.Tag], bool] = None) -> str:
        text = ''
        for tg in tag.contents:
            if tg.name is None or ignore(tg):
                text += tg.text.replace('\n', '')
        return text

    def add_to_hierarchy(self, depth: int, identifier: Callable[[bs4.Tag], bool], text_type: Text_Type, marker=''):
        self.hierarchy_table.append(Hierarchy_Identifier(
            depth, identifier, marker, text_type))

    def add_identifier(self, *identifier: list[Callable[[bs4.Tag], bool]]):
        self.identifiers.extend(identifier)

    def add_should_treat_as_text(self, f: Callable[[bs4.Tag], bool]):
        self.should_be_treated_as_text.append(f)

    def add_should_be_parsed(self, f: Callable[[bs4.Tag], bool]):
        self.should_be_parsed.append(f)

    def check_for_hierarchy(self, xml_element: bs4.Tag) -> Hierarchy_Identifier:
        for h in self.hierarchy_table:
            if h.check(xml_element):
                return h
        return ()

    def check_for_should_be_parsed(self, xml_element: bs4.Tag) -> bool:
        for f in self.should_be_parsed:
            if f(xml_element):
                return True
        return False

    def check_for_should_be_treated_as_text(self, xml_element: bs4.Tag) -> bool:
        for f in self.should_be_treated_as_text:
            if f(xml_element):
                return True
        return False

    def parse_element_and_add_to_a_list(self, xml_element: bs4.Tag, current_depth: int, parsed_location: list[Text]) -> int:

        if xml_element.text == '\n':
            return current_depth

        hierarchy = self.check_for_hierarchy(xml_element)
        should_be_treated_as_text = self.check_for_should_be_treated_as_text(
            xml_element)
        should_be_parsed = self.check_for_should_be_parsed(xml_element)

        # Is a text
        if xml_element.name is None or should_be_treated_as_text:
            cleaned_text = xml_element.text.replace('\n', '')

            if not parsed_location:
                temp_text = Text(cleaned_text, 0,
                                 self.TEXT_EXPECTED_DEPTH, self.single_text_category)
                parsed_location.append(temp_text)
                current_depth = self.TEXT_EXPECTED_DEPTH
                self._current_index = [0, 0]
                return current_depth

            (parent, index) = get_last_element_with_index(parsed_location[-1])
            index.insert(0, len(parsed_location) - 1)
            # print('Aqui:', get_element(parsed_location, index))

            if parent.is_single_text:
                parent = parent.parent

            if len(parent.sub_text) == 0:
                temp_text = Text(cleaned_text, parent.depth + 1,
                                 self.TEXT_EXPECTED_DEPTH, self.single_text_category, parent=parent, is_single_text=True)
                parent.append(temp_text)
                current_depth = self.TEXT_EXPECTED_DEPTH
                index.append(0)
                self._current_index = index
            else:
                child: Text = parent.sub_text[-1]
                child.add_to_main_text(cleaned_text)
        # should be butchered
        elif should_be_parsed:
            # print(xml_element.contents)
            for xml_child in xml_element.contents:
                current_depth = self.parse_element_and_add_to_a_list(
                    xml_child, current_depth, parsed_location)
        # Is a Tag
        elif hierarchy:
            cleaned_text = xml_element.text.replace('\n', '')

            if hierarchy.expected_depth == 0:
                current_depth = 0
                self._current_index.clear()
                self._current_index.append(len(parsed_location))
                parsed_location.append(
                    Text(cleaned_text, 0, 0, hierarchy.text_type, hierarchy.marker))
            elif hierarchy.expected_depth > current_depth:
                current_depth = hierarchy.expected_depth
                if not self._current_index:
                    current_sub_text_parent_sub_text_len = 0
                    self._current_index.append(0)
                    parsed_location.append(
                        Text(cleaned_text, 0, hierarchy.expected_depth, hierarchy.text_type, hierarchy.marker))
                else:
                    parent = get_element(parsed_location, self._current_index)
                    current_sub_text_parent_sub_text_len = len(
                        parent.sub_text)
                    if current_sub_text_parent_sub_text_len == 0:
                        self._current_index.append(0)
                    else:
                        self._current_index[-1] = current_sub_text_parent_sub_text_len

                    temp_text = Text(
                        cleaned_text, parent.depth + 1, hierarchy.expected_depth, hierarchy.text_type, hierarchy.marker, parent)

                    parent.append(temp_text)
            elif hierarchy.expected_depth <= current_depth:
                child = get_element(parsed_location, self._current_index)
                current_parent = child
                for went_back in range(1, current_depth - hierarchy.expected_depth + 2):
                    current_parent = current_parent.parent
                    if hierarchy.expected_depth > current_parent.expected_depth:
                        self._current_index = self._current_index[:-went_back]
                        current_sub_text_parent_sub_text_len = len(
                            current_parent.sub_text)
                        self._current_index.append(
                            current_sub_text_parent_sub_text_len)

                        temp_text = Text(cleaned_text, current_parent.depth + 1,
                                         hierarchy.expected_depth, hierarchy.text_type, hierarchy.marker, current_parent)
                        current_parent.append(temp_text)
                current_depth = hierarchy.expected_depth

        return current_depth

    def parse_string(self, page: str, skipped: int) -> list[Text]:
        parsed_text: list[Text] = []

        xml_tree = bs4.BeautifulSoup(page, features='html.parser')

        current_depth = 0
        self._current_index.clear()

        identifiers = self.identifiers

        def all_identifier(tag: bs4.Tag):
            for identifier in identifiers:
                if identifier(tag):
                    return True
            return False

        for xml_element in xml_tree.find_all(all_identifier)[skipped:]:
            current_depth = self.parse_element_and_add_to_a_list(
                xml_element, current_depth, parsed_text)

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
