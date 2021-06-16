import urllib.request as ur
import requests
import random
from bs4 import BeautifulSoup as soup
import translate


class book:
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
            return False

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
                    tags.append(
                        translate.tagsDict[s.text] + '(' + s.text + ')')
                except:
                    tags.append(s.text)
        if(info[3]):
            for s in info[3]:
                artists.append(s.text)
        if(info[5]):
            for s in info[5]:
                try:
                    languages.append(translate.langDict[s.text])
                except:
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


class tag:
    def __init__(self, tag):
        self.tag = tag
        self.url = ""

    def checkConnection(self):
        self.tag = str(self.tag).replace(' ', '-')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        self.url = "https://nhentai.net/tag/" + self.tag + "/"
        resp = requests.get(self.url, headers)
        if resp.status_code == 200:
            return True
        else:
            return False

    def getInfo(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        req = ur.Request(self.url, headers=headers)
        html = soup(ur.urlopen(req).read().decode('utf-8'), "html.parser")

        urllist = []

        for url in html.find_all('a'):
            l = list(url.get('href'))
            if len(l) >= 3 and l[1] == 'g' and l[2] == '/':
                urllist.append('https://nhentai.net' + url.get('href'))

        i = 0
        for title in html.find_all('div', 'caption'):
            urllist.insert(i*2+1, title.text + '$%^&')
            i += 1

        return(', '.join(urllist).replace(', ', '\n').replace('$%^&', '\n'))


n = tag('paizuri')
n.checkConnection()
n.getInfo()
