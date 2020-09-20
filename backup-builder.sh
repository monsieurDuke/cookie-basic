#! /bin/bash

exec_help() {
    printf "[backup-builder] : it backups your python files in this directory, to other desired directory\n"
    printf "[arguments]      : -d >> the directory of the destination path\n"
    printf "                   -o >> the directory of the origin path\n"
    printf "                   -g >> proceed to execute the backups process\n"		   
    printf "                   -h >> help. display help about backup-builder\n\n"
    printf "root Origin      : $1\n"
    printf "root Destination : $2\n\n"        
    printf "* make sure to confirm the root directory"
    printf " clear of the destination and the origin path\n"
}

missing_arg() {
	printf "[ERROR] : detecting an invalid argument\n"
    printf "          use option '-h' for more details\n\n"
    printf "root Origin      : $1\n"
    printf "root Destination : $2\n"    
	exit 1
}

exec_copy() {
	dest_path=$1
	orgn_path=$2
	cd $orgn_path
	IFS='/'
	file_name=(*)
	failed_file=()
	file_counter=${#file_name[@]}
	file_checker=true
	inc=0
	fail_inc=0

	printf "destination folder  : $dest_path\n"
	printf "origin folder       : $orgn_path\n"	
	printf "total project files : $file_counter\n"
	printf "checking available resources ($file_counter) ...\n\n"

	for i in "${file_name[@]}"
	do
		if [[ -f "$i" ]]
		then
			test_ext="$i"
			cp $i "$dest_path"
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
}

def_dest_path="/home/cookie/gitrepo/school-stuffs/"
def_orgn_path="/mnt/c/Users/Rizka/Documents/DATA/Code/"
dest_path=""
orgn_path=""

while getopts ":d:o:gh" flag
do
	case "${flag}" in
		d)
			dest_path=${OPTARG}
			;;
		o)
			orgn_path=${OPTARG}
			;;
		g)
			if [ ! -z "$dest_path" ] && [ ! -z "$orgn_path" ]
			then
				orgn_path="$def_orgn_path$orgn_path"
				dest_path="$def_dest_path$dest_path"				
				if [[ -d "$dest_path" ]] && [[ -d "$orgn_path" ]] 
				then				
					exec_copy "$dest_path" "$orgn_path"	
				else
					printf "[ERROR] : either the destination or the origin path are misstyped or doesn't exist\n"
					printf "          please verify this issue about the naming of directory\n\n"
    				printf "root Origin      : $def_orgn_path\n"
			   		printf "root Destination : $def_dest_path\n"    					
				fi					
			fi	
			;;
		h)
			exec_help "$def_orgn_path" "$def_dest_path"
			;;
		*)
			missing_arg "$def_orgn_path" "$def_dest_path"
			;;
	esac
done

