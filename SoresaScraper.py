#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class SoresaNewsScraper:
    def __init__(self, url='https://www.soresa.it/notizie'):
        self.url = url

    def getNews(self):
        # .. get real news
        # test json
        return json.dumps({
            "result": [
                {
                    "date": "Martedì, 27 Giu 2017",
                    "title": "COMUNICAZIONE AI SENSI DELL'ART. 1 D.L. 50 DEL 24 APRILE 2017 - SPLIT PAYMENT SOCIETA' PARTECIPATE",
                    "url": "https://www.soresa.it/Pagine/NewsDettaglio.aspx?id=109"
                },
                {
                    "date": "Venerdì, 23 Giu 2017",
                    "title": "HACK NIGHT @ MUSEUM – MUSEO DI CAPODIMONTE, NAPOLI – 1-2 LUGLIO 2017",
                    "url": "https://www.soresa.it/Pagine/NewsDettaglio.aspx?id=108"
                },
                {
                    "date": "Lunedì, 12 Giu 2017",
                    "title": "AVVISO INTERRUZIONE ENERGIA ELETTRICA",
                    "url": "https://www.soresa.it/Pagine/NewsDettaglio.aspx?id=107"
                }
            ]
        })
