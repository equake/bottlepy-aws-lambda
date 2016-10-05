from __future__ import print_function

import bottle
import json
import StringIO
from pprint import pprint

app = bottle.default_app()


@bottle.route('/py_bottle_test')
def index():
    return {'key': 'ha ha ha'}


def start_response(a, b, c=None):
    print('START_RESPONSE: %s, %s, %s' % (str(a), str(b), str(c)))


def handler(wsgi_app, event, context):
    pprint(event)
    wsgi_errors = StringIO.StringIO()
    wsgi_environ = {
        'wsgi.input': None,  # body
        'wsgi.errors': wsgi_errors,
        'CONTENT_TYPE': event['headers'].get('Content-Type'),
        'HTTP_COOKIE': '',
        'PATH_INFO': event['path'],
        'QUERY_STRING': event['queryStringParameters'],
        'REQUEST_METHOD': event['httpMethod']
    }

    response = wsgi_app(wsgi_environ, start_response)
    pprint(response)
    pprint(wsgi_errors.getvalue())
    # pprint(wsgi_app)
    # print(context)



if __name__ == '__main__':
    with open('../../test/aws_api_gateway_lambda_proxy.json') as api_gw_event_json:
        event = json.loads(api_gw_event_json.read())
    handler(app, event, None)
