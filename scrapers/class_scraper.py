from scrapper_base import Scrapper, Text_Type as tt
import requests as rq
from bs4 import Tag


def is_p_with_em_as_child(tag: Tag):  # Descrição da classe
    return tag.name == 'p' and not tag.findChild('em') is None


def is_p(tag: Tag):  # Descrições genericas
    return tag.name == 'p'


def is_table(tag: Tag):  # Tabelas genéricas
    return tag.name == 'table'


def is_h_something_with_toc(tag: Tag):
    return tag.name.find('h') != -1 and (not tag.attrs.get('id') is None and tag.attrs.get('id').find('toc') != -1)


def is_ul(tag: Tag):
    return tag.name == 'ul'


scrapper = Scrapper()

scrapper.add_identifier(is_p, is_h_something_with_toc)

link = input('Classe: ')
web_page_text = rq.get(link).text
# file_name = input('Nome do arquivo: ')


data = []

data = scrapper.parse_string(web_page_text, 0, True)
