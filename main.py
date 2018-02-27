import time

import Server

if __name__ == "__main__":
    go = True
    while go:
        try:
            d = raw_input("(Q)uit, (W)ebserver\n")
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
        time.sleep(1)
    else:
        pass
        # TODO close server class here
