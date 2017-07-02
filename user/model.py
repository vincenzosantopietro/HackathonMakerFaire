from google.appengine.ext import ndb
from Crypto.Hash import SHA256
import logging

class AccountModel(ndb.Model):
    username = ndb.StringProperty(required=True)
    user_id = ndb.KeyProperty(required=True)
    type = ndb.StringProperty(required=True, choices=[
        'privato',
        'pa',
        'asl',
        'impresa'
    ])
    chat_id = ndb.StringProperty(required=True)

    def get_key_from_username(self):
        return ndb.Key(AccountModel, SHA256.new(self.username).hexdigest())


class AliasModel(ndb.Model):
    alias = ndb.StringProperty(required=True)
    platform = ndb.StringProperty(required=True)


class BandiWatcherModel(ndb.Model):
    username = ndb.StringProperty(required=True)
    link = ndb.StringProperty(required=True)
    last_edits = ndb.TextProperty(required=True)

