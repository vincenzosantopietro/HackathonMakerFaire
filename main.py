#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import json
from values import *
from SoresaScraper import SoresaNewsScraper
from RegisterHandler import RegisterHandler
import logging

class MainHandler(webapp2.RequestHandler):

    def post(self):
        jsonobject = json.loads(self.request.body)

        speech = ""
        source = ""
        keyboard = None
        logging.info(jsonobject['result']['metadata']['intentName'])

        if jsonobject['result']['metadata']['intentName'] == SORESA_NEWS_INTENT_NAME:
            newsScraper = SoresaNewsScraper()
            news_json = json.loads(newsScraper.getNews())

            speech = "Ecco gli ultimi 3 articoli pubblicati sul sito soresa.it\n\n"
            source = jsonobject['result']['source']

            for i in range(3):
                speech += news_json['result'][i]['date'] + ": " + news_json['result'][i]['title'] + " - link: " + news_json['result'][i]['url'] + "\n\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_WELCOME_INTENT_NAME:

            speech ="Ciao, sono E.L.S.A., il tuo assistente personale per il mondo So.Re.Sa.\n\nLa So.Re.Sa. S.p.A. – Società Regionale per la Sanità – è una società strumentale costituita dalla Regione Campania per la realizzazione di azioni strategiche finalizzate alla razionalizzazione della spesa sanitaria regionale. \n\nChe tipologia di utente pensi di essere?"
            source = jsonobject['result']['source']
            keyboard = dict(inline_keyboard=[
                [dict(text="Pubblica Amministrazione", url="https://soresaassistant.appspot.com/register?type=pa&username=".format(jsonobject['originalRequest']['data']['message']['username']))],
                [dict(text="Privato", url="https://soresaassistant.appspot.com/register?type=privato&username=".format(jsonobject['originalRequest']['data']['message']['username']))],
                [dict(text="ASL", url="https://soresaassistant.appspot.com/register?type=asl&username=".format(jsonobject['originalRequest']['data']['message']['username']))],
                [dict(text="Impresa privata / libero professionista", url="https://soresaassistant.appspot.com/register?type=impresa&username=".format(jsonobject['originalRequest']['data']['message']['username']))]
            ])

        #else:

        #    speech = self.request.body
        #    source = jsonobject['result']['source']
        if(keyboard is None):
            self.response.headers['Content-Type'] = 'application/json'

            out_json = json.dumps({
                    "speech":speech,
                    "displayText":speech,
                    "source":source
                },indent=4)

            self.response.write(out_json)
        else:
            self.response.headers['Content-Type'] = 'application/json'

            out_json = json.dumps({
                "speech": speech,
                "displayText": speech,
                "source": source,
                "data": {
                    "telegram": {
                      "chat_id": jsonobject['id'],
                      "text" : speech,
                      "reply_markup": keyboard
                    }
                }
            }, indent=4)

            self.response.write(out_json)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterHandler)
], debug=True)
