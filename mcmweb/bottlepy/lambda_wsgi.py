import logging
from urllib.parse import urlencode
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


# noinspection PyBroadException
def handler(wsgi_app, event, context):
    wsgi_environ = {
        'wsgi.input': StringIO(event.get('body')),
        'wsgi.errors': StringIO(),
        'PATH_INFO': '/%s%s' % (str(event.get('requestContext', {}).get('stage', 'local')), str(event.get('path'))),
        'REQUEST_METHOD': str(event.get('httpMethod', 'GET'))
    }

    query_string = event.get('queryStringParameters')
    if query_string:
        wsgi_environ['QUERY_STRING'] = urlencode(query_string)

    headers = event.get('headers')
    if headers:
        for header, value in headers.items():
            header = str(header.replace('-', '_')).upper()
            if header not in SPECIAL_HEADERS:
                header = 'HTTP_%s' % header
            wsgi_environ[header] = str(value)

    start_response = StartResponse()
    wsgi_response = wsgi_app(wsgi_environ, start_response.start)

    lambda_response = {
        'body': b''.join(wsgi_response).decode('utf-8'),
        'headers': start_response.get_response_headers(),
        'statusCode': int(start_response.get_status().split(' ')[0])
    }

    if start_response.get_exc_info():
        try:
            raise start_response.get_exc_info()  # re-launch exception just for
        except:
            logging.exception('Error executing request')  # catching it here for logging

    return lambda_response
