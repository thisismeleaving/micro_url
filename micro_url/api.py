"""
Author: Berty Pribilovics

A simple JSON REST API for URL shortening.

"""
import json
from datetime import datetime

import short_url
import user_agents

from bottle import (default_app, get, post, run, request,
                    response, hook, redirect, HTTPError)

from sqlitedb import cursor


@get('/')
@get('/<slug>')
def index(slug=None):
    """
    If a shortened URL is not provided return the list of URLs.
    If a shortened URL is provided attempt to Detect device type and route to the appropriate URL
    If device type is undertermined or no target is specified for that device type default to desktop

    """
    if slug is None:
        host = request.get_header('host')
        res = {'data': [], 'total': 0}
        try:
            with cursor() as dbc:
                dbc.execute("""SELECT * FROM main.urls""")
                records = dbc.fetchall()

            data = [
                {
                    'shortened_url': get_url(host, r.get('slug')),
                    'redirects': json.loads(r.get('cfg')),
                    'time_since_creation': elapsed_time(r.get('created'))
                }
                for r in records
            ]
            res['data'] = data
            res['total'] = len(data)
        except Exception as e:
            print(repr(e))

        return res

    with cursor() as dbc:
        dbc.execute("""SELECT cfg from main.urls where slug=?""", (slug,))
        res = dbc.fetchone()
        if res:
            cfg = json.loads(res.get('cfg'))
            ua = user_agents.parse(request.get_header('User-Agent'))
            mobile_url = cfg.get('mobile').get('url')
            tablet_url = cfg.get('tablet').get('url')
            desktop_url = cfg.get('desktop').get('url')

            if ua.is_mobile and mobile_url:
                url = mobile_url
                cfg['mobile']['hits'] += 1

            elif ua.is_tablet and tablet_url:
                url = tablet_url
                cfg['tablet']['hits'] += 1

            else:
                url = desktop_url
                cfg['desktop']['hits'] += 1

            # attempt to standardize url
            if not 'http' in url:
                url = 'http://{}'.format(url)

            with cursor() as dbc:
                dbc.execute(
                    """UPDATE main.urls set cfg=? where slug=?""", (json.dumps(cfg), slug))

            redirect(url)
        else:
            raise HTTPError(404, 'Resource Not Found')


@post('/')
def url():
    """
    Generate a shortened url. Expects a raw json payload with at least 'desktop' defined
    {
        'mobile' : '',
        'tablet' : '',
        'desktop' :'google.com'
    }

    """
    data = request.json
    created = datetime.now().timestamp()
    try:
        targets = {
            'mobile': {
                'url': data.get('mobile', ''),
                'hits': 0
            },
            'tablet': {
                'url': data.get('tablet', ''),
                'hits': 0
            },
            'desktop': {
                'url': data.get('desktop', ''),
                'hits': 0
            }
        }

        with cursor() as dbc:
            res = dbc.execute(
                "INSERT INTO main.urls(cfg, created) values(?,?)",
                (json.dumps(targets),
                 created))
            _id = res.lastrowid
            slug = short_url.encode_url(_id)
            dbc.execute("UPDATE main.urls set slug=? where id=?", (slug, _id))
    except Exception as e:
        raise HTTPError(400, 'Bad Request - This route expects a POST of raw JSON')

    return {'shortened_url': get_url(request.get_header('host'), slug)}


def get_url(host, slug):
    return 'http://{}/{}'.format(host, slug)


def elapsed_time(timestamp):
    """
    Return a string describing the amount of time that has passed
    since the supplied timestamp
    
    """
    return str(datetime.now() - datetime.fromtimestamp(timestamp))


if __name__ == "__main__":
    app = run(host="0.0.0.0", port=8000, debug=True)
