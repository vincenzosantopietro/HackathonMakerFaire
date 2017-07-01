# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json
import sys
import ssl
import urllib
import yaml

class Scraper:

    def __init__(self, url='https://www.soresa.it/'):
        self.base_url = url
        # self.context = ssl._create_unverified_context()

    def getNews(self):


        # page = urllib.urlopen(self.base_url + "Pagine/News.aspx", context=self.context).read()

        page = requests.get(self.base_url + "Pagine/News.aspx", verify=False)

        # soup = BeautifulSoup(page, 'html.parser')
        soup = BeautifulSoup(page.content, 'html.parser')

        elements = soup.findAll(attrs={"class" : "newsItem"})

        list_news = []

        _news = {

            "date": '',
            "text": '',
            "link": ''

        }

        elements = elements[:-1]

        for el in elements:
            date = el.find(attrs={"class": "date"})
            text = el.find('a', href=True).string
            link = el.find('a', href=True)
            link = self.base_url + link['href']
            wk_day = date.find(attrs={"class": "wk-day"}).string
            day = date.find(attrs={"class": "day"}).string
            month = date.find(attrs={"class": "month"}).string
            year = date.find(attrs={"class": "year"}).string

            _news["date"] = wk_day + day + month + year
            _news["text"] = text
            _news["link"] = link
            #
            list_news.append(_news)

        return json.dumps( { "result": list_news }, indent=4, encoding='iso-8859-8').__str__()


def saveJson(url, data):

    with open(url, 'w') as f:
        json.dump(data,f)

def loadJson(url):

    with open(url) as data_file:
        data = json.load(data_file)

    return data

if __name__=='__main__':

    url = '/Users/davidenardone/PycharmProjects/HackathonMakerFaire/resources/news.json'

    _scraper = Scraper()

    _list_news = _scraper.getNews()
    saveJson(url,_list_news)




