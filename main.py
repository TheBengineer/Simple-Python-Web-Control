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
            web.go = False
            reload(WebServer)
            web = WebServer.Web(game)
            web.start()
        if "G" in d.upper():
            print "Reloading Game Server"
            game.go = False
            reload(GameServer)
            game = GameServer.Game()
            web.parent = game
            game.start()
        time.sleep(1)
    else:
        game.go = False
        web.go = False
        # TODO close server class here
