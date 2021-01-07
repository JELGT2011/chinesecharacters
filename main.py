import requests
from bs4 import BeautifulSoup
import json
from lxml import html

base_url = 'http://chinese-characters.org/pinyin'
image_url_prefix = 'http://chinese-characters.org/images'

data = list()

def extract_data_from_character_url(character_url):
    datum = list()
    parsed_response = BeautifulSoup(requests.get(character_url).content)
    images = [tag for tag in parsed_response.find_all('img')]
    fonts = [tag for tag in parsed_response.find_all('font') if tag.get('size') == '+2']

    images = [tag for tag in parsed_response.find_all('img') if 'http://chinese-characters.org/images/' in tag.get('src')]
    simplified_image = [img for img in images if f'{image_url_prefix}/2simp/' in img['src']][0]
    traditional_image = [img for img in images if f'{image_url_prefix}/1trad/' in img['src']][0]
    ancient1_image = [img for img in images if f'{image_url_prefix}/1ancient/' in img['src']][0]
    ancient2_image = [img for img in images if f'{image_url_prefix}/2ancient/' in img['src']][0]
    archaic_images = [img for img in images if f'{image_url_prefix}/1archaic/' in img['src']]

    # variants
    # phonetic
    # semantic
    # apparent

    left_trs = [tr for tr in parsed_response.find_all('tr') if tr.get('align') == 'left']
    tr1 = left_trs[0]
    tr2 = left_trs[1]

    pronunciation = parsed_response.find_all('center')[-1].text.rstrip()
    definition = [tr for tr in parsed_response.find_all('tr') if tr.get('align') == 'left']
    mnemonic = parsed_response.find_all('')

    [tag for tag in parsed_response.find_all('td') if tag.get('align') == 'left']
    return datum


def main():
    parsed_response = BeautifulSoup(requests.get(base_url).content)
    letters_urls = [tag['href'] for tag in parsed_response.find_all('a') if 'pinyin' in tag['href']]
    for letter_url in letters_urls:
        parsed_response = BeautifulSoup(requests.get(letter_url).content)
        sounds_urls = [tag['href'] for tag in parsed_response.find_all('a') if 'pinyin' in tag['href']]
        for sound_url in sounds_urls:
            parsed_response = BeautifulSoup(requests.get(sound_url).content)
            characters_urls = [tag['href'] for tag in parsed_response.find_all('a') if 'meaning' in tag['href']]
            for character_url in characters_urls:
                data.append(extract_data_from_character_url(character_url))


if __name__ == '__main__':
    main()
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
