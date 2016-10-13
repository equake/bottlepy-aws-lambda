from __future__ import print_function

import logging
import urllib
from StringIO import StringIO


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
    wsgi_environ = {
        'wsgi.input': event.get('body'),
        'wsgi.errors': StringIO(),
        # 'CONTENT_TYPE': event['headers'].get('Content-Type'),
        'PATH_INFO': str(event.get('path', '/')),
        'REQUEST_METHOD': str(event.get('httpMethod', 'GET'))
    }

    if 'queryStringParameters' in event and event['queryStringParameters']:
        wsgi_environ['QUERY_STRING'] = urllib.urlencode(event['queryStringParameters'])
    else:
        wsgi_environ['QUERY_STRING'] = ''

    if 'headers' in event and event['headers']:
        for key, value in event['headers'].iteritems():
            cgi_key = 'HTTP_%s' % key.replace('-', '_').upper()
            wsgi_environ[cgi_key] = value

    start_response = StartResponse()
    wsgi_response = wsgi_app(wsgi_environ, start_response.start)

    lambda_response = {
        'body': ''.join(wsgi_response),
        'headers': start_response.get_response_headers(),
        'statusCode': int(start_response.get_status().split(' ')[0])
    }

    # error_value = wsgi_environ['wsgi.errors'].getvalue()
    # if error_value:
    #     lambda_response['Error'] = error_value

    if start_response.get_exc_info():
        try:
            raise start_response.get_exc_info()
        except:
            # lambda_response['Exception'] = str(start_response.get_exc_info())  # blargh :(
            logging.exception('Error executing request')

    return lambda_response
