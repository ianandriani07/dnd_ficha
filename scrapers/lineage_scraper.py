import requests as rq
from bs4 import BeautifulSoup
import bs4
import adjacent_text as aj


def is_h1_parent_and_is_span(tag: bs4.Tag):
    return tag.name == 'span' and tag.parent.name == 'h1'


def is_p_and_em_child(tag: bs4.Tag):
    return tag.name == 'p' and tag.findChild('em') != -1


def either_way(tag: bs4.Tag):
    return is_p_and_em_child(tag) or is_h1_parent_and_is_span(tag)


# Pedir o site para o scraping relaciona a linhagens
link = input('Linhagem: ')
web_page_text = rq.get(link).text

# Separando o arquivo xml usando o bs4 para ficar fácil a procura e extração de texto
parsed = BeautifulSoup(web_page_text, features="html.parser")

data: list[aj.LinkedText] = []

last_header: int = -1

# Ignorar os dois primeiros elementos porque eles são lixo
for xml_element in parsed.find_all(either_way)[2:]:
    if xml_element.name == 'span':
        data.append(aj.LinkedText(xml_element.text))
        last_header += 1
    else:
        if xml_element.text.find('Source: ') == -1:
            data[last_header].description = xml_element.text

for i in data:
    print(i)
