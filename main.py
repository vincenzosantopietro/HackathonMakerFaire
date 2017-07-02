#!/usr/bin/env python
# -*- coding: utf-8 -*-


import webapp2
from values import *
from scraping.Scraper import *
from RegisterHandler import RegisterHandler
import logging
import utils
from user.handlers import *
import re
import base64
from watchers import *
from google.appengine.api import urlfetch
import urllib


class MainHandler(webapp2.RequestHandler):

    def get(self):
        url = 'http://www.soresa.it/Pagine/BandoDettaglio.aspx?idDoc=142728&tipoDoc=BANDO_GARA_PORTALE'
        _scraper = Scraper()
        bando = _scraper.get_dettaglio_bando(url)
        logging.info(bando)


    def post(self):

        jsonobject = json.loads(self.request.body)
        out_json = None

        speech = ""

        source = jsonobject['result']['source']
        keyboard = None
        location = None
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
            chat_id = jsonobject['originalRequest']['data']['message']['chat']['id']
            username = jsonobject['originalRequest']['data']['message']['from']['username']
            keyboard = dict(inline_keyboard=[
                [dict(text="Pubblica Amministrazione", url="https://elsa-proj.appspot.com/register?type=pa&username={0}&id={1}".format(username, chat_id))],
                [dict(text="Privato", url="https://elsa-proj.appspot.com/register?type=privato&username={0}&id={1}".format(username, chat_id))],
                [dict(text="ASL", url="https://elsa-proj.appspot.com/register?type=asl&username={0}&id={1}".format(username, chat_id))],
                [dict(text="Impresa privata / libero professionista", url="https://elsa-proj.appspot.com/register?type=impresa&username={0}&id={1}".format(username, chat_id))]
            ])

        elif jsonobject['result']['metadata']['intentName'] == SORESA_CONSIGLIOAMMINISTRAZIONE_INTENT_NAME:

            speech="Il consiglio di amministrazione di Soresa è composto da {} persone:\n\n".format(len(consiglio_amministrazione))
            for name in consiglio_amministrazione:
                speech += name + "\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_COLLEGIOSINDACALE_INTENT_NAME:

            speech= "Il collegio sindacale di Soresa è composto da {} persone:\n\n".format(len(collegio_sindacale))
            for name in collegio_sindacale:
                speech += name + "\n"


        elif jsonobject['result']['metadata']['intentName'] == SORESA_BANDI_INTENT_NAME:

            user = get_user(jsonobject['originalRequest']['data']['message']['from']['username'])
            # if(user.type == "impresa"):
            scraper = Scraper()
            list_bandi = scraper.getBandi()
            data = json.loads(list_bandi)
            speech = "Ecco i bandi per le imprese:\n\n"
            for i in range(len(data['result'])):
                speech += data['result'][i]['date'] + ": " + data['result'][i]['text'] + " - link: " + data['result'][i]['link'] + "\n\n"
            # else:
            #     speech = "Non ci sono informazioni utili per il tuo tipo di account\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_CONVENZIONI_INTENT_NAME:
            user = get_user(jsonobject['originalRequest']['data']['message']['from']['username'])

            # if (user.type == "pa"):
            scraper = Scraper()
            list_convenzioni = scraper.getConvenzioni()
            data = json.loads(list_convenzioni)

            for i in range(len(data['result'])):
                speech += data['result'][i]['date'] + ": " + data['result'][i]['text'] + " - link: " + \
                          data['result'][i]['link'] + "\n\n"
            # else:
            #     speech = "Non ci sono informazioni utili per il tuo tipo di account\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_LAVORA_CON_NOI_NAME:
            # user = get_user(jsonobject['originalRequest']['data']['message']['from']['username'])

            # if (user.type == "pa"):
            scraper = Scraper()
            list_convenzioni = scraper.LavoraConNoi()
            data = json.loads(list_convenzioni)

            speech = "Ecco gli ultimi 3 bandi di concorso sul sito Soresa.it\n\n"

            for i in range(len(data['result'][:3])):
                speech += data['result'][i]['text'] + "\n - link: " + \
                          data['result'][i]['link'] + "\n\n"

            # else:
            #     speech = "Non ci sono informazioni utili per il tuo tipo di account\n"

        elif jsonobject['result']['metadata']['intentName'] == SORESA_CHISIAMO_NAME:

            speech = "La So.Re.Sa. S.p.A. – Società Regionale per la Sanità – " \
                     "è una società strumentale costituita dalla Regione Campania " \
                     "per la realizzazione di azioni strategiche finalizzate alla razionalizzazione della spesa sanitaria regionale.\n" \
                     "Telefono: 081 212 8174\n" \
                     "Provincia: Provincia di Napoli\n" \
                     "Sito Web:  https://www.soresa.it/'>https://www.soresa.it/"


        elif 'Contatti_Orari' in jsonobject['result']['metadata']['intentName']:
            office = jsonobject['result']['parameters']['ufficio'].lower()
            office = re.sub('[\s+]', '', office)
            speech = utils.office_work_hour_contact_formatter(office)

        elif 'Contatti_Telefono' in jsonobject['result']['metadata']['intentName']:
            office = jsonobject['result']['parameters']['ufficio'].lower()
            office = re.sub('[\s+]', '', office)
            speech = utils.office_tel_contact_formatter(office)

        elif 'Contatti_Email' in jsonobject['result']['metadata']['intentName']:
            office = jsonobject['result']['parameters']['ufficio'].lower()
            office = re.sub('[\s+]', '', office)
            speech = utils.office_email_contact_formatter(office)

        elif 'Contatti_Informazioni' in jsonobject['result']['metadata']['intentName']:
            office = jsonobject['result']['parameters']['ufficio'].lower()
            office = re.sub('[\s+]', '', office)
            speech = utils.office_full_contact_formatter(office)

        elif jsonobject['result']['metadata']['intentName'] == SORESA_LOCATION_INTENT_NAME:

            speech = "I nostri uffici sono a Napoli, Complesso Esedra, Centro Direzionale Is. F9 80143 \n"
            speech += 'https://goo.gl/maps/mTs9KfbM4ZU2'
            source = jsonobject['result']['source']
            location = position

        elif jsonobject['result']['metadata']['intentName'] == SORESA_TRACCIA_BANDI_INTENT_NAME:

            user = get_user(jsonobject['originalRequest']['data']['message']['from']['username'])
            # if (user.type == "impresa"):
            scraper = Scraper()
            list_bandi = scraper.getBandi()
            data = json.loads(list_bandi)
            speech = "Ecco i bandi per le imprese:\n\n"
            inline_keyboard = []
            for i in range(len(data['result'])):
                speech += data['result'][i]['date'] + ": " + data['result'][i]['text'] + " - link: " + \
                          data['result'][i]['link'] + "\n\n"
                inline_keyboard.append([dict(text="Traccia Bando {}".format(i+1),url="https://elsa-proj.appspot.com/watcher_bandi?username={}&link={}".format(jsonobject['originalRequest']['data']['message']['from']['username'],base64.b64encode(data['result'][i]['link'])))])
            keyboard = dict(inline_keyboard=inline_keyboard)

            # else:
            #     speech = "Non ci sono informazioni utili per il tuo tipo di account\n"


        else:

            speech = self.request.body

        # Generating output JSON

        if keyboard is None and location is None:
            self.response.headers['Content-Type'] = 'application/json'

            out_json = json.dumps({
                    "speech": speech,
                    "displayText": speech,
                    "source": source
                }, indent=4)

            self.response.write(out_json)
        elif keyboard is not None:
            self.response.headers['Content-Type'] = 'application/json'

            out_json = json.dumps({
                "speech": speech,
                "displayText": speech,
                "source": source,
                 "data": {
                     "telegram": {
                       "chat_id": jsonobject['id'],
                       "text": speech,
                       "reply_markup": keyboard
                     }
                 }
            }, indent=4)

            logging.info(out_json)

            self.response.write(out_json)

        elif location is not None:
            self.response.headers['Content-Type'] = 'application/json'

            out_json = json.dumps({
                "speech": speech,
                "displayText": speech,
                "source": source
            }, indent=4)

            urlfetch.fetch("https://api.telegram.org/bot" + BOT_TOKEN + "/sendLocation",
                           payload=urllib.urlencode({
                                "chat_id": jsonobject['originalRequest']['data']['message']['chat']['id'],
                                "latitude": float(location['latitude']),
                                "longitude": float(location['longitude'])
                            }),
                           method=urlfetch.POST)

            logging.info(out_json)

            self.response.write(out_json)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterHandler),
    ('/watcher_bandi', BandiGaraHandler),
    ('/control_bandi', CronHandler)
], debug=True)
