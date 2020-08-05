#!/bin/bash

IFS='/'
file_name=(*.py)
failed_file=()
dest_dir="$PWD/container/"
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

