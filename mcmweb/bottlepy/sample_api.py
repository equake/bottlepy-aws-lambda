from bottle import Bottle, request, debug

app = Bottle()
debug(True)


@app.route('/py_bottle_test')
def index():
    return {'a': 'b', 'c': 'd'}


@app.route('/path/to/resource', method=['GET', 'POST'])
def post_url():
    params = dict()
    headers = dict()

    for key in request.GET:
        params[key] = request.GET.get(key)

    for key in request.headers:
        headers[key] = request.headers.get(key)

    return {'method': request.method, 'params': params, 'headers': headers}


@app.route('/test')
def test():
    response = '<h1>Funfa!</h1>'

    if request.headers:
        response += '<h3>Headers:</h3>\n'
        for header in request.headers:
            response += '<b>%s</b>: %s<br>\n' % (header, request.headers.get(header))

    if request.GET:
        response += '<h3>Params com request.GET:</h3>\n'
        for param in request.GET:
            response += '<b>%s</b>: %s<br>\n' % (param, request.GET.get(param))

    return response


if __name__ == '__main__':
    from bottle import run
    run(app, debug=True, reloader=True)
