import requests
from bs4 import BeautifulSoup


def get_file_url(vk_url):
    if 'https://vk.com/' in vk_url:

        vk_url = vk_url[vk_url.rfind('z=') + 2:]
        vk_url = 'https://vk.com/{}?rev=1'.format(vk_url[:vk_url.find('%')])
        response = requests.get(vk_url)

        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find(class_='pv_photo_wrap')
            if div:
                src = div.find('img')['src']
                if 'https://' in src:
                    return src
    return 'Not photo'