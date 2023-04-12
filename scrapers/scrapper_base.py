from collections.abc import Callable
from typing import NamedTuple, Optional
from text_type import Text_Type
from bs4 import Tag, BeautifulSoup
from pandas import DataFrame
from collections import Counter


def _clean_text(s: str) -> str:
    s = s.replace('\n', '')
    s = s.replace('\n\r', '')
    s = s.replace('\t', '')
    return s


class ObjectBase:

    __slots__ = ('depth',
                 'expected_depth', 'marker', 'children', 'parent', 'category', 'root', 'associated_text_category')

    def __init__(self, depth: int, expected_depth: int, category: Text_Type, marker: str, parent, root, associated_text_category: Text_Type) -> None:
        self.depth: int = depth
        self.expected_depth: int = expected_depth
        self.marker: str = marker
        self.parent: Optional[ObjectBase] = parent
        self.children: list[ObjectBase] = []
        self.category: Text_Type = category
        self.associated_text_category: Text_Type = associated_text_category
        self.root: Optional[ObjectBase] = root

    def append(self, obj):
        self.children.append(obj)


class Text(ObjectBase):

    __slots__ = ('main_text', 'is_single_text')

    def __init__(self, main_text: str, depth: int, expected_depth: int, category: int, associated_text_category: Text_Type, marker: str = '', parent=None, is_single_text: bool = False, root=None) -> None:
        self.main_text: str = main_text
        self.is_single_text: bool = is_single_text
        super().__init__(depth, expected_depth, category,
                         marker, parent, root, associated_text_category)

    def add_to_main_text(self, text: str):
        self.main_text += text

    def print_list_of_sub_text(self):
        text = ''
        for sub_text in self.children:
            text += str(sub_text)
        return text

    def __repr__(self) -> str:
        return f"{' '*(2*self.depth)}{self.marker}{self.main_text}\n{self.print_list_of_sub_text()}"


class Table(ObjectBase):

    __slots__ = ('table', 'size')

    def __init__(self, depth: int, expected_depth: int, category: int, associated_text_category: Text_Type, marker: str = '', parent=None, root=None) -> None:
        super().__init__(depth, expected_depth, category,
                         marker, parent, root, associated_text_category)
        self.table: list[list[str]] = []
        # Size of rows is not guaranteed, it's only the most common amount of rows
        self.size: tuple[int, int] = ()

    def most_common_table_size(self) -> tuple[int, int]:
        table_size: list[int] = []
        for l in self.table:
            table_size.append(len(l))

        x_table_size = Counter(table_size).most_common(1)[0][0]
        y_table_size = len(self.table)
        return (x_table_size, y_table_size)

    def trim(self, to_be_trimmed: list[list[str]]) -> list[list[str]]:
        if len(to_be_trimmed) < 2:
            return to_be_trimmed

        copied_table = to_be_trimmed.copy()

        table_size: list[int] = []
        for l in to_be_trimmed:
            table_size.append(len(l))

        (x, _) = self.size

        removed: int = 0

        for (index, value) in enumerate(table_size):
            if value != x:
                copied_table.pop(index + removed)
                removed += 1

        return copied_table

    def parse_table_element_to_table(self, xml_element: Tag):
        if xml_element.name != 'table':
            raise TypeError(
                f'A table element should be passed but a {xml_element.name} was passed!')

        tr_list = xml_element.findChildren('tr')
        for tr in tr_list:
            td_text_list: list[str] = []
            for td in tr.children:
                text = _clean_text(td.text)
                if text:
                    td_text_list.append(text)
            self.table.append(td_text_list)

        self.size = self.most_common_table_size()

    def __repr__(self) -> str:
        safe_table = self.trim(self.table)
        if len(safe_table) == 0:
            return ''
        table = safe_table[1:]
        columns = safe_table[0]
        if len(safe_table) == 1:
            table = safe_table
            columns = None
        index = [' '*(2*self.depth) + self.marker]*(len(safe_table) - 1)
        frame = DataFrame(table, index=index, columns=columns)
        return '-There may be elements that dont fit that were excluded in this print!\n-' + frame.to_string(justify='center') + '\n'


def get_element(l: list[ObjectBase], position_map: list[int]) -> Text:
    if len(position_map) == 0:
        raise IndexError("The position_level must have at least one index")
    for (index, pos) in enumerate(position_map[0:-1]):
        if pos >= len(l):
            raise IndexError(
                f'The index number {index} of the position_map is out of bounds')
        l = l[pos].children
    return l[position_map[-1]]


def get_last_element(text_sequence: ObjectBase) -> ObjectBase:
    if len(text_sequence.children) == 0:
        return text_sequence[-1]
    return get_last_element(text_sequence.children[-1])


# TODO: MAKE SO INDEX IS NOT DEPENDANT ON BEING PASSED AS REFERENCE!
def _get_last_element_with_index(text_sequence: ObjectBase, index: list[int]) -> tuple[ObjectBase, list[int]]:
    if len(text_sequence.children) == 0:
        return (text_sequence, index)
    index.append(len(text_sequence.children) - 1)
    return _get_last_element_with_index(text_sequence.children[-1], index)


def get_last_element_with_index(text_sequence: ObjectBase) -> tuple[ObjectBase, list[int]]:
    index: list[int] = []
    return _get_last_element_with_index(text_sequence, index)


class Hierarchy_Identifier(NamedTuple):
    expected_depth: int
    check: Callable[[Tag], bool]
    marker: str
    text_type: Text_Type
    associated_text_type: Text_Type


class Scrapper:

    def __init__(self) -> None:
        self.identifiers: list[Callable[[Tag], bool]] = []
        self.hierarchy_table: list[Hierarchy_Identifier] = []
        self.hierarchy_table_for_tables: list[Hierarchy_Identifier] = []
        self.should_be_parsed: list[Callable[[Tag], bool]] = []
        self.should_be_treated_as_text: list[Callable[[Tag], bool]] = []
        self.single_text_category: Text_Type = None
        self.TEXT_EXPECTED_DEPTH = 100
        self._current_index: list[int] = []

    def get_text_from_just_this_tag(self, tag: Tag, ignore: Callable[[Tag], bool] = None) -> str:
        text = ''
        for tg in tag.contents:
            if tg.name is None or ignore(tg):
                text += _clean_text(tg.text)
        return text

    def add_to_hierarchy(self, depth: int, identifier: Callable[[Tag], bool], text_type: Text_Type, marker='', is_table: bool = False, associated_text_type: Optional[Text_Type] = None):
        associated_text_type = self.single_text_category if associated_text_type is None else associated_text_type
        if is_table:
            self.hierarchy_table_for_tables.append(Hierarchy_Identifier(
                depth, identifier, marker, text_type, associated_text_type))
        else:
            self.hierarchy_table.append(Hierarchy_Identifier(
                depth, identifier, marker, text_type, associated_text_type))

    def add_identifier(self, *identifier: list[Callable[[Tag], bool]]):
        self.identifiers.extend(identifier)

    def add_should_treat_as_text(self, f: Callable[[Tag], bool]):
        self.should_be_treated_as_text.append(f)

    def add_should_be_parsed(self, f: Callable[[Tag], bool]):
        self.should_be_parsed.append(f)

    def check_for_hierarchy(self, xml_element: Tag) -> Hierarchy_Identifier:
        for h in self.hierarchy_table:
            if h.check(xml_element):
                return h
        return ()

    def check_for_should_be_parsed(self, xml_element: Tag) -> bool:
        for f in self.should_be_parsed:
            if f(xml_element):
                return True
        return False

    def check_for_should_be_treated_as_text(self, xml_element: Tag) -> bool:
        for f in self.should_be_treated_as_text:
            if f(xml_element):
                return True
        return False

    def check_for_hierarchy_for_tables(self, xml_element: Tag) -> Hierarchy_Identifier:
        for h in self.hierarchy_table_for_tables:
            if h.check(xml_element):
                return h
        return ()

    def parse_element_and_add_to_a_list(self, xml_element: Tag, current_depth: int, parsed_location: list[ObjectBase]) -> int:

        if xml_element.text == '\n' or xml_element.text == '\r\n':
            return current_depth

        hierarchy = self.check_for_hierarchy(xml_element)
        should_be_treated_as_text = self.check_for_should_be_treated_as_text(
            xml_element)
        should_be_parsed = self.check_for_should_be_parsed(xml_element)
        table_hierarchy = self.check_for_hierarchy_for_tables(xml_element)

        # Is a text
        if xml_element.name is None or should_be_treated_as_text:
            cleaned_text = _clean_text(xml_element.text)

            if not parsed_location:
                temp_text = Text(cleaned_text, 0,
                                 self.TEXT_EXPECTED_DEPTH, self.single_text_category, None)
                parsed_location.append(temp_text)
                current_depth = self.TEXT_EXPECTED_DEPTH
                self._current_index = [0, 0]
                return current_depth

            (parent, index) = get_last_element_with_index(parsed_location[-1])
            index.insert(0, len(parsed_location) - 1)

            if type(parent) is Text and parent.is_single_text:
                parent = parent.parent

            if len(parent.children) == 0:
                temp_text = Text(cleaned_text, parent.depth + 1,
                                 parent.expected_depth + 1, parent.associated_text_category, None, parent=parent, is_single_text=True, root=parent.root)
                parent.append(temp_text)
                current_depth = parent.expected_depth + 1
                index.append(0)
                self._current_index = index
            else:
                child: Text = parent.children[-1]
                child.add_to_main_text(cleaned_text)
        # should be butchered
        elif should_be_parsed:
            for xml_child in xml_element.contents:
                current_depth = self.parse_element_and_add_to_a_list(
                    xml_child, current_depth, parsed_location)
        # Is table
        elif table_hierarchy:
            if table_hierarchy.expected_depth == 0:
                current_depth = 0
                self._current_index.clear()
                self._current_index.append(len(parsed_location))

                temp_table = Table(
                    0, 0, table_hierarchy.text_type, table_hierarchy.associated_text_type, table_hierarchy.marker)

                temp_table.parse_table_element_to_table(xml_element)

                parsed_location.append(temp_table)
            elif table_hierarchy.expected_depth > current_depth:
                current_depth = table_hierarchy.expected_depth
                if not self._current_index:
                    current_sub_text_parent_sub_text_len = 0
                    self._current_index.append(0)

                    temp_table = Table(
                        0, table_hierarchy.expected_depth, table_hierarchy.text_type, table_hierarchy.associated_text_type, table_hierarchy.marker)

                    temp_table.parse_table_element_to_table(xml_element)

                    parsed_location.append(temp_table)
                else:
                    parent = get_element(parsed_location, self._current_index)
                    current_sub_text_parent_sub_text_len = len(
                        parent.children)
                    if current_sub_text_parent_sub_text_len == 0:
                        self._current_index.append(0)
                    else:
                        self._current_index[-1] = current_sub_text_parent_sub_text_len

                    root = parent.root
                    if root is None:
                        root = parent

                    temp_table = Table(parent.depth + 1, table_hierarchy.expected_depth,
                                       table_hierarchy.text_type, table_hierarchy.associated_text_type, table_hierarchy.marker, parent, root)

                    temp_table.parse_table_element_to_table(xml_element)

                    parent.append(temp_table)
            elif table_hierarchy.expected_depth <= current_depth:
                child = get_element(parsed_location, self._current_index)
                current_parent = child
                for went_back in range(1, current_depth - table_hierarchy.expected_depth + 2):
                    current_parent: ObjectBase = current_parent.parent
                    if current_depth is None:
                        raise
                    if table_hierarchy.expected_depth > current_parent.expected_depth:
                        self._current_index = self._current_index[:-went_back]
                        current_sub_text_parent_sub_text_len = len(
                            current_parent.children)
                        self._current_index.append(
                            current_sub_text_parent_sub_text_len)

                        root = current_parent.root
                        if root is None:
                            root = current_parent

                        temp_table = Table(current_parent.depth + 1, table_hierarchy.expected_depth,
                                           table_hierarchy.text_type, table_hierarchy.associated_text_type, table_hierarchy.marker, current_parent, root)

                        temp_table.parse_table_element_to_table(xml_element)

                        current_parent.append(temp_table)
                current_depth = table_hierarchy.expected_depth
        # Is a Tag
        elif hierarchy:
            cleaned_text = _clean_text(xml_element.text)

            if hierarchy.expected_depth == 0:
                current_depth = 0
                self._current_index.clear()
                self._current_index.append(len(parsed_location))

                temp_text = Text(cleaned_text, 0, 0,
                                 hierarchy.text_type, hierarchy.associated_text_type, hierarchy.marker)

                parsed_location.append(temp_text)
            elif hierarchy.expected_depth > current_depth:
                current_depth = hierarchy.expected_depth
                if not self._current_index:
                    current_sub_text_parent_sub_text_len = 0
                    self._current_index.append(0)

                    temp_text = Text(
                        cleaned_text, 0, hierarchy.expected_depth, hierarchy.text_type, hierarchy.associated_text_type, hierarchy.marker)

                    parsed_location.append(temp_text)
                else:
                    parent = get_element(parsed_location, self._current_index)
                    current_sub_text_parent_sub_text_len = len(
                        parent.children)
                    if current_sub_text_parent_sub_text_len == 0:
                        self._current_index.append(0)
                    else:
                        self._current_index[-1] = current_sub_text_parent_sub_text_len

                    root = parent.root
                    if root is None:
                        root = parent

                    temp_text = Text(
                        cleaned_text, parent.depth + 1, hierarchy.expected_depth, hierarchy.text_type, hierarchy.associated_text_type, hierarchy.marker, parent, root=root)

                    parent.append(temp_text)
            elif hierarchy.expected_depth <= current_depth:
                child = get_element(parsed_location, self._current_index)
                current_parent = child
                for went_back in range(1, child.depth + 1):
                    current_parent: ObjectBase = current_parent.parent
                    if current_parent is None:
                        raise
                    if hierarchy.expected_depth > current_parent.expected_depth:
                        self._current_index = self._current_index[:-went_back]
                        current_sub_text_parent_sub_text_len = len(
                            current_parent.children)
                        self._current_index.append(
                            current_sub_text_parent_sub_text_len)

                        root = current_parent.root
                        if root is None:
                            root = current_parent

                        temp_text = Text(cleaned_text, current_parent.depth + 1,
                                         hierarchy.expected_depth, hierarchy.text_type, hierarchy.associated_text_type, hierarchy.marker, current_parent, root=root)
                        current_parent.append(temp_text)
                        break
                current_depth = hierarchy.expected_depth

        return current_depth

    def parse_string(self, page: str, skipped: int, show_identified_elements: bool = False) -> list[Text]:
        parsed_text: list[ObjectBase] = []

        # Instalar lxml com o pip. Ou trocar 'lxml' por 'html.parser'
        xml_tree = BeautifulSoup(page, features='lxml')

        current_depth = 0
        self._current_index.clear()

        identifiers = self.identifiers

        def all_identifier(tag: Tag):
            for identifier in identifiers:
                if identifier(tag):
                    return True
            return False

        if show_identified_elements:
            print(xml_tree.find_all(all_identifier))
        for xml_element in xml_tree.find_all(all_identifier)[skipped:]:
            current_depth = self.parse_element_and_add_to_a_list(
                xml_element, current_depth, parsed_text)

        return parsed_text


# def is_p(tag: Tag):
#     return tag.name == 'p'


# def is_h1(tag: Tag):
#     return tag.name == 'h1'


# def is_h2(tag: Tag):
#     return tag.name == 'h2'


# def general(tag: Tag):
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

#     def gn(tag: Tag):
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
