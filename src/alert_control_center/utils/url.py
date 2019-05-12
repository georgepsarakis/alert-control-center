from django.utils.crypto import get_random_string


def short_url_token(length=20):
    return get_random_string(length)
