#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import base64
from user.model import *
from scraping.Scraper import *
import json
from Crypto.Hash import MD5

from google.appengine.api import urlfetch
from values import BOT_TOKEN
import urllib
from user.handlers import *
from datetime import datetime

from datetime import timedelta
from django.utils.encoding import smart_str


class BandiGaraHandler(webapp2.RequestHandler):

    def get(self):
        # seleziona un bando da tracciare
        link = base64.b64decode(self.request.get('link'))
        bandi = BandiWatcherModel()
        bandi.username = self.request.get('username')
        bandi.link = link

        # Page scraping
        scraper = Scraper()
        dettaglio_bando = scraper.get_dettaglio_bando(link)

        bandi.last_edits = json.dumps(dettaglio_bando)
        bandi.put()

        pass


class CronHandler(webapp2.RequestHandler):

    def get(self):

        scraper = Scraper()
        h = MD5.new()

        bandi = BandiWatcherModel.query().fetch()
        if len(bandi) > 0:
            for bando in bandi:
                dettaglio_bando = scraper.get_dettaglio_bando(bando.link)
                j_bando = json.dumps(dettaglio_bando)
                logging.info("bando")
                logging.info(bando.last_edits)
                h.update(j_bando)
                new = h.hexdigest()
                h.update(bando.last_edits)
                old = h.hexdigest()

                # datetime_object = datetime.strptime(, '%b %d %Y %I:%M%p')
                bando_last_edits = json.loads(bando.last_edits)
                date = datetime.strptime(smart_str(bando_last_edits['dettaglio']['Termine Presentazione Offerte/Domande Di Partecipazione']), "%a, %d %b %Y %H: %M").date()

                if new != old:
                    user = get_user(bando.username)
                    urlfetch.fetch("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage",
                                   payload=urllib.urlencode({"chat_id": user.chat_id, "text": 'Il bando e\' stato aggiornato: \n' + bando.link}),
                                   method=urlfetch.POST)
                    bando.last_edits = j_bando
                    bando.put()
                if date - datetime.now().date() < 3:

                    user = get_user(bando.username)
                    urlfetch.fetch("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage",
                                   payload=urllib.urlencode({"chat_id": user.chat_id,
                                                             "text": 'Mancano 3 giorni alla scadenza del bando \n' + bando.link}),
                                   method=urlfetch.POST)
                    bando.last_edits = j_bando
                    bando.put()


