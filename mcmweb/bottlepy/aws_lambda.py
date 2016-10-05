from __future__ import print_function

import json
from StringIO import StringIO
from pprint import pprint

import bottle


app = bottle.default_app()

# app.uninstall(bottle.JSONPlugin)
# app.install(bottle.JSONPlugin(json_dumps=str))


@bottle.route('/py_bottle_test')
def index():
    return {'a': 'b', 'c': 'd'}


class StartResponse(object):
    status = None
    response_headers = None
    exc_info = None

    def __init__(self):
        pass

    def start(self, status, response_headers, exc_info=None):
        self.status = status
        self.response_headers = response_headers
        self.exc_info = exc_info

    def get_status(self):
        return self.status

    def get_response_headers(self):
        return dict(self.response_headers)

    def get_exc_info(self):
        return self.exc_info


def handler(wsgi_app, event, context):
    # pprint(event)
    wsgi_environ = {
        'wsgi.input': None,  # body
        'wsgi.errors': StringIO(),
        'CONTENT_TYPE': event['headers'].get('Content-Type'),
        'HTTP_COOKIE': '',
        'PATH_INFO': event['path'],
        'QUERY_STRING': event['queryStringParameters'],
        'REQUEST_METHOD': event['httpMethod']
    }

    start_response = StartResponse()
    wsgi_response = wsgi_app(wsgi_environ, start_response.start)
    # print(tuple(wsgi_response))
    response = {
        'Body': wsgi_response,
        'Error': wsgi_environ['wsgi.errors'].getvalue(),
        'Headers': start_response.get_response_headers(),
        'Status': start_response.get_status()
    }
    if start_response.get_exc_info():
        response['Exception'] = str(start_response.get_exc_info())  # blargh :(

    return response


if __name__ == '__main__':
    with open('../../test/aws_api_gateway_lambda_proxy.json') as api_gw_event_json:
        event = json.loads(api_gw_event_json.read())
    pprint(handler(app, event, None))
