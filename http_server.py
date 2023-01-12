import http.server
import ssl
import argparse
import socket
import os


def run_server(host, port, protocol, certificate, key):
    server_address = (host, port)
    if protocol == "https":
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certificate, keyfile=key, server_side=True)
        print(f"Serving HTTPS on {host}:{port}...")
        listdirs(host, port, protocol)
    else:
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
        print(f"Serving HTTP on {host}:{port}...")
        listdirs(host, port, protocol)
    httpd.serve_forever()
    
def do_checks(host, port, protocol, certificate, key,generate_ssl):
    if generate_ssl==True:
        print("Not available (future update) in the meantime run the command")
        print("openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365")

    def linNetInfo(host):
        interface_names = []
        for index, name in socket.if_nameindex():
            interface_names.append(name)
        netinfo={}
        for interface in interface_names:
            i = os.popen('ifconfig ' + interface + ''' | grep "inet" | grep "netmask" |tr -s ' ' | cut -d ' ' -f 3 | ''' + "sed 's/ //g'")
            netinfo[interface] = i.read().strip() 
        try:
            host = netinfo[host]
        except:
            if host not in netinfo.values():
                host = list(netinfo.values())[-1]
        return host
    def winNetInfo(host):
        iplist= []
        for ip in socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET):   
            iplist.append(ip[4][0])
        if host not in iplist:
            host = iplist[-1]
        return host
    
    if os.name == "nt":
        host = winNetInfo(host)
    else:
        host = linNetInfo(host)

    if port not in range(1, 65535):
        raise ValueError("invalid port")
    
    protocol = protocol.lower()
    if protocol != "http" and protocol != "https": 
        raise ValueError("invalid protocol")
    if protocol == "https":
        if certificate == "":
            raise ValueError("invalid certificate")
        if key == "":
            raise ValueError("invalid key")
    return host, port, protocol, certificate, key

def listdirs(host, port, protocol):
    files = []
    folders=next(os.walk('.'))[1]
    for (dirpath, dirnames, filenames) in os.walk("."):
        files.extend(filenames)
        break
        
    if protocol == "https": 
        for x in folders:
            print("https://" + str(host) + ":" + str(port) + "/" + x +"/")

        for x in files: 
            print("https://" + str(host) + ":" + str(port) + "/" + x)

    else: 
        for x in folders:
            print("http://" + str(host) + ":" + str(port) + "/" + x +"/")

        for x in files: 
            print("http://" + str(host) + ":" + str(port) + "/" + x)
 
    if ".ssh" in folders :
        print('''
      ____            _   _                         _       _       _          _                 
     / ___|__ _ _   _| |_(_) ___  _ __      ___ ___| |__   (_)___  (_)_ __    | |__   ___ _ __ ___                                       
    | |   / _` | | | | __| |/ _ \| '_ \    / __/ __| '_ \  | / __| | | '_ \   | '_ \ / _ \ '__/ _ \                                   
    | |__| (_| | |_| | |_| | (_) | | | |  _\__ \__ \ | | | | \__ \ | | | | |  | | | |  __/ | |  __/                      
     \____\__,_|\__,_|\__|_|\___/|_| |_| (_)___/___/_| |_| |_|___/ |_|_| |_|  |_| |_|\___|_|  \___|
        ''')


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Run a HTTP file server")
        parser.add_argument("--host", type=str, default="", help="hostname/ip to listen on")
        parser.add_argument("--port", type=int, default=8000, help="port number to listen on (default set to 8000)")
        parser.add_argument("--protocol", type=str,default="http", help="Protocol to use (http or https)")
        parser.add_argument("--certificate", type=str, default="", help="https certificate.pem")
        parser.add_argument("--key", type=str, default="", help="https private key.pem")
        parser.add_argument("--generate-ssl" ,default="False" ,action='store_true',help="generate https server certificate")
        args = parser.parse_args()
        

        i = do_checks(args.host, args.port, args.protocol,args.certificate,args.key,args.generate_ssl)
        
        run_server(i[0], i[1], i[2],i[3],i[4])

    except KeyboardInterrupt:
        print ("\nShutdown requested...exiting")
