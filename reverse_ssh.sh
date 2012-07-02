#!/bin/bash

usage() {
	echo "usage: `basename $0` [options]"
	echo -e "\tThis script generates reverse ssh tunnels.\n"
	echo -e "Options:"
	echo -e "\t-c\t: check for existing reverse tunnel to remote host."
	echo -e "\t-k\t: kill all reverse tunnels to remote host."
	echo -e "\t-p PORT\t: remote port for reverse SSH tunnel.\n"
	echo -e "\t-r HOSTNAME: remote hostname for reverse SSH tunnel.\n"
	echo -e "\t-u USERNAME: remote username for reverse tunnel."
	echo -e "\t-h\t: Show this help message.\n\n"
}

CHECK=
REMOTE=
PID=
KILL=
USER=$(whoami)
PORT=19999

while getopts "hckr:p:u:" OPTION
do
	case $OPTION in
		h)
			usage
			exit 1
			;;
		c)
			CHECK=1
			;;
		k)
			KILL=1
			;;
		p)
			PORT=$OPTARG
			;;
		r)
			REMOTE=$OPTARG
			;;
		u)
			USER=$OPTARG
			;;
		?)
			usage
			exit
			;;
	esac
done

if [[ -z $REMOTE ]];
then
	echo "You must specify a remote ssh tunnel source."
	usage
	exit 1;
fi

if [[ ! -z $KILL ]];
then
	for PID in `ps -ef | grep "ssh" | grep "\-R" | grep "$REMOTE" | awk '{ print $2 }'`;
	do
		kill $PID
	done
	exit 0;
fi

if [[ ! -z $CHECK ]];
then
	ps -ef | grep "ssh" | grep "\-R" | grep "$REMOTE" >/dev/null 2>&1
	if [[ $? -eq 0 ]];
	then
		echo "Reverse tunnel already in place."
		exit 0;
	fi
fi

# this will run in background creating a reverse tunnel.
ssh -nNT -f -R $PORT:localhost:22 $USER@$REMOTE
exit 0;



