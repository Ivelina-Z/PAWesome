import secrets
from django.core import signing
from django.http import Http404


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

    @staticmethod
    def check_token(model, token):
        try:
            user = model.objects.get(token=token)
        except model.DoesNotExist:
            raise Http404('Invalid token.')
        return user
