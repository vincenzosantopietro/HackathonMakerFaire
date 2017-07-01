from model import *


def insert_user(username, type, platform='telegram'):

    key = ndb.Key(AccountModel, username)

    user = AccountModel.query(AccountModel.user_id == key).get()

    if user is None:
        user = AccountModel()
        user.username = username
        user.user_id = user.get_key_from_username()
        user.type = type
        user.put()

        user_alias = AliasModel(parent=user.user_id)
        user_alias.alias = username
        user_alias.platform = platform
        user_alias.put()


def get_user(username):
    key = ndb.Key(AccountModel, username)
    return AccountModel.query(AccountModel.user_id == key).get()
