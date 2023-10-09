import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from .models import *
from .image_downloader import *

TIME_PAUSE = 2
MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


def driver_prepare():
    print('*Запускаем браузер FireFox в фоновом режиме.')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print('*Браузер открыт в фоновом режиме.')
    return driver


def add_to_db(data):
    try:
        country = Country.objects.get(name=data['country'])
    except:
        country = Country.objects.create(name=data['country'])
    try:
        director = Director.objects.get(**data['director'])
    except:
        director = Director.objects.create(**data['director'])
    try:
        age_rating = AgeRating.objects.get(rate=data['ager'])
    except:
        age_rating = AgeRating.objects.create(rate=data['ager'])
    try:
        genre = Genre.objects.get(name=data['genre'])
    except:
        genre = Genre.objects.create(name=data['genre'])
    movie = Movie.objects.create(title=data['title'],
                                 genre=genre,
                                 rating=data['rating'],
                                 country=country,
                                 director=director,
                                 summary=data['summary'],
                                 year=data['year'],
                                 age_rating=age_rating,
                                 subscription=Subscription.objects.get(id=choice([1, 2, 3])),
                                 poster=data['poster'])
    for actor in data['actors']:
        try:
            act = Actor.objects.get(firstname=actor['firstname'], lastname=actor['lastname'])
        except:
            act = Actor.objects.create(**actor)
        movie.actors.add(act)
        movie.save()


def is_in_db(title, year):
    print('Фильм', f'"{title}" ({year})')
    if Movie.objects.filter(title=title, year=year):
        print('Фильм есть в базе')
        return True
    else:
        print('Фильма нет в базе')
        return False


def get_movies():
    driver = driver_prepare()
    print('Ищем фильмы...')
    try:
        for i in range(1, 2):
            driver.get('https://www.kinopoisk.ru/lists/movies/top250/?page=' + str(i))
            time.sleep(5)
            for n in range(0, 30):
                movies = driver.find_elements(By.CLASS_NAME, 'styles_root__ti07r')
                m = movies[n]
                movie_title = m.find_element(By.CLASS_NAME, 'styles_mainTitle__IFQyZ')
                title = movie_title.text
                year = m.find_element(By.CLASS_NAME, 'desktop-list-main-info_secondaryText__M_aus').text.split(', ')
                if len(year) == 2:
                    year = int(year[0])
                else:
                    year = int(year[1])
                if not is_in_db(title, year):
                    info = m.find_element(By.CLASS_NAME, 'desktop-list-main-info_truncatedText__IMQRP').text.split(
                        ' • ')
                    country = info[0]
                    genre = info[1].split('  ')[0]
                    director = {'firstname': info[1].split(': ')[1].split(' ')[0],
                                'lastname': info[1].split(': ')[1].split(' ')[1]}
                    rating = m.find_element(By.CLASS_NAME, 'styles_kinopoiskValueBlock__qhRaI').text
                    print(f'Первичные данные: {country}, {genre}, {director}, {rating}')

                    # переход на страницу фильма
                    movie_title.click()
                    time.sleep(TIME_PAUSE)
                    summary = driver.find_element(By.CLASS_NAME, 'styles_synopsisSection__nJoAj').text
                    ager_all = driver.find_elements(By.CLASS_NAME, 'styles_rootHighContrast__Bevle')
                    if len(ager_all) > 1:
                        ager = ager_all[1].text
                    else:
                        ager = ager_all[0].text
                    url = driver.find_element(By.CLASS_NAME, 'film-poster').get_attribute('src')
                    image_name = title
                    image_name = download_image_from_url(url, IMAGE_DIR, image_name)
                    poster = f'{IMAGE_DIR_STATIC}/{image_name}.jpg'
                    print('Получил остальные данные и постер')

                    # поиск актёров
                    actors = []
                    i = 0
                    while True:
                        actor_li = driver.find_elements(By.CLASS_NAME, 'styles_list___ufg4')[0].find_elements(
                            By.TAG_NAME, 'li')
                        actor_li[i].find_element(By.TAG_NAME, 'a').click()
                        time.sleep(TIME_PAUSE)
                        name = driver.find_element(By.CLASS_NAME, 'styles_primaryName__2Zu1T').text
                        try:
                            actor_firstname = name[0:name.index(' ')]
                            actor_lastname = name[name.index(' ') + 1:]
                        except:
                            actor_firstname = name
                            actor_lastname = ''
                        info = driver.find_elements(By.CLASS_NAME, 'styles_rowDark__ucbcz')
                        actor_country = ''
                        actor_born = ''
                        for info_string in info:
                            if info_string.text.split('\n')[0] == 'Дата рождения' \
                                    and info_string.text.split('\n')[1] != '—':
                                try:
                                    born_date = info_string.text.split(' • ')[0].split('\n')[1]
                                    born_year = int(born_date.split(', ')[-1])
                                    born_month = int(MONTHS.index(born_date.split(', ')[0].split()[1]) + 1)
                                    born_day = int(born_date.split()[0])
                                    actor_born = datetime.date(born_year, born_month, born_day)
                                except:
                                    pass
                            if info_string.text.split('\n')[0] == 'Место рождения' \
                                    and info_string.text.split('\n')[1] != '—':
                                actor_country = info_string.text.split('\n')[1].split(', ')[-1]
                        actor = {'firstname': actor_firstname, 'lastname': actor_lastname}
                        try:
                            url = driver.find_element(By.CLASS_NAME, 'image').get_attribute('src')
                        except:
                            url = ''
                        portrait_name = f'{actor_firstname}_{actor_lastname}'
                        portrait_name = download_image_from_url(url, PORTRAIT_DIR, portrait_name)
                        if actor_country:
                            actor.update({'country': actor_country})
                        if actor_born:
                            actor.update({'birthday': actor_born})
                        if url:
                            actor.update({'portrait': f'{PORTRAIT_DIR_STATIC}/{portrait_name}.jpg'})
                        print('Актёр: ', actor)
                        actors.append(actor)
                        driver.back()
                        time.sleep(TIME_PAUSE)
                        i += 1
                        if i >= len(actor_li):
                            break

                    driver.back()
                    movie = {'title': title,
                             'year': year,
                             'country': country,
                             'genre': genre,
                             'director': director,
                             'rating': rating,
                             'summary': summary,
                             'ager': ager,
                             'poster': poster,
                             'actors': actors}
                    add_to_db(movie)
                    print(f'Добавил "{title}" в базу')
    except Exception as e:
        print(e)
    driver.close()
