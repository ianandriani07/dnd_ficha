import requests as rq
from bs4 import BeautifulSoup
import bs4
import adjacent_text as aj

# TODO: Tabelas não são consideradas


def is_h1_parent_and_is_span(tag: bs4.Tag):
    return tag.name == 'span' and tag.parent.name == 'h1'


def is_p_and_em_child(tag: bs4.Tag):
    return tag.name == 'p' and tag.findChild('em')


def is_li_without_a_as_child(tag: bs4.Tag):
    return tag.name == 'li' and (tag.findChild('a') is None or tag.findChild('strong'))


def all_of_them(tag: bs4.Tag):
    return is_p_and_em_child(tag) or is_h1_parent_and_is_span(tag) or is_li_without_a_as_child(tag)


def exclude_tag_from_text(tag: bs4.Tag, to_be_excluded: str) -> str:
    text = ''
    for tg in tag.contents:
        if tg.name != to_be_excluded:
            text += tg.text
    return text


# Pedir o site para o scraping relaciona a linhagens
link = input('Linhagem: ')
web_page_text = rq.get(link).text

# Separando o arquivo xml usando o bs4 para ficar fácil a procura e extração de texto
parsed = BeautifulSoup(web_page_text, features="html.parser")

data: list[aj.LinkedText] = []

last_header: int = -1

# print(parsed.find_all(all_of_them)[2:])

# Ignorar os dois primeiros elementos porque eles são lixo
for xml_element in parsed.find_all(all_of_them)[2:]:

    cleaned_text: str = xml_element.text.replace('\n', '')

    # xml_element: bs4.Tag = bs4.Tag()
    if xml_element.name == 'span':
        data.append(aj.LinkedText(cleaned_text))
        last_header += 1
    elif xml_element.name == 'li':
        # Pegar o nome da categoria que está em negrito e sempre termina em ponto
        category = cleaned_text[:cleaned_text.find('.')]

        # Checar se há um ul como filho do elemento
        # Se houver, adicione o filho ao pai como um subtexto
        if not xml_element.findChild('ul') is None:
            desc = exclude_tag_from_text(xml_element, 'ul').replace('\n', '')
            desc = desc[desc.find('.') + 1:]
            data[last_header].subcategories[category] = aj.Text(desc)

            child_elements = xml_element.findChildren('li')

            for el in child_elements:
                data[last_header].subcategories[category].sub_text.append(
                    el.text)
            continue

        desc = cleaned_text[cleaned_text.find('.') + 1:]
        data[last_header].subcategories[category] = aj.Text(desc)
    else:
        if cleaned_text.find('Source: ') == -1:
            data[last_header].description += (
                '\n' if data[last_header].description else '') + '      ' + cleaned_text

for i in data:
    print(i)
