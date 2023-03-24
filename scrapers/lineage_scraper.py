import requests as rq
import bs4
import scrapper_base as sb
from scrapper_base import Text
from scrapper_base import Text_Type as tt

# TODO: Tabelas não são consideradas


def is_h1_parent_and_is_span(tag: bs4.Tag) -> bool:
    return tag.name == 'span' and tag.parent.name == 'h1'


def is_p_and_em_child(tag: bs4.Tag) -> bool:
    return tag.name == 'p' and tag.findChild('em')


def is_li_without_a_as_child(tag: bs4.Tag) -> bool:
    return tag.name == 'li' and (tag.findChild('a') is None or tag.findChild('strong'))


scrapper = sb.Scrapper()
scrapper.add_identifier(is_h1_parent_and_is_span,
                        is_p_and_em_child, is_li_without_a_as_child)

scrapper.add_to_hierarchy(0, is_h1_parent_and_is_span,
                          tt.MAIN_CATEGORY, marker='<->')
scrapper.add_to_hierarchy(1, is_li_without_a_as_child,
                          tt.DESCRIPTION, True, True, marker='->')
scrapper.add_to_hierarchy(1, is_p_and_em_child, tt.DESCRIPTION, marker='->')

# Pedir o site para o scraping relaciona a linhagens
link = input('Linhagem: ')
web_page_text = rq.get(link).text


data: list[Text] = []

data = scrapper.parse_string(web_page_text, 2)

for i in data:
    print(i)
