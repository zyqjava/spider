import json
import re
from urllib.parse import urlencode

import requests
from requests import RequestException
from bs4 import BeautifulSoup
import lxml

def get_page_index(offset, keyword):
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = "https://www.toutiao.com/api/search/content/?" + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("error")
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("error",url)
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    # title = soup.select('title')[2].get_text()
    images = re.compile('var gallery = (.*?);',re.S)
    result = re.search(images,html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            return {
                'image':images,
                'url': url
            }

def mian():
    html = get_page_index(0,'美女街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            reslut = parse_page_detail(html,url)

if __name__ == '__main__':
    mian()