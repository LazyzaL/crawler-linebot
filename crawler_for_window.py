import urllib.request as ur
import requests
import random
import os
import time
from bs4 import BeautifulSoup as soup
import translate


class view:
    def __init__(self, name):
        self.name = name
        self.url = ""

    def randombook(self):
        self.name = str(random.randint(1, 400000))

    def checkConnection(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        self.url = "https://nhentai.net/g/" + self.name + "/"
        resp = requests.get(self.url, headers)
        if resp.status_code == 200:
            return True
        else:
            print("\n查無此號碼：" + self.name)
            return False

    def setLink(self):
        while True:
            self.name = input("\n輸入神的語言（最多6位數，輸入-1產生隨機本子）：")
            if len(self.name) <= 6:
                break
            else:
                print("\n輸入格式錯誤")

        if self.name == "-1":
            while True:
                self.randombook()
                if self.checkConnection() == True:
                    break
                print("尋找下一本")

    def getInfo(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        req = ur.Request(self.url, headers=headers)
        html = soup(ur.urlopen(req).read().decode('utf-8'), "html.parser")

        cover = html.select('div#cover img')[0].get('data-src')
        main_title = html.find_all('span', 'before')[0].text + html.find_all(
            'span', 'pretty')[0].text + html.find_all('span', 'after')[0].text
        if (len(html.find_all('span', 'before')) > 1):
            sub_title = html.find_all('span', 'before')[1].text + html.find_all(
                'span', 'pretty')[1].text + html.find_all('span', 'after')[1].text
        else:
            sub_title = ''

        info = []

        for i in range(7):
            info.append(html.html.find_all('span', 'tags')
                        [i].find_all('span', 'name'))

        parodies = []
        characters = []
        tags = []
        artists = []
        languages = []
        catogories = []

        if(info[0]):
            for s in info[0]:
                parodies.append(s.text)
        if(info[1]):
            for s in info[1]:
                characters.append(s.text)
        if(info[2]):
            for s in info[2]:
                try:
                    tags.append(translate.tagsDict[s.text])
                except:
                    tags.append(s.text)
        if(info[3]):
            for s in info[3]:
                artists.append(s.text)
        if(info[5]):
            for s in info[5]:
                languages.append(s.text)
        if(info[6]):
            for s in info[6]:
                catogories.append(s.text)

        pages = html.find_all('span', 'tags')[7].find('span', 'name').text

        return [cover,
                main_title,
                sub_title,
                str(parodies).replace(
                    '[', '').replace(']', '').replace(', ', '\n').replace('\'', ''),
                str(characters).replace(
                    '[', '').replace(']', '').replace(', ', '\n').replace('\'', ''),
                str(tags).replace(
                    '[', '').replace(']', '').replace(', ', '\n').replace('\'', ''),
                str(artists).replace(
                    '[', '').replace(']', '').replace(', ', '\n').replace('\'', ''),
                str(languages).replace(
                    '[', '').replace(']', '').replace(', ', '\n').replace('\'', ''),
                str(catogories).replace(
                    '[', '').replace(']', '').replace(', ', '\n').replace('\'', ''),
                pages]
