import json
from mcmweb.bottlepy.lambda_wsgi import handler
from mcmweb.bottlepy.sample_api import app


def sample_handler(event, context):
    print json.dumps(event)
    return handler(app, event, context)
