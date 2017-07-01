# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from google.appengine.api import urlfetch
# import requests
import json
import sys
import ssl
import urllib
import yaml

class Scraper:

    def __init__(self, url='https://www.soresa.it/'):
        self.base_url = url

    def getNews(self):

        # page = urllib.urlopen(self.base_url + "Pagine/News.aspx", context=self.context).read()

        page = urlfetch.fetch(self.base_url + "Pagine/News.aspx", validate_certificate=True)

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

            list_news.append(_news)

        return json.dumps( { "result": list_news }, indent=4, encoding='iso-8859-8').__str__()


    def getConvenzioni(self):

        # self.context = ssl._create_unverified_context()

        page = urlfetch.fetch(self.base_url + "area-pa", validate_certificate=True)

        # page = urllib.urlopen(self.base_url + "area-pa", context=self.context).read()

        soup = BeautifulSoup(page.content, 'html.parser')

        elements = soup.find(attrs={"class" : "convenzioni"})

        list_convenzioni = []

        _convenzione = {
            "date": '',
            "text": '',
            "link": ''
        }

        elem = elements.find(attrs={"class": "row pitchItem dark"})

        list_elem = elem.findAll(attrs={"class": "row pitchItem dark"})

        for el in list_elem:
            date = el.find(attrs={"class": "scadenza-bando"})
            text = el.find(attrs={"class": "col-lg-10 col-md-10 col-sm-12 col-xs-12 description"}).find('p').string
            day = date.find(attrs={"class": "day"}).string
            month = date.find(attrs={"class": "month"}).string
            year = date.find(attrs={"class": "year"}).string
            link = el.find('a', href=True)
            link = self.base_url + link['href']

            _convenzione["date"] = day + month + year
            _convenzione["text"] = text
            _convenzione["link"] = link

            list_convenzioni.append(_convenzione)

        return json.dumps( { "result": list_convenzioni }, indent=4, encoding='iso-8859-8').__str__()


    def getBandi(self):

        self.context = ssl._create_unverified_context()

        # page = urlfetch.fetch(self.base_url + "area-pa", validate_certificate=True)

        page = urlfetch.fetch(self.base_url + "area-imprese", validate_certificate=True)

        soup = BeautifulSoup(page.content, 'html.parser')

        elements = soup.find(attrs={"id" : "ctl00_ctl46_g_ac06dc6c_e4cd_48cb_a345_7433379f2a6d"})

        # print(elements)

        list_bandi = []

        _bando = {
            "date": '',
            "text": '',
            "link": ''
        }


        row_pitchItem = elements.findAll(attrs={"class": "row pitchItem"} )
        row_pitchItem_dark = elements.findAll(attrs={"class": "row pitchItem dark"})

        for el in row_pitchItem:
            text = el.find(attrs={"class": "show-read-more"}).string
            date = el.find(attrs={"class": "scadenza-bando"}).string
            link = el.find('a', href=True)
            link = self.base_url + link['href']

            _bando["date"] = date
            _bando["text"] = text
            _bando["link"] = link

            list_bandi.append(_bando)

        for el in row_pitchItem_dark:
            text = el.find(attrs={"class": "show-read-more"}).string
            date = el.find(attrs={"class": "scadenza-bando"}).string
            link = el.find('a', href=True)
            link = self.base_url + link['href']

            _bando["date"] = date
            _bando["text"] = text
            _bando["link"] = link

            list_bandi.append(_bando)


        return json.dumps( { "result": list_bandi }, indent=4, encoding='iso-8859-8').__str__()


# def saveJson(url, data):
#
#     with open(url, 'w') as f:
#         json.dump(data,f)
#
# def loadJson(url):
#
#     with open(url) as data_file:
#         data = json.load(data_file)
#
#     return data

if __name__=='__main__':

    url = '/Users/davidenardone/PycharmProjects/HackathonMakerFaire/resources/news.json'

    _scraper = Scraper()

    # _list_news = _scraper.getNews()
    # _list_news = _scraper.getConvenzioni()
    _list_bandi = _scraper.getBandi()

    print (_list_bandi)





