#!/bin/bash

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

script_location='/usr/share/http-file-share'

mkdir $script_location

cp ./http_server.py ./README.md $script_location

py=$(which python3)

echo -e "#!/bin/bash \n$py $script_location/http_server.py $@" > "/usr/local/bin/httpserver"

chmod 755  /usr/local/bin/httpserver

