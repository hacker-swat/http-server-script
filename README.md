# HTTP-file-share

This script is a HTTP server that allows you to serve either HTTP or HTTPS traffic. It offers the following features:

## Features
- Prints the URLs of all the files and folders in the current directory
- Ability to generate SSL certificate and key files
- Serves either HTTP or HTTPS traffic

## Getting Started

### Prerequisites
- Python3 must be installed on the machine

### Installation
1. Clone this repository
2. Add the script directory to the system's PATH environment variable to run the script from any directory
3. Run the script with the desired arguments

### Usage
```sh
python http-server.py -H <hostname> -p <port> -P <protocol> -c <certificate> -k <key> -gs <generate_ssl>
```
### Default Network Interface
If no hostname or IP address is specified, the script will automatically select the last network interface that was connected as the default.

![Screenshot](https://github.com/hackerswat/http-server-script/blob/main/Screenshot.jpg)
