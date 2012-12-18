#!/usr/bin/env python


# I think Will McCutchen wrote this originally? Not sure.
"""
Basically:

    curl -s -u "$user:$pass" -X POST "http://api-ssl.bitly.org/oauth/access_token" --header "X-Scheme: https"
    curl -s -H "X-Scheme: https" "http://api.bitly.org$1?access_token=$access_token" | python2.7 -mjson.tool

"""

import cgi
import getpass
import os
import re
import sys
import urlparse

import simplejson as json
import requests


__usage__ = """%(cmd)s url

Makes a request to the given URL, which is assumed to be a bitly API endpoint.
If no access_token param is found in the URL, an access token will be fetched
and and added to the request.

Examples:

    %(cmd)s /v3/user/info
    %(cmd)s api.bitly.org/v3/user/info?login=will
    %(cmd)s api-ssl.bitly.net/v3/user/link_history?limit=1&offset=20
    %(cmd)s https://api-ssl.bitly.com/v3/user/info

""" % dict(cmd=os.path.basename(sys.argv[0]))

# Valid API hosts
hosts = [
    'http://api.bitly.org',
    'https://api-ssl.bitly.com',
    'https://api-ssl.bitly.net',
]
default_host = hosts[0]

token_path = os.path.expanduser('~/.bitly_api_tokens')


def load_tokens():
    try:
        return json.load(open(token_path))
    except:
        return {}


def write_tokens(tokens):
    json.dump(tokens, open(token_path, 'w'), indent=2)


def get_headers():
    return {'X-Scheme': 'https'}


def get_token(host):
    tokens = load_tokens()
    if host in tokens:
        return tokens[host]
    else:
        print 'Getting OAuth token for %s...' % host
        user = raw_input('username: ')
        password = getpass.getpass('password: ')
        url = host + '/oauth/access_token'
        resp = requests.post(
            url, headers=get_headers(), body='',
            auth=(user, password))
            #validate_cert=False)
        if resp.status == 401:
            print >> sys.stderr, 'Invalid username/password.'
            return get_token(host)
        resp.raise_for_status()
        token = resp.body.strip()
        tokens[host] = token
        write_tokens(tokens)
        return token


def fetch(url):
    # If we were given a URL like /v3/user/link_history, we assume we're
    # making a request against a local dev VM.
    if url.startswith('/'):
        url = default_host + url

    # And we'll add the scheme if it's not given
    elif not re.match(r'^https?://', url):
        url = 'https://' + url

    try:
        scheme, host, path, _, qs, frag = urlparse.urlparse(url)
    except Exception, e:
        print >> sys.stderr, 'Invalud URL: %s (%s)' % (url, e)
        return 1

    host = scheme + '://' + host
    if host not in hosts:
        print >> sys.stderr, 'Invalid host: %r (valid hosts: %s)' % (
            host, ', '.join(hosts))
        return 1

    params = cgi.parse_qs(qs)
    if not params.get('access_token'):
        params['access_token'] = get_token(host)

    response = requests.get(host + path, params=params, headers=get_headers())
    response.raise_for_status()
    return response.json()


def main(url):
    info = fetch(url)
    print json.dumps(info, indent=2)
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Invalid command. Usage:\n\n%s' % __usage__
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
