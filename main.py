import requests
from bs4 import BeautifulSoup
import re

director_list = {}
cast_list = {}
genre_list = {}

class Movie:
    def __init__(self, name, director, cast) -> None:
        self.name = name
        self.director = director
        self.cast = cast

def clean_name(input_string):
    pattern = re.compile(r'\([^)]*\)')
    cleaned_string = pattern.sub('', input_string)
    return cleaned_string

def search_by_cast(name, objects):
    result = []
    for movie_object in objects:
        if name in movie_object.cast:
            result.append(movie_object.name)
        if len(result) >= cast_list[name]:
            break
    return result

def search_by_director(name, objects):
    result = []
    for movie_object in objects:
        if name in movie_object.director:
            result.append(movie_object.name)
        if len(result) >= director_list[name]:
            break
    return result

try:
    year = int(input("Enter The Year : "))
except:
    print("invalid Input")

url = f"https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_{year}"
responce = requests.get(url)
if responce.status_code != 200:
    print("Films Are Not Available right now. Try Again later or with a different year.")
    exit()

html_content = responce.text
soup =BeautifulSoup(html_content, 'lxml')
table = soup.find('table', class_='wikitable')
t_rows = table.find_all('tr')
t_rows.pop(0)
movies = []
for row in t_rows:
    t_datas = row.find_all('td')
    while True:
        if 'rowspan' in t_datas[0].attrs or ('style' in t_datas[0].attrs and t_datas[0]['style']!='text-align:center;'):
            t_datas.pop(0)
        else:
            break
    movie_name = t_datas[0].text
    movie_name = movie_name.replace("\n", "")
    movie_name = clean_name(movie_name)
    movie_name = movie_name.strip()

    director_string = t_datas[1].text
    directors = director_string.split(",")
    for i in range(len(directors)):
        directors[i] = clean_name(directors[i])
        directors[i] = directors[i].strip()
        if directors[i] in director_list:
            director_list[directors[i]] += 1
        else:
            director_list[directors[i]] = 1

    cast_string = t_datas[2].text
    casts = cast_string.split(",")
    for i in range(len(casts)):
        casts[i] = clean_name(casts[i])
        casts[i] = casts[i].strip()
        if casts[i] in cast_list:
            cast_list[casts[i]] += 1
        else:
            cast_list[casts[i]] = 1

    movie_object = Movie(movie_name, directors, casts)

    movies.append(movie_object)


for movie in movies:
    print(movie.name)

# print("1. Search By Cast\n2.Search By Director\n")
# option = input("Enter Option : ")
# if option == '1':
#     print(cast_list)
#     cast_name = input("Enter Cast Name : ")
#     out = search_by_cast(cast_name, movies)
# elif option == '2':
#     print(director_list)
#     director_name = input("Enter Director Name : ")
#     out = search_by_director(director_name, movies)
# else:
#     print("Thank You For Using")
#     exit()
# print(out)