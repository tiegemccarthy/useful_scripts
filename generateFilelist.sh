#!/bin/bash

# A fairly simple bash script for generating station filelists.

# Help message and usage information
HelpMessage()
{
   # Display Help
    echo
    echo "Usage: ~/generateFilelist.sh <experiment_name> <station_code> <data_location> <datastreams_option> <data_format> "
    echo "e.g. ~/generateFilelist.sh aua093 Hb /mnt/vbs4 1 1"
    echo
    echo "Valid datastream options are:"
    echo "0 : standard single datastream (typically useful for legacy stations)."
    echo "1 : Mixed-mode UTAS stations, 4 data streams labelled as XX, XY, SX and SY."
    echo "2 : VGOS stations, 8 data streams, labelled A through H."
    echo
    echo "Valid data format options are:" 
    echo "0 : Mark5 data format"
    echo "1 : VDIF data format"
    echo
}

## TO-DO ########################################

# 1. Bake in some defaults
# 2. Replace vsum.gappy.py script call with some bash code (might be very messy - probably smoother to use python for everything in that case)

##################################################
# get options
while getopts ":h" option; 
do
   case $option in
      h) # display Help
         HelpMessage
         exit;;
     \?) # incorrect option
         echo "Error: Invalid option, use '-h' to print usage information."
         exit;;
   esac
done
# setup variables for clarity
experiment=${1:?"Please specify an experiment name (as displayed on data files)"}
station=${2:?"Please specify a station!"}
data_location=${3:?"Please specify a data location!"}
datastream_option=${4:?"Please specify what datastreams are required - use 0 for standard, 1 for mixed-mode and 2 for 8 stream VGOS."}
data_format=${5:?"Please specify data format - use 0 for Mark5 and 1 for VDIF"}
# Determine what datastreams need to have filelists generated
if [ $datastream_option == 0 ]; then
	datastream_list="N/A"
	echo "Standard mode - A single datastream will be produced."
elif [ $datastream_option == 1 ]; then
	datastream_list="xx xy sx sy"
	echo "Mixed mode - 4 datastreams will be produced (XX, XY, SX, SY)"
elif [ $datastream_option == 2 ]; then
	datastream_list="a b c d e f g h"
	echo "VGOS mode - 8 datastreams will be produced (A, B, C, D, E, F, G, H)"
else 
	echo "Invalid value for datastream mode - use 0 for standard, 1 for mixed-mode and 2 for 8 datastream VGOS"
fi

# Determine whether to use vsum or m5bsum where relevant
if [ $data_format == 0 ]; then
	program="m5bsum"
else
	program="vsum"
fi

# Generate the filelists
if [ $datastream_option == 0 ]; then
	for i in $(ls $data_location/*${experiment}*${station,,}*); do $program -s $i; done > ${station,,}.filelist
else
    for x in $datastream_list; do for i in $(ls $data_location/*${experiment}*${station,,}*_$x*); do ~/vsum.gappy.py $i VDIF_8000-1024-8-2; done > ${station,,}${x^^}.filelist; done
fi
