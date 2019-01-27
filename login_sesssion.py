import app_init
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import load_only
from flask import json

app_init.db.create_all()

class LoginSessionItem(app_init.db.Model):
    __tablename__: str = 'SESSION'
    id: int = Column(Integer, primary_key=True)
    access_token: str = Column(String)
    gplus_id: str = Column(String)
    username: str = Column(String)
    picture: str = Column(String)
    email: str = Column(String)
    session_token: str = Column(String)
    userinfo_url: str = Column(String)
    logged_in: bool = Column(Boolean, default=False)


class LoginSession:
    # session_tokens = {}

    def __getitem__(self, key: str) -> LoginSessionItem:
        loginSessionItem: LoginSessionItem = LoginSessionItem.query.filter_by(session_token=key).first()
        if loginSessionItem is not None:
            # print(json.dumps(loginSessionItem))
            return loginSessionItem
        # if key in self.session_tokens:
            # return self.session_tokens.get(key)
        return None

    def __setitem__(self, key: str, value: LoginSessionItem):
        loginSessionItem: LoginSessionItem = LoginSessionItem.query.filter_by(session_token=key).first()
        if loginSessionItem is not None:
            loginSessionItem.access_token = value.access_token
            loginSessionItem.gplus_id = value.gplus_id
            loginSessionItem.username = value.username
            loginSessionItem.picture = value.picture
            loginSessionItem.email = value.email
            loginSessionItem.userinfo_url = value.userinfo_url
            loginSessionItem.logged_in = value.logged_in
            print("session object updated")
        else:
            print("add object to database")
            # print(json.dumps(value))
            app_init.db.session.add(value)
        app_init.db.session.commit()
        # self.session_tokens[key] = value

    def __delitem__(self, key):
        loginSessionItem: LoginSessionItem = LoginSessionItem.query.filter_by(session_token=key).first()
        if loginSessionItem is not None:
            app_init.db.session.delete(loginSessionItem)
            app_init.db.session.commit()
        # del self.session_tokens[key]

    def keys(self):
        keys_list = []
        for x in LoginSessionItem.query.options(load_only("session_token")).all():
            print(x.session_token)
            keys_list.append(x.session_token)
        print(keys_list)
        return keys_list
        # return self.session_tokens.keys()
