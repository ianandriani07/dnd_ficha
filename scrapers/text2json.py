from text_type import Text_Type as tt
from scrapper_base import Text


def _convert_single_Text_to_dict(text: Text, data: dict) -> dict:
    category: tt = text.category
    if category == tt.CAMPAIGN:
        should_be: str = 'body'
        if len(text.sub_text) != 0 and text.sub_text[0].category == tt.SUBRACE:
            should_be = 'subraces'
        data[text.main_text] = {
            "type": "CAMPAIGN",
            "desc": [],
            should_be: {}
        }
    elif category == tt.DESCRIPTION:
        # campaign.body.desc.append()
        data[text.root.main_text]['desc'].append(text.main_text)
    elif category == tt.SUBRACE:
        # campaign.subraces.sub_race_name
        data[text.root.main_text]['subraces'][text.main_text] = {
            "type": "SUBRACE",
            "body": {}
        }
    elif category == tt.CATEGORY:
        if text.parent.category == tt.SUBRACE:
            subrace_name = text.parent.main_text
            # campaign.subrace.body.category
            data[text.root.main_text][subrace_name]['body'][text.main_text] = {}
        elif text.parent.category == tt.CAMPAIGN:
            # campaign.body.category
            data[text.root.main_text]['body'][text.main_text] = {}
    elif category == tt.CATEGORY_DESCRIPTION:
        if text.parent.parent.category == tt.SUBRACE:
            subrace_name = text.parent.parent.main_text
            # campaign.subrace.body.category.desc -> desc is a list
            data[text.root.main_text]['subraces'][subrace_name]['body'][text.parent.main_text][text.main_text] = []
        elif text.parent.parent.category == tt.CAMPAIGN:
            # campaign.body.category.desc -> desc is a list
            data[text.root.main_text]['body'][text.parent.main_text][text.main_text] = []
    elif category == tt.CATEGORY_EXPANSION:
        if text.parent.parent.parent == tt.SUBRACE:
            subrace_name = text.parent.parent.parent.main_text
            category_name = text.parent.parent.main_text
            # campaign.subraces.body.category.desc.append()
            data[text.root.main_text]['subraces'][subrace_name]['body'][category_name][text.parent.main_text].append(
                text.main_text)
        elif text.parent.parent.parent == tt.CAMPAIGN:
            category_name = text.parent.parent.main_text
            # campaign.body.category.desc.append()
            data[text.root.main_text]['body'][category_name][text.parent.main_text].append(
                text.main_text)

    return data


def convert_Text_to_dict(text: Text, data: dict = {}) -> dict:
    data = _convert_single_Text_to_dict(text, data)
    for t in text.sub_text:
        data = convert_Text_to_dict(t, data)
    return data


def convert_Text_list_to_dict(text_list: list[Text]) -> dict:
    result: dict = {}
    for text in text_list:
        result = convert_Text_to_dict(text, result)
    return result
