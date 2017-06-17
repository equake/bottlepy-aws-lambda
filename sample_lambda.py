from mcmweb.bottlepy.lambda_wsgi import handler
from mcmweb.bottlepy.sample_api import app
from bottle import Bottle

lambda_app = Bottle()
lambda_app.mount('/prod/test', app)


def sample_handler(event, context):
    return handler(lambda_app, event, context)
