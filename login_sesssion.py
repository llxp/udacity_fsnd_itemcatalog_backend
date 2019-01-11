class LoginSessionItem:
    access_token: str = ""
    gplus_id: str = ""
    username: str = ""
    picture: str = ""
    email: str = ""
    session_token: str = ""
    userinfo_url: str = ""
    logged_in: bool = False


class LoginSession:
    session_tokens = {}

    def __getitem__(self, key: str) -> LoginSessionItem:
        if key in self.session_tokens:
            return self.session_tokens.get(key)
        return None

    def __setitem__(self, key: str, value: LoginSessionItem):
        self.session_tokens[key] = value

    def __delitem__(self, key):
        del self.session_tokens[key]

    def keys(self):
        return self.session_tokens.keys()
