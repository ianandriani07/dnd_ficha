import requests as rq
from bs4 import BeautifulSoup


link = input('Linhagem:')
web_page_text = rq.get(link).text
