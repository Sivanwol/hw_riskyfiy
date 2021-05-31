import json
from urllib.parse import urlparse

import requests
from flask import request, url_for
from sqlalchemy import inspect

from src.utils.responses import response_error


def verify_response():
    if not request.is_json:
        return response_error({"msg": "Missing JSON in request"}, None, 400)


def scan_routes(app):
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urlparse("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


def request_post(url, headers, post_data={}):
    headers_default = {'Content-Type': 'application/json'}
    headers = headers_default | headers
    print('request post -> %s' % url)
    print('request headers -> %s' % json.dumps(headers))
    print('request post data-> %s' % json.dumps(post_data))
    r = requests.request('post', url, data=json.dumps(post_data), headers=headers)
    print('response post status code-> %s' % r.status_code)
    print('response post data-> %s' % r.content)
    if r.status_code == 200 or r.status_code == 400:
        try:
            resp_content = r.json()
            return resp_content
        except ValueError:
            return None
    return None


