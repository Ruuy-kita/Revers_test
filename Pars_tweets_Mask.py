import re
import requests

from bs4 import BeautifulSoup
from constants import url_profile, proxy, headers


def get_x_guest_token():

    url = 'https://twitter.com/'

    with requests.Session() as sess:
        response = sess.get(url, proxies=proxy, headers=headers)
        x_guest_token = response.text.split('document.cookie="gt=')[1].split(';')[0]

    return x_guest_token


def get_authorization_token():

    url = 'https://abs.twimg.com/responsive-web/client-web-legacy/main.16bf340a.js'

    with requests.Session() as sess:
        response = sess.get(url, proxies=proxy, headers=headers)
        bearer_token = response.text.split('B=function(){return"')[1].split('"},')[0]

    return bearer_token


def get_parse_tweets(guest_token, authorization_token):

    """
    :param guest_token: гостевой токен в заголовок запроса
    :param authorization_token: токен авторизации в заголовок запроса
    :return: ничего не возвращает
    """

    header = {
        'Host': 'api.twitter.com',
        'Accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': authorization_token,
        'origin': 'https://twitter.com',
        'referer': 'https://twitter.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/122.0.0.0'
                      ' Safari/537.36',
        'x-guest-token': guest_token,
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'ru'
    }

    # Отправляем HTTP запрос к странице профиля с использованием прокси
    session = requests.Session()
    session.max_redirects = 60
    response = session.get(url_profile, proxies=proxy, headers=header)

    # Проверяем статус код ответа
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        str_soup = str(soup)
        pattern = r'"full_text":"(.*?)",'
        result = re.findall(pattern, str_soup)
        with open('tweets_Mask.txt', 'w', encoding='utf-8') as f:
            for x, itm in enumerate(result[:10]):
                tweet = f"{x + 1}: {itm}\n"
                print(tweet)
                f.write(tweet)
    else:
        print("Failed to fetch tweets. Status code:", response.status_code)


g_t = get_x_guest_token()  # получаем гостевой токен
a_t = get_authorization_token()  # получаем токен авторизации
get_parse_tweets(g_t, a_t)  # парсим твиты

