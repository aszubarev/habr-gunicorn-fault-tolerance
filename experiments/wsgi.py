import logging
import os
from datetime import datetime
from time import sleep


logger = logging.getLogger('gunicorn.error')

def app(environ, start_response):
    """
    A basic WSGI application.
    """
    logger.info("Starting handle request")
    sleep(0.01)
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    output = b'index'
    content_length = str(len(output))
    response_headers.append(('Content-Length', content_length))

    start_response(status, response_headers)

    logger.info("Stopping handle request")
    return [output]
