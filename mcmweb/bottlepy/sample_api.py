from bottle import Bottle, request, response, debug

app = Bottle()
debug(True)


@app.route('/', method=['GET', 'POST'])
def main_route():
    response = '<h1>Funfa!</h1>'

    if request.headers:
        response += '<h3>Headers:</h3>\n'
        for header in request.headers:
            response += '<b>%s</b>: %s<br>\n' % (header, request.headers.get(header))

    if request.params:
        response += '<h3>Params com request.params:</h3>\n'
        for param in request.params:
            response += '<b>%s</b>: %s<br>\n' % (param, request.params.get(param))

    if request.POST:
        response += '<h3>Params com request.POST:</h3>\n'
        for param in request.POST:
            response += '<b>%s</b>: %s<br>\n' % (param, request.POST.get(param))

    return response


@app.route('/banana')
def banana_route():
    response.set_cookie("visited", "yes")
    return {'banana': True}


if __name__ == '__main__':
    from bottle import run
    run(app, debug=True, reloader=True)
