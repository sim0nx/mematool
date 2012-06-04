#!/bin/bash

python setup.py extract_messages
#python setup.py update_catalog

for k in `find mematool/i18n -name \*.po`
do
  echo $k
  msgmerge $k mematool/i18n/mematool.pot > ${k}_
  mv ${k}_ $k
done
