# http-server-script

This script is a HTTP server that can serve either HTTP or HTTPS (with SSL ) traffic. 

## Features
- Can serve either HTTP or HTTPS traffic
- Can generate SSL certificate and key files
- Print the URLs of all the files and folders in the current directory

## Getting Started

### Prerequisites
- Python3 should be installed on the machine
- It is recommended to add the script directory to the system's PATH environment variable so that the script can be run from any directory 

### Installing
- Clone this repository
- Run the script with the desired arguments

### Usage
```sh
python http-server.py -H <hostname> -p <port> -P <protocol> -c <certificate> -k <key> -gs <generate_ssl>
```
### Default Network Interface
If no hostname or IP address is specified, the script will automatically choose the last network interface that connected

![Screenshot](https://github.com/hackerswat/http-server-script/blob/main/Screenshot.jpg)
