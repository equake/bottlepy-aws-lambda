from bottle import Bottle, request, response, debug

app = Bottle()
debug(True)


@app.route('/', method=['GET', 'POST'])
def main_route():
    html = '<h1>Funfa!</h1>'

    if request.headers:
        html += '<h3>Headers:</h3>\n'
        for header in request.headers:
            html += '<b>%s</b>: %s<br>\n' % (header, request.headers.get(header))

    if request.params:
        html += '<h3>Params com request.params:</h3>\n'
        for param in request.params:
            html += '<b>%s</b>: %s<br>\n' % (param, request.params.get(param))

    if request.POST:
        html += '<h3>Params com request.POST:</h3>\n'
        for param in request.POST:
            html += '<b>%s</b>: %s<br>\n' % (param, request.POST.get(param))

    return html


@app.route('/banana')
def banana_route():
    response.set_cookie("visited", "yes")
    return {'banana': True}


if __name__ == '__main__':
    from bottle import run
    run(app, debug=True, reloader=True)
