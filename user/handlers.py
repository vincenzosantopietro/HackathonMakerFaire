from model import *


def insert_user(username, type, platform='telegram'):

    key = ndb.Key(AccountModel, username)

    user = AccountModel.query(AccountModel.key == key).get()

    if user is None:
        user = AccountModel()
        user.username = username
        user.key = user.get_key_from_username()
        user.type = type
        user.put()

        user_alias = AliasModel(parent=user.key)
        user_alias.aliases = [username]
        user_alias.platforms = [platform]
        user_alias.put()


def get_user(username):
    key = ndb.Key(AccountModel, username)
    return AccountModel.query(AccountModel.key == key).get()