import logging
import urllib
from io import StringIO

SPECIAL_HEADERS = ('CONTENT_TYPE', 'CONTENT_LENGTH')


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
        'wsgi.input': StringIO(event.get('body')),
        'wsgi.errors': StringIO(),
        'PATH_INFO': '/%s%s' % (str(event['requestContext']['stage']), str(event['path'])),
        'REQUEST_METHOD': str(event.get('httpMethod', 'GET'))
    }

    if 'queryStringParameters' in event and event['queryStringParameters']:
        wsgi_environ['QUERY_STRING'] = urllib.urlencode(event['queryStringParameters'])

    if 'headers' in event and event['headers']:
        for header, value in event['headers'].items():
            header = str(header.replace('-', '_')).upper()
            if header not in SPECIAL_HEADERS:
                header = 'HTTP_%s' % header
            wsgi_environ[header] = str(value)

    start_response = StartResponse()
    wsgi_response = wsgi_app(wsgi_environ, start_response.start)

    lambda_response = {
        'body': ''.join(wsgi_response),
        'headers': start_response.get_response_headers(),
        'statusCode': int(start_response.get_status().split(' ')[0])
    }

    if start_response.get_exc_info():
        try:
            raise start_response.get_exc_info()
        except:
            logging.exception('Error executing request')

    return lambda_response
