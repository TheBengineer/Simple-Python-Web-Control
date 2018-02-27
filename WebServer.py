# coding=utf-8
__author__ = 'Ben'

import BaseHTTPServer
import SimpleHTTPServer
import time
import json
import urllib
import sys
from threading import Thread

BASE_DIR = ''
PORT = 80


class WebHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """An instance is created to handler every connection to the web interface."""

    def __init__(self, request, client_address, server):
        self.parent = server.parent  # This handy bit of code allows the web handler to still have reference to the server thread, and through that, the Game Server.
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        """This is a request for a file. The file the user wants is either built for them or loaded from disk and given to them."""
        print self.path
        if ("?" in self.path and self.path[:self.path.find("?")] == "/html") or self.path == "/html":
            a = self.path.split("?")[1:]
            print a
            player = " "
            if a:
                c = {}
                # Data about POST request

                for b in a:
                    d = b.split("=")
                    c[d[0]] = d[1]

                for key in c:
                    c[key] = urllib.unquote_plus(c[key])

                print "Dictionary of request data", c
                if "PLAYER" in c:
                    player = c["PLAYER"]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # self.wfile.write(self.parent.parent.draw_board())
            # self.wfile.write(" <meta http-equiv=\"refresh\" content=\"2\" />")
            self.wfile.write("<style></style>")
            if player == "O":
                self.wfile.write("<form method=\"post\"><table><tr><td><input type=\"radio\" name=\"PLAYER\" value=\"X\">Player X<br></td>"
                                 "<td><input type=\"radio\" name=\"PLAYER\" value=\"O\" checked>Player O<br></td></tr></table>"
                                 "<table><tr><td></td></tr></table>")
            else:
                self.wfile.write("<form method=\"post\"><table><tr><td><input type=\"radio\" name=\"PLAYER\" value=\"X\" checked>Player X<br></td>"
                                 "<td><input type=\"radio\" name=\"PLAYER\" value=\"O\">Player O<br></td></tr></table>"
                                 "<table><tr><td></td></tr></table>")
            self.wfile.write("<input type='hidden' name='ACTION' value='PLAY'>")
            self.wfile.write("<table>")
            for x in range(3):
                self.wfile.write("<tr>")
                for y in range(3):
                    self.wfile.write("<td>")
                    self.wfile.write("<button type='submit' name='CELL' value='{}' style='width:100px; height:100px; font-size:80px'>{}".format(y + (x * 3), self.parent.parent.board[x][y]))
                    self.wfile.write("</td>")
                self.wfile.write("</tr>")
            self.wfile.write("</table>")
            self.wfile.write("</form>")

            self.wfile.write("<form method=\"post\"><button name=\"ACTION\" value=\"RESET\">RESET</button></form>")
        if ("?" in self.path and self.path[:self.path.find("?")] == "/asdf") or self.path == "/asdf":
            a = self.path.split("?")[1:]
            print a
            player = " "
            if a:
                c = {}
                # Data about POST request

                for b in a:
                    d = b.split("=")
                    c[d[0]] = d[1]

                for key in c:
                    c[key] = urllib.unquote_plus(c[key])

                print "Dictionary of request data", c
                if "PLAYER" in c:
                    player = c["PLAYER"]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # self.wfile.write(self.parent.parent.draw_board())
            # self.wfile.write(" <meta http-equiv=\"refresh\" content=\"2\" />")
            self.wfile.write("<style></style>")
            if player == "O":
                self.wfile.write("<form method=\"post\"><table><tr><td><input type=\"radio\" name=\"PLAYER\" value=\"X\">Player X<br></td>"
                                 "<td><input type=\"radio\" name=\"PLAYER\" value=\"O\" checked>Player O<br></td></tr></table>"
                                 "<table><tr><td></td></tr></table>")
            else:
                self.wfile.write("<form method=\"post\"><table><tr><td><input type=\"radio\" name=\"PLAYER\" value=\"X\" checked>Player X<br></td>"
                                 "<td><input type=\"radio\" name=\"PLAYER\" value=\"O\">Player O<br></td></tr></table>"
                                 "<table><tr><td></td></tr></table>")
            self.wfile.write("<input type='hidden' name='ACTION' value='PLAY'>")
            self.wfile.write("<table>")
            for x in range(3):
                self.wfile.write("<tr>")
                for y in range(3):
                    self.wfile.write("<td>")
                    self.wfile.write("<button type='submit' name='CELL' value='{}' style='width:100px; height:100px; font-size:80px'>{}".format(y + (x * 3), self.parent.parent.board[x][y]))
                    self.wfile.write("</td>")
                self.wfile.write("</tr>")
            self.wfile.write("</table>")
            self.wfile.write("</form>")

            self.wfile.write("<form method=\"post\"><button name=\"ACTION\" value=\"RESET\">RESET</button></form>")
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

        result = "asdf"
        if "ACTION" in c:
            if c["ACTION"] == "PLAY":
                if not "PLAYER" in c or not "CELL" in c:
                    self.log(1, "Data missing from request", c)
                    return ""
                else:
                    player = c["PLAYER"]
                    cell = int(c["CELL"])
                    x = cell / 3
                    y = cell % 3
                    self.parent.parent.play_cell([x, y], player)
                    if self.parent.parent.check_win("X"):
                        print "X wins"
                        self.parent.parent.reset_board()
                        result = "<!DOCTYPE html><html><head><style></style>" \
                                 "<a href=\"html\"><button >Done</button></a></body></html>"
                    elif self.parent.parent.check_win("O"):
                        print "O wins"
                        self.parent.parent.reset_board()
                        result = "<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0; /html?PLAYER={}\" /></body></html>".format(player)
                    else:
                        result = "<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0; /html?PLAYER={}\" /></body></html>".format(player)
            elif c["ACTION"] == "RESET":
                self.parent.parent.reset_board()
                result = "<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0; /html\" /></body></html>"
            elif c["ACTION"] == "GETBOARD":
                board_data = self.parent.parent.board[:]
                result = json.dumps({"BOARD": board_data}, separators=(',', ':'))
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
