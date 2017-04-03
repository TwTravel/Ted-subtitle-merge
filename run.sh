#!/bin/sh
SRC=$1
DST=$2
TYPE=$3

for i in `seq ${SRC} ${DST}`
do
  python Main.py ${i} ${TYPE}
done
