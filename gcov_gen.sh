#!/bin/bash

usage() {
	echo "usage: `basename $0` [options]"
	echo -e "\tThis script generates gcov coverage reports.\n"
	echo -e "Options:"
	echo -e "\t-d DIR\t: Indicate project dir.\n\n"
	echo -e "\t-b\t: generate baseline info (Call before running tests)."
	echo -e "\t-t\t: generate total info (Call after running tests)."
	echo -e "\t-r DIR\t: generate HTML reports and place in specified DIR(Call after running tests).\n\n"
	echo -e "\t-c\t: clean all gcov files in project dir."
	echo -e "\t-q\t: Quiet."
	echo -e "\t-h\t: Show this help message.\n\n"
}


ERRORS=0
CLEAN=
QUIET=
BASELINE=
TOTAL=
HTML=
HTMLDIR=
PJDIR=.
while getopts "hcbtqr:d:" OPTION
do
	case $OPTION in
		h)
			usage
			exit 1
			;;
		c)
			CLEAN=1
			;;
		q)
			QUIET=1
			;;
		d)
			PJDIR=$OPTARG
			;;
		b)
			BASELINE=1
			;;
		t)
			TOTAL=1
			;;
		r)
			HTML=1
			HTMLDIR=$OPTARG
			;;
		?)
			usage
			exit
			;;
	esac
done


if [[ -z $BASELINE ]] && [[ -z $TOTAL ]] && [[ -z $HTML ]] && [[ -z $CLEAN ]]; 
then
	echo -e "No appropriate option flag passed!\n"
	usage
	exit 1
fi

if [[ $BASELINE == 1 ]];
then
	echo "Generating baseline info files..."
	for i in $(find $PJDIR -maxdepth 1 -type d | awk '{ if (NR != 1) { print } }' | sed 's/\.\///');
	do
		if [[ ! -z $QUIET ]];
		then
			lcov -c -i -d $PJDIR/$i -o ${i}_baseline.info >/dev/null 2>&1
		else
			lcov -c -i -d $PJDIR/$i -o ${i}_baseline.info
		fi
	done
	echo "You may now run your regression."
	exit 0;
fi


if [[ $TOTAL == 1 ]];
then
	echo "Generating test info and gcov files..."
	for i in $(find $PJDIR -maxdepth 1 -type d | awk '{ if (NR != 1) { print } }' | sed 's/\.\///');
	do
		if [[ ! -z $QUIET ]];
		then
			lcov -c -d $PJDIR/$i -o $PJDIR/${i}_test.info >/dev/null 2>&1
			lcov -a $PJDIR/${i}_baseline.info -a $PJDIR/${i}_test.info -o $PJDIR/${i}_total.info >/dev/null 2>&1
		else
			lcov -c -d $PJDIR/$i -o $PJDIR/${i}_test.info
			lcov -a $PJDIR/${i}_baseline.info -a $PJDIR/${i}_test.info -o $PJDIR/${i}_total.info
		fi

		if [[ ! -z $? ]];
		then
			ERRORS=1
		fi
	done
fi

if [[ $HTML == 1 ]];
then
	echo "Generating html reports..."
	for i in $(find $PJDIR -maxdepth 1 -type d | awk '{ if (NR != 1) { print } }' | sed 's/\.\///');
	do
		if [[ -e $PJDIR/${i}_total.info ]];
		then
			mkdir -p $HTMLDIR/${i}
			if [[ ! -z $QUIET ]];
			then
				genhtml -o $HTMLDIR/${i} $PJDIR/${i}_total.info >/dev/null 2>&1
			else
				genhtml -o $HTMLDIR/${i} $PJDIR/${i}_total.info
			fi

			if [[ ! -z $? ]];
			then
				ERRORS=1
			fi
		fi
	done
fi

if [[ $CLEAN == 1 ]];
then
	echo "Removing info files..."
	rm $PJDIR/*_baseline.info
	rm $PJDIR/*_test.info
	rm $PJDIR/*_total.info
	echo "Removing gcda files..."
	find $PJDIR -type f -name "*.gcda" -exec rm -f {} \;
fi

if [[ ! -z $ERRORS ]];
then
	echo -e "\033[1mWARNING\033[0m:\tScript completed succesfully but there were non-critical errors."
	if [[ $QUIET == 1 ]];
	then
		echo -e "\t\tconsider running the script in verbose (non-quiet) mode."
	fi
fi
