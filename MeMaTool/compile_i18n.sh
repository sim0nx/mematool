#!/bin/bash

for k in `find mematool/i18n -name \*.po`
do
  echo $k
  MO=`echo $k | sed "s/\.po/\.mo/"`
  msgfmt $k -o $MO
done
