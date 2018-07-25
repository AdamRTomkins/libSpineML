#!/bin/sh -
echo "file:"
echo "$0"

export BRAHMS_NS=/usr/lib/spineml-2-brahms/
export PATH=/home/ra/anaconda2/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/cuda-7.5/bin:/usr/local/cuda-7.5/bin
export REBUILD=false
export SYSTEMML_INSTALL_PATH

#rm /home/ra/spineml-2-brahms/temp/log/*

/usr/bin/convert_script_s2b -m ./$1/ -e 0 -w /home/ra/spineml-2-brahms -r

#touch ./data/$1/null  
#rm ./data/$1/* 
cp  /home/ra/spineml-2-brahms/temp/log/* ./data/$1/
