from urllib.parse import urlparse


def normalize_url(url) -> str:
    return urlparse(url)._replace(fragment='').geturl()
