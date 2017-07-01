import webapp2
from user.handlers import *


class RegisterHandler(webapp2.RequestHandler):

    def get(self):

        username = self.request.get('username')
        type = self.request.get('type')

        insert_user(username, type)

        self.response.out.write("Sei stato registrato a E.L.S.A. Per usufruire dei contenuti continua ad interagire con il bot su Telegram!")



