def app(environ, start_response):
    """
    A basic WSGI application.
    """
    status = '200 OK'
    output = b'index'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output))),
    ]

    start_response(status, response_headers)

    return [output]
