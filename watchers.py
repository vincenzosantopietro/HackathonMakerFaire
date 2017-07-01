import webapp2
import base64


class BandiGaraHandler(webapp2.RequestHandler):

    def get(self):
        # seleziona un bando da tracciare
        link = base64.b64decode(self.request.get('link'))
        pass


class CronHandler(webapp2.RequestHandler):

    def get(self):

        # controlla lo stato del bando
        pass