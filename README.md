# http-server-script

This script runs a HTTP or HTTPS server using the built-in Python libraries http.server and ssl.

It takes 5 arguments: host, port, protocol, certificate and key.

It starts the server on the specified host and port, using the specified protocol (either "http" or "https"). If "https" is specified, it uses the provided certificate and key files to wrap the socket in SSL/TLS.

It also has some helper functions to check and return the valid host, port, protocol, certificate and key.

It also has a function listdirs which list all the folders and files in the directory which is being served.

It prints the URLs of all files and folders in the directory being served, with "http" or "https" depending on the specified protocol.

It also has a function to generate SSL cert and key in case if not provided.

![The San Juan Mountains are beautiful!](/assets/images/san-juan-mountains.jpg "San Juan Mountains")
![Screenshot](https://github.com/hackerswat/http-server-script/blob/main/Screenshot.jpg)
