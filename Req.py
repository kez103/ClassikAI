import requests as r
from bs4 import BeautifulSoup as bs

base = 'http://search.ruscorpora.ru/'
page = 'search.xml?env=alpha&mode=poetic&sort=gr_created_&text=meta&doc_author=%C0.%20%D1.%20%CF%F3%F8%EA%E8%ED&p=0'
poem_links = list()

url = base + page

resp = r.get(url)
# print(resp.text)


def next_page(html_text):   #  Ссылка на следующую страницу. Получает html страницы выбора поэмы. 

    soup = bs(html_text, features="html.parser")

    for link in soup.find_all('a'):
        if link.contents[0] == 'следующая страница':
            return link.get('href')


def get_poem_list(html_text):  #  Список ссылок на поэмы. Получает html страницы выбора поэмы

    soup = bs(html_text, features="html.parser")

    for link in soup.find_all('a'):
        link_get = link.get('href')
        if link_get is not None and link_get[0:6] == 'search':
                poem_links.append(link_get)
    return poem_links


def get_poem(html_text):  #  Печатает стих построчно. Принимает html страницы с поэмой

    soup = bs(html_text, features="html.parser")

    uls = soup.find_all('li')

    lis = [li for ul in uls for li in ul.findAll('li')]

    out_line = ''

    for poem_str in str(lis).split('<br/>'):
        soup_str = bs(poem_str, features="html.parser")
        for link in soup_str.find_all('span', {'class', 'b-wrd-expl'}):
            print(link.contents[0] + ' ', end = '')
        print('\n')


s = str(next_page(resp.text))
# print(s)
# parse(resp.text)               
# s = 'search.xml?env=alpha&mode=poetic&nodia=1&expand=full&docid=12313&sid=0'
url = base + s
resp = r.get(url)
# print(poem_links[0])

for poem_link in get_poem_list(resp.text):   

# s = str(poem_links[0])
    url = base + str(poem_link)
    resp = r.get(url)
    get_poem(resp.text)

# search.xml?env=alpha&mode=poetic&nodia=1&expand=full&docid=12313&sid=0
