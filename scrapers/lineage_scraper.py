import requests as rq
from bs4 import Tag
import scrapper_base as sb
from scrapper_base import Text
from text_type import Text_Type as tt
import text2json as tj


# A campanha de onde aquelas raças vieram ou subraças especificas para aquela campanha
def is_h1_or_h2_with_id_toc(tag: Tag):
    return (tag.name == 'h1' or tag.name == 'h2') and (not tag.attrs.get('id') is None and tag.attrs.get('id').find('toc') != -1)


def is_h1(tag: Tag):
    return tag.name == 'h1'


def is_h2(tag: Tag):
    return tag.name == 'h2'


# Descrição generica em itálico e negrito de subraças ou de raças de uma campanha especifica
def is_p_with_em_as_child(tag: Tag):
    return tag.name == 'p' and not tag.findChild('em') is None


# Categorias normais e sua descrições
def is_li_without_an_a_if_not_with_strong_as_child(tag: Tag):
    return tag.name == 'li' and (tag.findChild('a') is None or not tag.findChild('strong') is None) and tag.findParent('li') is None


def is_strong(tag: Tag):  # Categorias
    return tag.name == 'strong'


def is_a(tag: Tag):  # Tag a ser ignorada
    return tag.name == 'a'


# Categoria, descrição de categoria e expansão de categoria
def is_li_with_strong_as_child(tag: Tag):
    return tag.name == 'li' and not tag.findChild('strong') is None


# Expansão de categoria
def is_li_with_li_as_parent_without_em_as_child(tag: Tag):
    return tag.name == 'li' and not tag.findParent('li') is None and tag.findChild('em') is None


def is_li_with_li_as_parent_with_em_as_child(tag: Tag):
    return tag.name == 'li' and not tag.findParent('li') is None and not tag.findChild('em') is None

# Subcategoria


def is_em_with_li_as_parent(tag: Tag):
    return tag.name == 'em' and not tag.findParent('li') is None


def is_ul_with_li_as_parent(tag: Tag):  # Múltiplas expansões de categoria
    return tag.name == 'ul' and not tag.findParent('li') is None


def is_table(tag: Tag):  # Tabela
    return tag.name == 'table'


def is_p_without_em_as_child(tag: Tag):  # Nome da Tabela
    return tag.name == 'p' and tag.findChild('em') is None


scrapper = sb.Scrapper()
scrapper.add_identifier(is_h1_or_h2_with_id_toc, is_p_with_em_as_child,
                        is_li_without_an_a_if_not_with_strong_as_child, is_p_without_em_as_child, is_table)
scrapper.add_to_hierarchy(0, is_h1, tt.CAMPAIGN, marker='<->')
scrapper.add_to_hierarchy(1, is_h2, tt.SUBRACE, marker='->')
scrapper.add_to_hierarchy(2, is_p_with_em_as_child,
                          tt.DESCRIPTION, marker='')
scrapper.add_to_hierarchy(2, is_strong, tt.CATEGORY,
                          marker='•', associated_text_type=tt.CATEGORY_DESCRIPTION)
scrapper.add_to_hierarchy(2, is_p_without_em_as_child, tt.TABLE_NAME, '<*>')
scrapper.add_to_hierarchy(3, is_table, tt.TABLE, '-', True)
scrapper.add_to_hierarchy(4, is_li_with_li_as_parent_without_em_as_child,
                          tt.CATEGORY_EXPANSION, marker='-->')
scrapper.add_to_hierarchy(4, is_em_with_li_as_parent, tt.SUBCATEGORY,
                          marker='••', associated_text_type=tt.SUBCATEGORY_DESCRIPTION)
scrapper.add_should_be_parsed(is_li_with_strong_as_child)
scrapper.add_should_be_parsed(is_ul_with_li_as_parent)
scrapper.add_should_be_parsed(is_li_with_li_as_parent_with_em_as_child)
scrapper.add_should_treat_as_text(is_a)

# Pedir o site para o scraping relaciona a linhagens
link = input('Linhagem: ')
web_page_text = rq.get(link).text
# file_name = input('Nome do arquivo: ')


data: list[Text] = []

data = scrapper.parse_string(web_page_text, 0)

for i in data:
    print(i)

# json_text = tj.convert_Text_list_to_JSON(data)

# with open(file_name + '.json', 'w') as f:
#     f.write(json_text)
