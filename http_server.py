import http.server
import ssl
import argparse
import socket
import os

def run_server(host, port, protocol, certificate, key):
    server_address = (host, port)
    if protocol == "https":
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=certificate, keyfile=key)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"Serving HTTPS on {host}:{port}...")
        listdirs(host, port, protocol)
    else:
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
        print(f"Serving HTTP on {host}:{port}...")
        listdirs(host, port, protocol)
    httpd.serve_forever()
    
def do_checks(host, port, protocol, certificate, key,generate_ssl):
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
    
    if generate_ssl == "True":
        generatessl(host)
    
    protocol = protocol.lower()
    if protocol != "http" and protocol != "https": 
        raise ValueError("invalid protocol")
    if protocol == "https":
        if certificate == "":
            if os.path.exists(host+".crt"):
                certificate = str("./" + host+".crt")
            else:
                raise ValueError("invalid certificate")
        if key == "":    
            if os.path.exists(host+".key"):
                    key = str("./" + host +".key")
            else:
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
    print("\n")

def generatessl(host):
    try:
        from OpenSSL import crypto
    except:
        raise ValueError("\nplease install openssl library\npip install pyopenssl")
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    cert = crypto.X509()
    cert.get_subject().C = "NA"
    cert.get_subject().ST = "NA"
    cert.get_subject().L = "NA"
    cert.get_subject().O = "NA"
    cert.get_subject().OU = "NA"
    cert.get_subject().CN = host
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(315360000)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    open("{}.key".format(host), "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    open("{}.crt".format(host), "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    certificate = "{}.crt".format(host)
    key = "{}.key".format(host)
    print("Certificate generated")   

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Run a simple HTTP file server")
        parser.add_argument("-H","--host", type=str, default="", help="hostname to listen on")
        parser.add_argument("-p", "--port", type=int, default=8000, help="port number to listen on (default set to 8000)")
        parser.add_argument("-P","--protocol", type=str,default="http", help="Protocol to use (http or https)")
        parser.add_argument("-c","--certificate", type=str, default="", help="https certificate.pem")
        parser.add_argument("-k","--key", type=str, default="", help="https private key.pem")
        parser.add_argument("-gs","--generate-ssl" ,action='store_true',help="generate https server certificate")
        args = parser.parse_args()
        

        i = do_checks(args.host, args.port, args.protocol,args.certificate,args.key,str(args.generate_ssl))
        

        run_server(i[0], i[1], i[2],i[3],i[4])


    except KeyboardInterrupt:
        print ("\nShutdown requested...exiting")
