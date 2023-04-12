from text_type import Text_Type as tt
from scrapper_base import Text, ObjectBase, Table
import json

for_the_nameless: int = 0


def _convert_single_ObjectBase_to_dict(text: ObjectBase, data: dict) -> dict:
    category: tt = text.category
    if type(text) == Text:
        if category == tt.L_CAMPAIGN:
            data[text.main_text] = {
                "desc": [],
                "body": {},
                "subraces": {}
            }
        elif category == tt.L_DESCRIPTION:
            # campaign.body.desc.append()
            if text.parent.category == tt.L_SUBRACE:
                subrace_name = text.parent.main_text
                data[text.root.main_text]['subraces'][subrace_name]['desc'].append(
                    text.main_text)
            elif text.parent.category == tt.L_CAMPAIGN:
                data[text.root.main_text]['desc'].append(text.main_text)
        elif category == tt.L_SUBRACE:
            # campaign.subraces.sub_race_name
            data[text.root.main_text]['subraces'][text.main_text] = {
                "desc": [],
                "body": {}
            }
        elif category == tt.L_CATEGORY:
            if text.parent.category == tt.L_SUBRACE:
                subrace_name = text.parent.main_text
                # campaign.subraces.subrace.body.category
                data[text.root.main_text]['subraces'][subrace_name]['body'][text.main_text] = {
                    "desc": {},
                    "subcategories": {}
                }
            elif text.parent.category == tt.L_CAMPAIGN:
                # campaign.body.category
                data[text.root.main_text]['body'][text.main_text] = {
                    "desc": {},
                    "subcategories": {}
                }
        elif category == tt.L_CATEGORY_DESCRIPTION:
            if text.parent.parent.category == tt.L_SUBRACE:
                subrace_name = text.parent.parent.main_text
                # campaign.subraces.subrace.body.category.desc -> desc is a list
                data[text.root.main_text]['subraces'][subrace_name]['body'][text.parent.main_text]['desc'][text.main_text] = []
            elif text.parent.parent.category == tt.L_CAMPAIGN:
                # campaign.body.category.desc -> desc is a list
                data[text.root.main_text]['body'][text.parent.main_text]['desc'][text.main_text] = []
        elif category == tt.L_CATEGORY_EXPANSION:
            if text.parent.parent.parent == tt.L_SUBRACE:
                subrace_name = text.parent.parent.parent.main_text
                category_name = text.parent.parent.main_text
                # campaign.subraces.subrace.body.category.desc.append()
                data[text.root.main_text]['subraces'][subrace_name]['body'][category_name]['desc'][text.parent.main_text].append(
                    text.main_text)
            elif text.parent.parent.parent == tt.L_CAMPAIGN:
                category_name = text.parent.parent.main_text
                # campaign.body.category.desc.append()
                data[text.root.main_text]['body'][category_name]['desc'][text.parent.main_text].append(
                    text.main_text)
        elif category == tt.L_SUBCATEGORY:
            if text.parent.parent.parent == tt.L_SUBRACE:
                subrace_name = text.parent.parent.parent.main_text
                category_name = text.parent.parent.main_text
                # campaign.subraces.subrace.body.category.subcategories.subcategory = ''
                data[text.root.main_text]['subraces'][subrace_name]['body'][category_name]['subcategories'][text.main_text] = ''
            elif text.parent.parent.parent == tt.L_CAMPAIGN:
                category_name = text.parent.parent.main_text
                # campaign.body.category.subcategories.subcategory = ''
                data[text.root.main_text]['body'][category_name]['desc'][text.main_text] = ''
        elif category == tt.L_SUBCATEGORY_DESCRIPTION:
            if text.parent.parent.parent.parent == tt.L_SUBRACE:
                subrace_name = text.parent.parent.parent.parent.main_text
                category_name = text.parent.parent.parent.main_text
                # campaign.subraces.subrace.body.category.subcategories.subcategory = ''
                data[text.root.main_text]['subraces'][subrace_name]['body'][category_name]['subcategories'][text.parent.main_text] = text.main_text
            elif text.parent.parent.parent.parent == tt.L_CAMPAIGN:
                category_name = text.parent.parent.main_text
                # campaign.body.category.subcategories.subcategory = ''
                data[text.root.main_text]['body'][category_name]['desc'][text.parent.main_text] = text.main_text
        elif category == tt.L_TABLE_NAME:
            if text.parent.category == tt.L_SUBRACE:
                subrace_name = text.parent.main_text
                # campaign.subraces.subrace.body.table_name
                data[text.root.main_text]['subraces'][subrace_name]['body'][text.main_text] = []
            elif text.parent.category == tt.L_CAMPAIGN:
                # campaign.body.table_name
                data[text.root.main_text]['body'][text.main_text] = []
    elif type(text) == Table:
        if category == tt.L_TABLE:
            if text.parent.category == tt.L_TABLE_NAME:
                if text.parent.parent.category == tt.L_SUBRACE:
                    subrace_name = text.parent.parent.main_text
                    # campaign.subraces.subrace.body.table_name = table
                    data[text.root.main_text]['subraces'][subrace_name]['body'][text.parent.main_text] = text.table
                elif text.parent.parent.category == tt.L_CAMPAIGN:
                    # campaign.body.table_name = table
                    data[text.root.main_text]['body'][text.parent.main_text] = text.table
            elif len(text.table[0]) == 1:
                name = text.table[0][0]
                if text.parent.category == tt.L_SUBRACE:
                    subrace_name = text.parent.main_text
                    # campaign.subraces.subrace.body.table_name = table
                    data[text.root.main_text]['subraces'][subrace_name]['body'][name] = text.table[1:]
                elif text.parent.category == tt.L_CAMPAIGN:
                    # campaign.body.table_name = table
                    data[text.root.main_text]['body'][name] = text.table[1:]
                elif text.parent.category == tt.L_DESCRIPTION:
                    name = text.table[0][0]
                    # campaign.body.table_name = table
                    data[text.root.main_text]['body'][name] = text.table[1:]
    return data


def convert_ObjetBase_to_dict(text: ObjectBase, data: dict = {}) -> dict:
    data = _convert_single_ObjectBase_to_dict(text, data)
    for t in text.children:
        data = convert_ObjetBase_to_dict(t, data)
    return data


def convert_ObjectBase_list_to_dict(text_list: list[Text]) -> dict:
    result: dict = {}
    for text in text_list:
        result = convert_ObjetBase_to_dict(text, result)
    return result


def convert_ObjectBase_to_JSON(text: Text) -> str:
    d: dict = convert_ObjetBase_to_dict(text)
    return json.dumps(d)


def convert_ObjectBase_list_to_JSON(text_list: Text):
    d: dict = convert_ObjectBase_list_to_dict(text_list)
    return json.dumps(d)
