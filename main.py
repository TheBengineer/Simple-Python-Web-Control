import time

import GameServer
import WebServer

if __name__ == "__main__":
    go = True
    game = GameServer.Game()
    game.start()
    web = WebServer.Web(game)
    web.start()
    while go:
        try:
            d = raw_input("(Q)uit, (W)ebServer, (G)ameServer\n")
        except EOFError:
            continue
        except KeyboardInterrupt:
            print "Keyboard interrupt. Exiting..."
            go = False
            break
        if "Q" in d.upper():
            print "Quiting"
            go = False
            break
        if "W" in d.upper():
            print "Reloading Web Server"
        if "G" in d.upper():
            print "Reloading Game Server"
        time.sleep(1)
    else:

        # TODO close server class here
