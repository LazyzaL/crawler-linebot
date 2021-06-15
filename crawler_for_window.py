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
        self.pages = 0

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

    def printInfo(self):
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
        self.pages = html.find_all('span', 'tags')[7].find('span', 'name').text

        print('\n號碼: #' + self.name)
        print('\nURL:\nhttps://nhentai.net/g/' + self.name + '/')
        print('\nCover Image URL:\n' + cover)
        print('\n' + main_title)
        if(sub_title):
            print('\n' + sub_title)
        if(info[0]):
            print('\nParodies:')
            for s in info[0]:
                print(s.text)
        if(info[1]):
            print('\nCharacters:')
            for s in info[1]:
                print(s.text)
        if(info[2]):
            print('\nTags:')
            for s in info[2]:
                try:
                    print(translate.tagsDict[s.text])
                except:
                    print(s.text)
        if(info[3]):
            print('\nArtists:')
            for s in info[3]:
                print(s.text)
        if(info[5]):
            print('\nLanguage:')
            for s in info[5]:
                print(s.text)
        if(info[6]):
            print('\nCatogories:')
            for s in info[6]:
                print(s.text)
        if(self.pages):
            print('\nPages:' + self.pages)

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
        self.pages = html.find_all('span', 'tags')[7].find('span', 'name').text

        return [cover, main_title, sub_title, info, self.pages]
