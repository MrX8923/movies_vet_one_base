import requests
from string import ascii_letters
from random import choice


IMAGE_DIR_STATIC = 'img/posters'
IMAGE_DIR = 'movies/static/img/posters'
PORTRAIT_DIR_STATIC = 'img/portraits'
PORTRAIT_DIR = 'movies/static/img/portraits'


class ImageWithThisNameExists(Exception):
    def __str__(self):
        return f'Изображение с таким именем уже существует!'


def download_image_from_url(url_address: str, image_dir: str = '../', image_name: str = 'image') -> str:
    """
    Функция загружает картинку по url и сохраняет ее по адресу image_dir под именем image_name.
    По умолчанию сохраняет image.jpg в корень проекта.
    Если файл с таким именем уже есть, возвращает рандомное название.
    """

    if not url_address:
        print('Не вышло скачать')
        return image_name

    # Убираем недопустимые и лишние символы в названии, а пробелы меняем на _:
    for j in '()[]{},.;:-+=!?@#$%^&*/\\':
        if j in image_name:
            image_name = image_name.replace(j, '')
    if ' ' in image_name:
        image_name = image_name.replace(' ', '_')

    image = requests.get(url_address).content

    try:
        with open(f'{image_dir}/{image_name}.jpg', 'rb+') as file:
            file.read()
        # Если файл уже существует и его вышло прочитать, вызываем исключение
        raise ImageWithThisNameExists()

    except ImageWithThisNameExists as exc:
        image_name = ''.join([choice(ascii_letters) for _ in range(20)])
        print(f'Ошибка: {exc} Запишем под новым: {image_name}.jpg')  # заменить на логер ошибок

    except FileNotFoundError:
        print(f'Нет файла "{image_name}.jpg", создаем новый!')  # заменить на логер ошибок

    finally:
        with open(f'{image_dir}/{image_name}.jpg', 'wb') as file:
            file.write(image)
        return image_name


"""
Пример использования для записи в базу Кино:

Проще всего бросить в каталог приложения:
from .image_downloader import *

url = driver.find_element(By.CLASS_NAME, 'film-poster').get_attribute('src')
image_name = title # от найденного фильма

Для загрузки указываем путь без каталога static IMAGE_DIR. 
За одно меняем название, чтобы не затереть файл с таким же именем:
image_name = download_image_from_url(url_address=url, image_dir=IMAGE_DIR_STATIC, image_name=image_name)

В базу пишем путь со static:
poster = f'{IMAGE_DIR_STATIC}/{image_name}.jpg'
"""
