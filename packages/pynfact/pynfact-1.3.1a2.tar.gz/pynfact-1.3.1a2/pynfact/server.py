# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Simple server for testing purposes.

    :copyright: © 2012-2020, J. A. Corbal
    :license: MIT
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys


class Server:
    """Simple server."""

    def __init__(self, host='127.0.0.1', port=4000, path='_build',
                 logger=None):
        """Constructor.

        :param host: Addres where the server will be listening
        :type host: str
        :param port: Port where the server will be listening
        :type port: str
        :param path: Where the static website will be generated
        :type path: str
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        """
        self.port = port
        self.host = host
        self.path = path
        self.logger = logger

    def serve(self):
        """Serve a specific directory and waits for keyboard interrupt.

        :raise: FileNotFoundError, OSError, KeyboardInterrupt
        """
        try:  # Find the deploy directory
            os.chdir(self.path)
        except FileNotFoundError:
            self.logger and self.logger.error("Deploy directory not found")
            sys.exit(61)

        try:  # Initialize the serve
            httpd = HTTPServer((self.host, self.port),
                               SimpleHTTPRequestHandler)
        except OSError:
            self.logger and self.logger.error(
                "Address not valid or already in use")
            sys.exit(62)

        self.logger and self.logger.info("Serving %s:%s at %s",
                                         self.host, self.port, self.path)

        try:  # Listen until a keyboard interruption
            httpd.serve_forever()
        except KeyboardInterrupt:
            self.logger and self.logger.info("Interrupted!")

