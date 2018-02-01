#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import BaseHTTPServer


class ServerException(Exception):
    """
    docstring for ServerException
    """
    pass


class case_no_file(object):
    """
    docstring for case_no_fie
    """

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))


class case_existing_file(object):
    """
    docstring for case_existing_file
    """

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        handler.handler_file(handler.full_path)


class case_always_fail(object):
    """
    docstring for case_always_fail
    """

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknow object '{0}'".format(handler.path))


class ResquestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    docstring for ResquestHandler
    """
    Cases = [case_no_file(), case_existing_file(), case_always_fail(())]

    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path

            for case in self.Case:
                if case.test(self):
                    case.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        try:
            with open(full_path, "rb") as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.sent_content(content, 404)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, ResquestHandler)
    server.serve_forever()
