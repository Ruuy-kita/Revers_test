import re

import requests
from bs4 import BeautifulSoup


def get_x_guest_token():
    x_guest_token = ''

    url = 'https://twitter.com/'

    # Прокси сервер
    proxy = {
        'https': 'http://mPWtUr:aQdDhw@134.195.155.38:9276'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    with requests.Session() as sess:
        response = sess.get(url, proxies=proxy, headers=headers)
        x_guest_token = response.text.split('document.cookie="gt=')[1].split(';')[0]

    return x_guest_token


def get_parse_tweets(x_guest_token):
    url = (
        "https://api.twitter.com/graphql/eS7LO5Jy3xgmd3dbL044EA/UserTweets?variables=%7B%22userId%22%3A%2244196397%22%2C%"
        "22count%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%2"
        "2withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_graphql_exclude_directive_en"
        "abled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enable"
        "d%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_u"
        "ser_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tw"
        "eetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graph"
        "ql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atru"
        "e%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_e"
        "nabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled"
        "%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_acti"
        "ons_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_rea"
        "d_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_en"
        "abled%22%3Afalse%7D")

    # Прокси сервер
    proxy = {
        'https': 'http://mPWtUr:aQdDhw@134.195.155.38:9276'
    }

    header = {
        'Host': 'api.twitter.com',
        'Accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'origin': 'https://twitter.com',
        'referer': 'https://twitter.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/122.0.0.0 Saf'
                      'ari/537.36',
        'x-guest-token': x_guest_token,
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'ru'
    }

    # Отправляем HTTP запрос к странице профиля с использованием прокси
    session = requests.Session()
    session.max_redirects = 60
    r = session.get(url, proxies=proxy, headers=header)
    response = requests.get(url, proxies=proxy, headers=header)

    # Проверяем статус код ответа
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        str_soup = str(soup)
        pattern = r'"full_text":"(.*?)",'
        result = re.findall(r'"full_text":"(.*?)",', str_soup)
        for x, itm in enumerate(result[:10]):
            print(f"{x + 1}: {itm}")
    else:
        print("Failed to fetch tweets. Status code:", response.status_code)


x_guest_token = get_x_guest_token()  # получаем токен
get_parse_tweets(x_guest_token) # парсим твиты

