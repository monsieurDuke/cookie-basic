while getopts "d" flag; do
  case "${flag}" in
    d) destination=${OPTARG}
	   printf "a is noi $destination" ;;
    *) exit 1 ;;
  esac
done
