from urllib.parse import urlparse
from urllib.request import urlopen


def fetch(url):
    with urlopen(url) as f:
        return f.read().decode('utf-8')


def is_webresource(url):
    # Lets consider that a valid web resource should be always prefixed
    # by http scheme, otherwise we consider is not a web resource.
    return "http" in urlparse(url).scheme
