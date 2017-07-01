import webapp2
import json

class RegisterHandler(webapp2.RequestHandler):

    def get(self):

        if self.request.body is not None:
            jsonobject = json.loads(self.request.body)

            self.response.write(
                {
                    "speech":self.request.body,
                    "displayText":self.request.body,
                    "source": jsonobject['result']['source']
                }
            )
