import requests as r
from json import JSONEncoder
from bs4 import BeautifulSoup as bs

base = 'http://search.ruscorpora.ru/'

# page = 'search.xml?env=alpha&mode=poetic&sort=gr_created_&text=meta&doc_author=%C0.%20%D1.%20%CF%F3%F8%EA%E8%ED&p=0'
authors_names = {'pushkin':'Пушкин',
           'esenin': 'Есенин', 
           'mayakovskij': 'Маяковский', 
           'blok': 'Блок', 
           'tyutchev': 'Тютчев'}

authors_links = {'pushkin':'search.xml?env=alpha&mode=poetic&sort=gr_created_&text=meta&doc_author=%C0.%20%D1.%20%CF%F3%F8%EA%E8%ED&p=0',
         'esenin': 'search.xml?env=alpha&mode=poetic&sort=gr_created_&text=meta&doc_author=%d1.%20%c0.%20%c5%f1%e5%ed%e8%ed',
         'mayakovskij': 'search.xml?env=alpha&mode=poetic&sort=gr_created_&text=meta&doc_author=%c2.%20%c2.%20%cc%e0%ff%ea%ee%e2%f1%ea%e8%e9',
         'blok': 'search.xml?env=alpha&mode=poetic&sort=gr_created_&text=meta&doc_author=%c0.%20%c0.%20%c1%eb%ee%ea',
         'tyutchev': 'search.xml?env=alpha&mode=poetic&sort=gr_created_&text=meta&doc_author=%d4.%20%c8.%20%d2%fe%f2%f7%e5%e2'}


# print(resp.text)


def next_page(html_text):   #  Ссылка на следующую страницу. Получает html страницы выбора поэмы. 

    soup = bs(html_text, features="html.parser")

    for link in soup.find_all('a'):
        if link.contents[0] == 'следующая страница':
            return str(link.get('href'))


def get_poem_list(html_text):  #  Генератор ссылок на поэмы. Получает html страницы выбора поэмы

    soup = bs(html_text, features="html.parser")

    for link in soup.find_all('a'):

        link_get = link.get('href')

        if link_get is not None and link_get[0:6] == 'search':
                yield str(link_get)


def get_poem(html_text):  #  Печатает стих построчно. Принимает html страницы с поэмой
    
    poem_dict = {"content": ""}
    soup = bs(html_text, features="html.parser")
    uls = soup.find_all('li')
    lis = [li for ul in uls for li in ul.findAll('li')]

    for poem_str in str(lis).split('<br/>'):
  
        soup_str = bs(poem_str, features="html.parser")
  
        for link in soup_str.find_all('span', {'class', 'b-wrd-expl'}):

            poem_dict["content"] += str(link.contents[0]) + ' '

        poem_dict["content"] += '\n'

    return poem_dict


def get_title(html_text, auth_name):

    title_dict = {"title": ""}
    soup = bs(html_text, features="html.parser")

    for link in soup.find_all('span', {'class', 'snippet-title'}):

        title_span = str(link.contents[0])
        authind = title_span.find(auth_name)
        year = title_span.find(' (1')
        title_dict["title"] += title_span[authind + len(auth_name) + 2:year]

    return title_dict


def get_jsdict():

    jslist = []
    dict_2_js = {}

    poet_id_dict = {"poet_id": ""}

    for nick in authors_links.keys():

        poet_id_dict["poet_id"] = nick
        url = base + authors_links[nick]
        resp = r.get(url)
    
        for poem_link in get_poem_list(resp.text):   

            url = base + poem_link
            resp = r.get(url)
            # print(get_title(resp.text, authors_names[nick]))
            dict_2_js.update(poet_id_dict)
            dict_2_js.update(get_title(resp.text, authors_names[nick]))
            dict_2_js.update(get_poem(resp.text))
            jslist.append(dict_2_js)
            dict_2_js = {}
            # break
    return jslist

# js = JSONEncoder()
# print(js.encode(get_jsdict()))
print(get_jsdict())
# parse(resp.text)               
# s = 'search.xml?env=alpha&mode=poetic&nodia=1&expand=full&docid=12313&sid=0'

# search.xml?env=alpha&mode=poetic&nodia=1&expand=full&docid=12313&sid=0
#
#

