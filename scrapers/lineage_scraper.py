import requests as rq
from bs4 import Tag
import scrapper_base as sb
from scrapper_base import Text
from text_type import Text_Type as tt
import text2json as tj
import json

# TODO: Tabelas não são consideradas


# A campanha de onde aquelas raças vieram ou subraças especificas para aquela campanha
def is_h1_or_h2_with_id_toc(tag: Tag):
    return (tag.name == 'h1' or tag.name == 'h2') and (not tag.attrs.get('id') is None and tag.attrs.get('id').find('toc') != -1)


def is_h1(tag: Tag):
    return tag.name == 'h1'


def is_h2(tag: Tag):
    return tag.name == 'h2'


# Descrição generica em itálico e negrito de subraças ou de raças de uma campanha especifica
def is_em_with_strong_parent(tag: Tag):
    return tag.name == 'em' and not tag.findParent('strong') is None


# Categorias normais e sua descrições
def is_li_without_an_a_if_not_with_strong_as_child(tag: Tag):
    return tag.name == 'li' and (tag.findChild('a') is None or not tag.findChild('strong') is None) and tag.findParent('li') is None


def is_li_without_li_as_parent(tag: Tag):
    return tag.name == 'li' and tag.findParent('li') is None


def is_strong(tag: Tag):  # Categorias
    return tag.name == 'strong'

# Tag a ser ignorada


def is_a(tag: Tag):
    return tag.name == 'a'


def is_li_with_strong_as_child(tag: Tag):
    return tag.name == 'li' and not tag.findChild('strong') is None


def is_li_with_li_as_parent(tag: Tag):
    return tag.name == 'li' and not tag.findParent('li') is None


def is_ul_with_li_as_parent(tag: Tag):
    return tag.name == 'ul' and not tag.findParent('li') is None


scrapper = sb.Scrapper()
scrapper.add_identifier(is_h1_or_h2_with_id_toc, is_em_with_strong_parent,
                        is_li_without_an_a_if_not_with_strong_as_child)
scrapper.add_to_hierarchy(0, is_h1, tt.CAMPAIGN, marker='<->')
scrapper.add_to_hierarchy(1, is_h2, tt.SUBRACE, marker='->')
scrapper.add_to_hierarchy(2, is_em_with_strong_parent,
                          tt.DESCRIPTION, marker='')
scrapper.add_to_hierarchy(2, is_strong, tt.CATEGORY, marker='•')
scrapper.single_text_category = tt.CATEGORY_DESCRIPTION
scrapper.TEXT_EXPECTED_DEPTH = 3
scrapper.add_to_hierarchy(4, is_li_with_li_as_parent,
                          tt.CATEGORY_EXPANSION, marker='-->')
scrapper.add_should_be_parsed(is_li_with_strong_as_child)
scrapper.add_should_be_parsed(is_ul_with_li_as_parent)
scrapper.add_should_treat_as_text(is_a)


# Pedir o site para o scraping relaciona a linhagens
link = input('Linhagem: ')
web_page_text = rq.get(link).text


data: list[Text] = []

data = scrapper.parse_string(web_page_text, 0)

d = tj.convert_Text_to_dict(data[0])
jsoned = json.dump(d)

with open('Fodase.txt', 'w') as f:
    f.write(jsoned)
