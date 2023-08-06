import multiprocessing
import requests
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from w3bch3ck.colorizers import (
    ok,
    notice,
)


def host(domain):
    if domain.startswith('http://'):
        domain.split('http://')


def check(source_domain):
    headers = dict()
    headers['Pragma'] = 'no-cache'
    headers['Referer'] = source_domain
    headers['User-Agent'] = (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/78.0.3904.108 YaBrowser/19.12.3.332 (beta) Yowser/2.5 Safari/537.36')

    response_page_title = None
    response_status = None
    response_url = None
    response_hostname = None
    response_ip = None
    source_hostname = None
    source_ip = None

    error = None

    try:
        response = requests.get(
            source_domain if source_domain.startswith('http') else 'http://%s' % source_domain,
            headers=headers
        )

        response.encoding = 'utf-8'

        if response.status_code:

            response_status = response.status_code
            response_url = response.url

            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('title')

            if len(titles):
                response_page_title = titles[0].text

            response_hostname = urlparse(response_url).hostname
            try:
                response_ip = socket.gethostbyname(response_hostname)
            except:
                pass

            source_hostname = urlparse(source_domain).hostname
            try:
                source_ip = socket.gethostbyname(source_hostname)
            except:
                pass
    except Exception as e:
        error = getattr(e, 'message', repr(e))

    return dict(
        source_domain=source_domain,
        source_hostname=source_hostname,
        source_ip=source_ip,
        response_status=response_status,
        response_page_title=response_page_title,
        response_url=response_url,
        response_hostname=response_hostname,
        response_ip=response_ip,
        error=error,
    )


def pooled_check(domains, callback_method=None, processes_count: int = None):
    if processes_count is None:
        processes_count = 2
    if callback_method is None:
        callback_method = do_nothing
    _pool = multiprocessing.Pool(processes=processes_count)

    for domain in domains:
        print(notice('Add pool check for: %s' % domain))
        _pool.apply_async(check, args=(domain,), callback=callback_method)

    _pool.close()
    print(ok('Start...'))
    _pool.join()
    print(ok('End.'))


def do_nothing(data):
    return data
