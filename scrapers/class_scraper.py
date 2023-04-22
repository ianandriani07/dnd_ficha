from scrapper_base import Scrapper, Text_Type as tt
import requests as rq
from bs4 import Tag

############# GENERIC #####################


def is_p_with_em_as_child(tag: Tag):  # Descrição da classe
    return tag.name == 'p' and not tag.findChild('em') is None


def is_p(tag: Tag):  # Descrições genericas
    return tag.name == 'p'


def is_table(tag: Tag):  # Tabelas genéricas
    return tag.name == 'table'


def is_h_something_with_toc(tag: Tag):  # Títulos genéricos
    return tag.name.find('h') != -1 and (not tag.attrs.get('id') is None and tag.attrs.get('id').find('toc') != -1)


def is_ul_with_special_div_parent(tag: Tag):  # Expansões genéricas
    return tag.name == 'ul' and (not tag.findParent('div') is None and 'col-lg-12' in tag.findParent('div').attrs.get('class'))
##############################################
############# SEPARATION #####################


def is_p_with_em_and_strong_as_child(tag: Tag):
    return tag.name == 'p' and not tag.findChild('em') is None and not tag.findChild('strong') is None


def is_table_with_div_id(tag: Tag):
    return tag.name == 'table' and not tag.findParent('div').attrs.get('id') is None


def is_h1(tag: Tag):
    return tag.name == 'h1'


def is_h3(tag: Tag):
    return tag.name == 'h3'


def is_h5(tag: Tag):
    return tag.name == 'h5'


def is_p_with_strong_child(tag: Tag):
    return tag.name == 'p' and not tag.findChild('strong') is None


def is_strong(tag: Tag):
    return tag.name == 'strong'


def is_ul(tag: Tag):
    return tag.name == 'ul'


def is_li(tag: Tag):
    return tag.name == 'li'


def is_table_with_div_special_class_parent(tag: Tag):
    return tag.name == 'table' and (not tag.findParent('div') is None and 'col-lg-12' in tag.findParent('div').attrs.get('class'))


scrapper = Scrapper()

scrapper.add_identifier(is_p, is_h_something_with_toc,
                        is_ul_with_special_div_parent, is_table)

scrapper.add_to_hierarchy(0, is_p_with_em_and_strong_as_child,
                          tt.C_MAIN_DESCRIPTION, '<->')
scrapper.add_to_hierarchy(0, is_p_with_em_as_child, tt.C_MULTICLASS_REQ, '&')
scrapper.add_to_hierarchy(0, is_table_with_div_id,
                          tt.C_MAIN_CLASS_INFO_TABLE, '', True)
scrapper.add_to_hierarchy(0, is_h1, tt.C_CLASS_FEATURES,
                          '->')
scrapper.add_to_hierarchy(1, is_h5, tt.C_BASIC_FEATURES, '->')
scrapper.add_to_hierarchy(2, is_strong, tt.C_BASIC_FEATURES_CATEGORY,
                          '*>', associated_text_type=tt.C_BASIC_FEATURES_CATEGORY_DESCRIPTION)
scrapper.add_should_be_parsed(is_p_with_strong_child)
scrapper.add_to_hierarchy(1, is_h3, tt.C_SPECIAL_FEATURES_CATEGORY, '->')
scrapper.add_to_hierarchy(2, is_p, tt.C_FEATURES_DESCRIPTION)
scrapper.add_should_be_parsed(is_ul)
scrapper.add_to_hierarchy(3, is_li, tt.C_FEATURES_EXPANSION, '*')
scrapper.add_to_hierarchy(2, is_table_with_div_special_class_parent,
                          tt.C_SPECIAL_FEATURES_CATEGORY_TABLE, is_table=True)


link = input('Classe: ')
web_page_text = rq.get(link).text
# file_name = input('Nome do arquivo: ')


data = []

data = scrapper.parse_string(web_page_text, 0)

for i in data:
    print(i)
