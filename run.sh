SRC=$1
DST=$2
for i in `seq ${SRC} ${DST}`
do
  python Main.py ${i} 
done
