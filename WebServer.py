# coding=utf-8
__author__ = 'Ben'

import BaseHTTPServer
import SimpleHTTPServer
import time
import urllib
import sys
from threading import Thread

BASE_DIR = 'Webfiles'
PORT = 80


class WebHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """An instance is created to handler every connection to the web interface."""

    def __init__(self, request, client_address, server):
        self.parent = server.parent  # This handy bit of code allows the web handler to still have reference to the server thread, and through that, the Game Server.
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        """This is a request for a file. The file the user wants is either built for them or loaded from disk and given to them."""
        print self.path
        if self.path == "/test":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.parent.draw_board())
        else:  # Not a file that's being overridden. Just give them the file from disk.
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):  # Stop the torrent of output.
        return

    def do_POST(self):
        """Handle a post request by returning the square of the number."""
        length = int(self.headers.getheader('content-length'))
        data_string = self.rfile.read(length)
        a = data_string.split("&")
        c = {}
        # Data about POST request
        print data_string

        for b in a:
            d = b.split("=")
            c[d[0]] = d[1]

        for key in c:
            c[key] = urllib.unquote_plus(c[key])

        print "Dictionary of request data", c
        # Dictionary created

        result = ""
        if "MOVE" in c:
            if c["MOVE"] == "PLAY":
                if not "PLAYER" in c["MOVEDATA"] or not "X" in c["MOVEDATA"] or not "Y" in c["MOVEDATA"]:
                    self.log(1, "Data missing from request", c)
                    return ""
                else:
                    player = c["MOVEDATA"]["PLAYER"]
                    x = c["MOVEDATA"]["X"]
                    y = c["MOVEDATA"]["Y"]
                    self.parent.play_cell([x, y], player)
            if c["MOVE"] == "RESET":
                self.parent.reset_board()
        else:
            result = "failed:" + data_string
        self.wfile.write(result)

    def log(self, level, *args):
        """
        Logs data.
        :param level: Level of importance. 0:print, 1-5:Debug
        :type level: int
        :param args: separate arguments to print
        :return: Does not return.
        """
        message = ""
        for arg in args:
            message += str(arg)
        if level == 0:
            print "[Web Handler]",
            print time.strftime("%c"),
            print message


class myServer(BaseHTTPServer.HTTPServer):
    """
    This is necessary so that the Handler can access the DB connection.
    """

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, parent=None):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.parent = parent


class Web(Thread):
    """
    Container to hold the server.
    """

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.server = self.create_server()
        self.go = True
        self.stopped = False

    def log(self, level, *args):
        """
        Logs data.
        :param level: Level of importance. 0:print, 1-5:Debug
        :type level: int
        :param args: separate arguments to print
        :return: Does not return.
        """
        message = ""
        for arg in args:
            message += str(arg)
        if level == 0:
            print "[Frontend]",
            print time.strftime("%c"),
            print message

    def getlocalip(self):
        """
        Returns the local ip address to host on.
        :return:
        """
        import sys, socket
        if sys.platform == "win32":
            return socket.gethostbyname(socket.gethostname())
        else:
            import os
            f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
            return f.read()[:-1]

    def create_server(self):
        """Start the server."""
        server_address = (self.getlocalip(), PORT)
        server = myServer(server_address, WebHandler, True, self)
        print server_address
        return server

    def shutdown(self):
        self.go = 0
        self.server.server_close()

    def run(self):
        """A hacked version of server_forever."""
        try:
            if sys.platform == "linux2":
                self.server.socket.settimeout(2)
            while self.go:
                self.server.handle_request()
        except Exception as e:
            import logging
            logging.exception("Error while handling request. {}".format(str(e)))
        finally:
            self.server.server_close()
            print "Web server has shut down."
        self.stopped = True
