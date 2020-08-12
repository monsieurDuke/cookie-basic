#!/bin/bash

missing_arg() {
	printf "[ERROR] : detecting an invalid argument\n"
    printf "          use option '-h' for more details\n"
	exit 1
}

exec_copy() {
	dest_dir=$1
	if [[ -d $dest_dir ]]
	then
		cd cookie-basic/
		IFS='/'
		file_name=(*.py)
		failed_file=()
		file_counter=${#file_name[@]}
		file_checker=true
		inc=0
		fail_inc=0

		printf "total project files : $file_counter\n"
		printf "destination folder  : $dest_dir\n"
		printf "checking available resources ($file_counter) ...\n\n"
		for i in "${file_name[@]}"
		do
			if [[ -f "$i" ]]
			then
				test_ext="test_$i"
				cp $i "$dest_dir$test_ext"
				inc=$((inc+1))
				printf "$inc"
				printf " - $i >> $test_ext\n"
			else
				failed_file[$fail_inc]=$i
				fail_inc=$((fail_inc+1))
			fi
		done
		printf "\n[NICE]: copying files successfully ($inc/$file_counter) ..."
		if [[ $inc<$file_counter ]]
		then
			file_checker=false
		fi
		if [[ $file_checker == false ]]
		then
			printf "\n[FAIL]: failed to copy ["
			for j in "${failed_file[@]}"
			do
				printf " $j "
			done
			printf "] to destination folder\n"
			printf "        issued file are not found in this directory\n"
		fi
		printf "\n"
	else
		printf "[ERROR] : destination path are either misstyped or not exist\n"
		printf "          please verify this issue about the naming of directory\n"
	fi
}

dest_dir="$PWD/../container/"
while getopts ":f:c:h" flag
do
	case "${flag}" in
		f) dest_dir=${OPTARG}
           exec_copy $dest_dir
		   exit 0 ;;
		c) dest_dir="$PWD/${OPTARG}"
		   exec_copy $dest_dir
           exit 0 ;;
		h) printf "[backup-builder] : it backups your python files in this directory, to other desired directory\n"
		   printf "[arguments]      : -f >> full path. require a full path to the directory / folder\n"
		   printf "                   -c >> current path. require a folder name within this directory\n"
		   printf "                   -h >> help. display help about backup-builder\n"
           exit 0 ;;
		*) missing_arg
	esac
done

missing_arg
