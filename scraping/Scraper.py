# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from google.appengine.api import urlfetch
# import requests
import json
import sys
import ssl
import urllib
import yaml
import re
from django.utils.encoding import smart_str

class Scraper:

    def __init__(self, url='https://www.soresa.it/'):
        self.base_url = url

    def getNews(self):

        # self.context = ssl._create_unverified_context()

        # page = urllib.urlopen(self.base_url + "Pagine/News.aspx", context=self.context).read()

        page = urlfetch.fetch(self.base_url + "Pagine/News.aspx", validate_certificate=True)

        # soup = BeautifulSoup(page, 'html.parser')
        soup = BeautifulSoup(page.content, 'html.parser')

        elements = soup.findAll(attrs={"class" : "newsItem"})

        list_news = []


        elements = elements[:-1]

        for el in elements:
            _news = {

                "date": '',
                "text": '',
                "link": ''

            }
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

        elem = elements.find(attrs={"class": "row pitchItem dark"})

        list_elem = elem.findAll(attrs={"class": "row pitchItem dark"})

        for el in list_elem:
            _convenzione = {
                "date": '',
                "text": '',
                "link": ''
            }
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

        # self.context = ssl._create_unverified_context()

        # page = urllib.urlopen(self.base_url + "area-imprese",  context=self.context).read()

        page = urlfetch.fetch(self.base_url + "area-imprese", validate_certificate=True)

        soup = BeautifulSoup(page.content, 'html.parser')

        elements = soup.find(attrs={"id" : "ctl00_ctl46_g_ac06dc6c_e4cd_48cb_a345_7433379f2a6d"})

        # print(elements)

        list_bandi = []



        row_pitchItem = elements.findAll(attrs={"class": "row pitchItem"} )
        row_pitchItem_dark = elements.findAll(attrs={"class": "row pitchItem dark"})

        for el in row_pitchItem:
            _bando = {
                "date": '',
                "text": '',
                "link": ''
            }
            text = el.find(attrs={"class": "show-read-more"}).string
            if text is None:
                continue
            # print (text)
            # if text is None:
            #     continue

            date = el.find(attrs={"class": "scadenza-bando"}).string
            link = el.find('a', href=True)
            link = self.base_url + link['href']

            _bando["date"] = re.sub('[\s\r\n]+Data', "Data", date)
            _bando["text"] = text
            _bando["link"] = link

            # print (_bando)
            # print ("***********************")
            list_bandi.append(_bando)

        for el in row_pitchItem_dark:

            _bando = {
                "date": '',
                "text": '',
                "link": ''
            }

            text = el.find(attrs={"class": "show-read-more"}).string
            if text is None:
                continue

            # print(text)
            date = el.find(attrs={"class": "scadenza-bando"}).string
            link = el.find('a', href=True)
            link = self.base_url + link['href']

            _bando["date"] = re.sub('[\s\r\n]+Data', "Data", date)
            _bando["text"] = text
            _bando["link"] = link


            list_bandi.append(_bando)

        # print ("***********************")



        return json.dumps( { "result": list_bandi }, indent=4, encoding='iso-8859-8').__str__()

    def get_dettaglio_bando(self, url):

        page = urlfetch.fetch(url, validate_certificate=True)

        # self.context = ssl._create_unverified_context()

        # page = urllib.urlopen(url,  context=self.context).read()

        soup = BeautifulSoup(page.content, 'html.parser')

        bando = {
            'dettaglio': {}
        }

        # Dettaglio bando
        parent_element = soup.find(attrs={"class": "form-horizontal"})
        for div in parent_element.findAll(attrs={"class": "form-group"}):

            title = div.find(attrs={"class": "control-label"})

            if title is None or title == 'Allegati':
                continue
            else:
                title = title.string

            text = div.find(attrs={"class": 'form-control-static'})

            if (title.startswith("Termine")):
                text = text.findAll('span')
                text = ''.join([d.string for d in text])
                bando['dettaglio'][title] = smart_str(text.encode('utf-8'))
            else:
                bando['dettaglio'][title] = smart_str(text.string.encode('utf-8')) if text.string is not None else ""

        # Altro
        keys = ['esiti', 'avvisi', 'chiarimenti']

        parent_element = soup.findAll(attrs={"class": "convenzioni"})
        for i, div in enumerate(parent_element):
            key = keys[i]
            bando[key] = []
            for j, tr in enumerate(div.findAll(attrs={"class": "contenuto"})):
                cols = tr.findAll(attrs={"class": 'form-control-static'})
                row = None
                if i < 2:
                    if len(cols) > 0:
                        row = {
                            'tipologia': smart_str(cols[0].string.encode('utf-8')),
                            'pub_date': smart_str(cols[1].string.encode('utf-8')) if len(cols) > 1 and cols[1].string is not None else "",
                            'desc': smart_str(cols[2].string.encode('utf-8')) if len(cols) > 2 and cols[2].string is not None else "",
                            'allegato': smart_str(cols[3].string.encode('utf-8')) if len(cols) > 3 and cols[3].string is not None else ""
                        }
                else:
                    if len(cols) > 0:
                        row = {
                            'protocollo': smart_str(cols[0].string.encode('utf-8')),
                            'domanda': smart_str(cols[1].string.encode('utf-8')) if len(cols) > 1 and cols[1].string is not None else "",
                            'risposta': smart_str(cols[2].string.encode('utf-8')) if len(cols) > 2 and cols[2].string is not None else "",
                            'allegato': smart_str(cols[3].string.encode('utf-8')) if len(cols) > 3 and cols[3].string is not None else ""
                        }
                bando[key].append(row)

        return bando



    def LavoraConNoi(self):

        # self.context = ssl._create_unverified_context()
        #
        page = urlfetch.fetch(self.base_url + "lavora-con-noi", validate_certificate=True)

        # page = urllib.urlopen(self.base_url + "lavora-con-noi", context=self.context).read()

        soup = BeautifulSoup(page.content, 'html.parser')

        # elements = soup.find_all(attrs={"class" : "AmmTrasp"})

        list_lavoro = []

        rows = soup.findAll('tr')[1:-1]

        for row in rows:
            _lavoro = {
                "text": '',
                "link": ''
            }
            text = row.find('p').string
            link = row.find('td')
            link = link.find(attrs={"class" : "AmmTrasp"})
            link = re.sub("[\s]", "+", link['href'])


            _lavoro['text'] = text
            _lavoro['link'] = link

            list_lavoro.append(_lavoro)


        return json.dumps( { "result": list_lavoro }, indent=4, encoding='iso-8859-8').__str__()



if __name__=='__main__':

    url = '/Users/davidenardone/PycharmProjects/HackathonMakerFaire/resources/news.json'

    _scraper = Scraper()

    # _list_news = _scraper.getNews()
    _list_bandi = _scraper.getBandi()
    # det = _scraper.get_dettaglio_bando("https://www.soresa.it/Pagine/BandoDettaglio.aspx?idDoc=213887&tipoDoc=BANDO_GARA_PORTALE")

    print (_list_bandi)





