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

class MainHandler(webapp2.RequestHandler):

    def post(self):
        jsonobject = json.loads(self.request.body)

        speech = ""
        source = ""

        if jsonobject['result']['metadata']['intentName'] == SORESA_NEWS_INTENT_NAME:
            newsScraper = SoresaNewsScraper()
            news_json = json.loads(newsScraper.getNews())

            speech = "Ecco gli ultimi 3 articoli pubblicati sul sito soresa.it\n\n"
            source = jsonobject['result']['source']

            for i in range(3):
                speech += news_json['result'][i]['date'] + ": " + news_json['result'][i]['title'] + " - link: " + news_json['result'][i]['url'] + "\n\n"




        self.response.headers['Content-Type'] = 'application/json'

        out_json = json.dumps({
                "speech":speech,
                "displayText":speech,
                "source":source
            },indent=4)

        self.response.write(out_json)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
