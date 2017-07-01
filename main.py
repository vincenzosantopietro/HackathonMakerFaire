#!/usr/bin/env python
# -*- coding: utf-8 -*-


import webapp2
from values import *
from scraping.Scraper import *
from RegisterHandler import RegisterHandler
import logging


class MainHandler(webapp2.RequestHandler):

    def post(self):

        jsonobject = json.loads(self.request.body)

        speech = ""

        source = jsonobject['result']['source']
        keyboard = None
        logging.info(jsonobject['result']['metadata']['intentName'])

        if jsonobject['result']['metadata']['intentName'] == SORESA_NEWS_INTENT_NAME:

            scraper = Scraper()
            list_news = scraper.getNews()
            data = json.loads(list_news)

            speech = "Ecco le 5 ultime news pubblicate nella seziona News sul sito Soresa.it\n\n"
            # source = jsonobject['result']['source']

            for i in range(3):
                speech += data['result'][i]['date'] + ": " + data['result'][i]['text'] + " - link: " + data['result'][i]['link'] + "\n\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_WELCOME_INTENT_NAME:

            speech ="Ciao, sono E.L.S.A., il tuo assistente personale per il mondo So.Re.Sa.\n\nLa So.Re.Sa. S.p.A. – Società Regionale per la Sanità – è una società strumentale costituita dalla Regione Campania per la realizzazione di azioni strategiche finalizzate alla razionalizzazione della spesa sanitaria regionale. \n\nChe tipologia di utente pensi di essere?"
            source = jsonobject['result']['source']
            logging.info(jsonobject['originalRequest']['data']['message']['from']['username'])
            keyboard = dict(inline_keyboard=[
                [dict(text="Pubblica Amministrazione", url="https://soresaassinstant.appspot.com/register?type=pa&username={}".format(jsonobject['originalRequest']['data']['message']['from']['username']))],
                [dict(text="Privato", url="https://soresaassinstant.appspot.com/register?type=privato&username={}".format(jsonobject['originalRequest']['data']['message']['from']['username']))],
                [dict(text="ASL", url="https://soresaassinstant.appspot.com/register?type=asl&username={}".format(jsonobject['originalRequest']['data']['message']['from']['username']))],
                [dict(text="Impresa privata / libero professionista", url="https://soresaassinstant.appspot.com/register?type=impresa&username={}".format(jsonobject['originalRequest']['data']['message']['from']['username']))]
            ])

        elif jsonobject['result']['metadata']['intentName'] == SORESA_ORARISEGRETERIA_INTENT_NAME:

            speech="Ecco gli orari della segreteria:\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_BANDI_INTENT_NAME:
            speech = "Mmmh..controllo se puoi accedere ai contenuti\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_CONSIGLIOAMMINISTRAZIONE_INTENT_NAME:

            speech="Il consiglio di amministrazione di Soresa è composto da {} persone:\n\n".format(len(consiglio_amministrazione))
            for name in consiglio_amministrazione:
                speech += name + "\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_COLLEGIOSINDACALE_INTENT_NAME:

            speech= "Il collegio sindacale di Soresa è composto da {} persone:\n\n".format(len(collegio_sindacale))
            for name in collegio_sindacale:
                speech += name + "\n"


        elif jsonobject['result']['metadata']['intentName'] == SORESA_ORARISEGRETERIA_INTENT_NAME:

            scraper = Scraper()
            list_bandi = scraper.getBandi()
            data = json.loads(list_bandi)

            for i in range(len(data)):
                speech += data['result'][i]['date'] + ": " + data['result'][i]['text'] + " - link: " + data['result'][i]['link'] + "\n\n"


        else:

            speech = self.request.body

        # Generating output JSON

        if keyboard is None:
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
