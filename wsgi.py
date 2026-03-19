from time import sleep


def app(environ, start_response):
    """
    A basic WSGI application.
    """
    sleep(0.008)
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    output = b'index'
    content_length = str(len(output))
    response_headers.append(('Content-Length', content_length))

    start_response(status, response_headers)
    return [output]
