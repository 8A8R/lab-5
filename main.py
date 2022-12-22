import requests
import json

import tkinter as tk
import aiohttp

from async_tkinter_loop import async_handler, async_mainloop
from io import BytesIO
from PIL import Image, ImageTk


# выполнение запроса
def getDataWebsite():
    url = 'https://cbr.ru/'
    answer = requests.get(url)
    print(answer.text)
    input("Нажмите 'enter' для продолжения.")


# getOpenWeatherMap() - получение данных о погоде
# city_name - город
def getOpenWeatherMap(city_name):
    API_key = 'a09feb70d4561b9f7966e1ba87f76241'
    answer = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}')
    answer = json.loads(answer.text)

    weather = answer['weather']
    humidity = answer['main']['humidity']
    pressure = answer['main']['pressure']

    print(
        f"В городе {city_name} погода {weather[0]['main']} ({weather[0]['description']}), влажность {humidity}, давление {pressure}")
    input("Нажмите 'enter' для продолжения.")


# Вывод данных по Api информацию с newsapi.org
def getDataWebsiteApi():
    API_key = 'ae00411e4e16458a9f1f7710756cce82'
    url = 'https://newsapi.org/'
    key_word = 'lion'
    answer = requests.get(f'{url}v2/everything?q={key_word}&from=2022-12-03&sortBy=popularity&apiKey={API_key}')
    answer = json.loads(answer.text)

    print(f"Всего найдено  {answer['totalResults']} статей по ключевому слову {key_word}")

    # проходим по статьям и выводим основную информацию
    for index, article in enumerate(answer['articles']):
        print(f"{index + 1}. Название статьи: {article['source']['name']}")
        print(f"Автор: {article['author']}")
        print(f"Описание: {article['description']}")
        print(f"Дата опубликования: {article['publishedAt']}")
        print(f"Ссылка на изображение: {article['urlToImage']}")
        print(f"Ссылка на статью: {article['url']}")


async def load_image(url):
    button.config(state=tk.DISABLED)
    label.config(text='Loading an image...')
    root.update()

    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status != 200:
            label.config(text=f'HTTP error {response.status}')
        else:
            content = await response.content.read()
            pil_image = Image.open(BytesIO(content))
            image = ImageTk.PhotoImage(pil_image)
            label.config(image=image, text='')
            label.image = image

    button.config(state=tk.NORMAL)


url = 'https://api.nasa.gov/planetary/apod?api_key=9Y3GDITYJi2aZBKEUF4f2VjEpnwkFSgm5Cutk8Sd'

answer = requests.get(url)
answer = json.loads(answer.text)
url_img = answer['url']

# создается Объект окна с кнопной для получения изображения
root = tk.Tk()
button = tk.Button(root, text='Загрузить изображение', command=async_handler(load_image, url_img))
button.pack()
label = tk.Label(root)
label.pack()

if __name__ == "__main__":
    # 1 пункт
    print("1 пункт) Вывод информации из запроса.")
    getDataWebsite()

    # 2 пункт
    print("2 пункт) Информация о погоде в городе.")
    city_name = input("Введите название города (на анг.): ")
    getOpenWeatherMap(city_name)

    # 3 пункт
    print("3 пункт) Вывод данных Api с сайта newsapi.org")
    getDataWebsiteApi()

    # Альтер. задание
    async_mainloop(root)