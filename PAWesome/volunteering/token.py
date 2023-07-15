import secrets
from django.core import signing


class Token:
    def __init__(self):
        self.signed_token = self.make_token()

    def make_token(self):
        token = secrets.token_hex(16)
        self.signed_token = signing.dumps(token)
        return self.signed_token

    def get_token(self):
        token = signing.loads(self.signed_token)
        return token
