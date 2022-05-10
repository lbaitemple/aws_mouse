#!/usr/bin/env bash

if [ $# -eq 1 ]; then
   if [ $1 = "backup" ]; then
      dir=`pwd`"/install/img_recognition/share/img_recognition/"
      dir1=${dir}"param"
      cmd=`cp -rf ${dir1} ${dir1}.bak`
      dir2=${dir}"model"
      cmd=`cp -rf ${dir2} ${dir2}.bak`
   elif [ $1 = "restore" ]; then 
      dir=`pwd`"/install/img_recognition/share/img_recognition/"
      dir1=${dir}"param"
      cmd=`cp -rf ${dir1}.bak ${dir1}`
      dir2=${dir}"model"
      cmd=`cp -rf ${dir2}.bak ${dir2}`
   else
      echo "$0 [backup|restore]"
   fi
else
   echo "$0 [backup|restore]"
fi


