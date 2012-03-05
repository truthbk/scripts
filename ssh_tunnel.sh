#!/bin/bash

usage() {
 cat << EOF

 usage: `basename $0` [options]

 This script establishes an ssh tunnel through the hostname provided.

 OPTIONS:
   -h      Show this message
   -r      Hostname of server through which you wish to ssh tunnel
   -l      Hostname login or username
   -d      Local device you wish to activate SOCKS proxy for.
   -p      Port through which you wish to tunnel (default: 8080)
   -x      Disable ssh tunnel and proxy configuration
EOF
}

USERNAME=
HOSTNAME=
DEVICE=
DISABLE=
PORT=8080
ISMAC=0

if [ $(uname)=="Darwin" ]; then
	ISMAC=1
fi

while getopts ":l:r:d:p:hx" opt; do
    case $opt in
     l)
        USERNAME=$OPTARG
        ;;
     d)
        DEVICE=$OPTARG
        ;;
     r)
	HOSTNAME=$OPTARG
        ;;
     x)
	DISABLE=1
        ;;
     p)
	PORT=$OPTARG
        ;;
     h)
	usage
	exit 0
        ;;
    \?)
        usage
        exit 1
      ;;
  esac
done


if [[ -z $DEVICE ]]
then
    echo "Error: No network device specified.\n"
    usage
    exit 1
fi

if [[ $DISABLE -eq 1 ]];
then
    echo 'disabling ssh tunnel, and SOCKS proxy.'
    if [[ 1 -eq $ISMAC ]];
    then
        networksetup -setsocksfirewallproxystate $DEVICE off
    fi

    kill -9 $(ps aux |grep 'ssh -D 8080 -f -C -q -N' | grep -v 'grep' | head -n1 | awk '{ print $2 }')
    exit 0
fi

if [[ $DISABLE -eq 1 ]];
then
    echo 'disabling ssh tunnel, and SOCKS proxy.'
    if [ 1 -eq $ISMAC ];
    then
        networksetup -setsocksfirewallproxystate $DEVICE off
    fi

    killall ssh
    exit 0
fi

if [[ -z $USERNAME ]] || [[ -z $HOSTNAME ]] 
then
     echo "Error: Hostname and username must be specified.\n"
     usage
     exit 1
fi

echo 'creating ssh tunnel...'
ssh -D $PORT -f -C -q -N $USERNAME@$HOSTNAME
if [ 0 -eq $? ]; 
then
	echo 'ssh tunnel create succesfully.'
else
	echo 'host down or wrong password.'
	exit 1
fi

if [ 1 -eq $ISMAC ];
then
	networksetup -setsocksfirewallproxy $DEVICE 127.0.0.1 $PORT off
fi
echo "SOCKS proxy activated succesfully on device: $DEVICE"
exit 0
