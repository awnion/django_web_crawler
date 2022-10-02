from hashlib import sha256
from time import sleep
from bs4 import BeautifulSoup
from celery import shared_task
import httpx
from urllib.parse import urlparse, urljoin
from django.db.utils import IntegrityError

from .utils import normalize_url


@shared_task
def crawl(url: str):
    print(f'start {url}')
    # TODO: normalize url (e.g. %2a -> %2A)

    # 1. do all cleanups and checks
    clean_url_str = normalize_url(url)
    base_netloc = urlparse(clean_url_str).netloc
    print(f'base_netloc {base_netloc}')

    # reduce stress
    sleep(1)

    # TODO: interesting problem with redirects (redirect spam, hash spam)
    # TODO: retries
    r = httpx.get(clean_url_str, follow_redirects=True)
    print(r)
    if r.status_code != 200:
        return

    content_type = r.headers.get('content-type')
    if not content_type.startswith('text/html'):
        # if not HTML page
        print(f'SKIP: content-type is not HTML: {content_type}')
        return

    real_url = urlparse(normalize_url(str(r.url)))  # after redirects

    assert real_url.netloc != ''

    if real_url.netloc != base_netloc:
        # hardcoded: don't follow external links
        # TODO: actually should consider using strategy field
        print(f'SKIP: real_url netloc != base_netloc')
        return

    real_url_str = real_url.geturl()
    print(f'{real_url_str=}')

    # 2. process page

    # circular import
    from .models import Page

    try:
        page, created = Page.objects.get_or_create(
            url=real_url_str, content_hash=sha256(r.content).hexdigest()
        )
    except IntegrityError:
        # hash or url already parsed
        return

    if not created:
        # TODO: in the future we could need invalidate cache
        print(f'SKIP: already exists')
        return

    soup = BeautifulSoup(r.text, 'html.parser')

    # NOTE: external link can be internal after redirects
    # but we ignore that case
    internal_urls = set()

    for link in soup.find_all('a'):
        raw_url = link.get('href')
        print(f'found raw url {raw_url}')
        url = normalize_url(urljoin(real_url_str, raw_url))
        print(f'found new url {url}')
        if urlparse(url).netloc != base_netloc:
            # external link -> skip
            print(f'skip {url}')
            continue
        internal_urls.add(url)

    print(f'{internal_urls=}')

    for url in internal_urls:
        # setup tasks
        crawl.delay(url)

    # TODO: handle errors related to race conditions + retries in case DB error
    page.save()

    # TODO: fix overall consistency and persistency issues
