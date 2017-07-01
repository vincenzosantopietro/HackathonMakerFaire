from google.appengine.ext import ndb
from Crypto.Hash import SHA256


class AccountModel(ndb.Model):
    username = ndb.StringProperty(required=True)
    key = ndb.KeyProperty(required=True)
    type = ndb.StringProperty(required=True, choices=[
        'privato',
        'pa',
        'asl',
        'impresa'
    ])

    def get_key_from_username(self):
        return SHA256.new(self.username).hexdigest()


class AliasModel(ndb.Model):
    aliases = ndb.StringProperty(required=True)
    platforms = ndb.StringProperty(required=True)

