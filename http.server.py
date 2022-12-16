import http.server
import socketserver
from os import walk
import os
import sys

Port = 8000
interface="tun0"

ip = os.popen('ifconfig ' + interface + ''' | grep "inet" | grep "netmask" |tr -s ' ' | cut -d ' ' -f 3 | ''' + "sed 's/ //g'")
ip=ip.read().strip()

files = []
for (dirpath, dirnames, filenames) in walk("."):
    files.extend(filenames)
    break

for x in files:
    print("http://" + str(ip) + ":" + str(Port) + "/" + x)

import sys, traceback

def main():
    try:
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", Port), Handler) as httpd:
            print("serving at port", Port)
            httpd.serve_forever()

    except KeyboardInterrupt:
        print ("Shutdown requested...exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)

if __name__ == "__main__":
    main()