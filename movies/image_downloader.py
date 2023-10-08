import requests
from string import ascii_letters
from random import choice


IMAGE_DIR_STATIC = 'static/img/posters'
IMAGE_DIR = 'img/posters'


def download_image_from_url(url_address: str, image_dir: str = '../', image_name: str = 'image') -> str:
    """
    Функция загружает картинку по url и сохраняет ее по адресу image_dir под именем image_name.
    По умолчанию сохраняет image.jpg в корень проекта.
    Если файл с таким именем уже есть, возвращает рандомное название.
    """
    # Убираем недопустимые и лишние символы в названии, а пробелы меняем на _:
    for j in '()[]{},.;:-+=_!?@#$%^&*/\\':
        if j in image_name:
            image_name = image_name.replace(j, '')
    if ' ' in image_name:
        image_name = image_name.replace(' ', '_')

    image = requests.get(url_address).content

    try:
        with open(f'{image_dir}/{image_name}.jpg', 'rb') as file:
            file.read()
        # Если файл уже существует и его вышло прочитать, меняем название на рандом
        image_name = ''.join([choice(ascii_letters) for _ in range(20)])

    except Exception as exc:
        print(exc)  # заменить на логер ошибок

    finally:
        with open(f'{image_dir}/{image_name}.jpg', 'wb+') as file:
            file.write(image)
    return image_name


"""
Пример использования для записи в базу Кино:

url = driver.find_element(By.CLASS_NAME, 'film-poster').get_attribute('src')
image_name = title # от найденного фильма

Для загрузки указываем путь без каталога static. 
За одно меняем название, чтобы не затереть файл с таким же именем:
image_name = download_image_from_url(url_address=url, image_dir=IMAGE_DIR, image_name=image_name)

В базу пишем путь со static:
poster = f'{IMAGE_DIR_STATIC}/{image_name}.jpg'
"""

