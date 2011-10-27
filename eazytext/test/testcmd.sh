#! /usr/bin bash

echo "Help text ...."
../eztext.py -h
if [ $? -gt 0 ] ; then exit $? ; fi

echo "Test -o flag ..."
../eztext.py -o out.html stdfiles/sample1.etx
if [ $? -gt 0 ] ; then exit $? ; fi

echo "Test --outfile flag ..."
../eztext.py --outfile=out.html stdfiles/sample2.etx
if [ $? -gt 0 ] ; then exit $? ; fi

echo "Test -d flag ..."
../eztext.py -d stdfiles/macro.etx
if [ $? -gt 0 ] ; then exit $? ; fi

echo "Test -s flag ..."
../eztext.py -s stdfiles/link.etx
if [ $? -gt 0 ] ; then exit $? ; fi

echo "Test -x flag ..."
../eztext.py -x stdfiles/sample2.etx
if [ $? -gt 0 ] ; then exit $? ; fi

echo "Test -a flag ..."
../eztext.py -a '["hello", "world"]' stdfiles/specialchars.etx
if [ $? -gt 0 ] ; then exit $? ; fi

echo "Test -c flag ..."
../eztext.py -c '{"key" : "value"}' stdfiles/tbl1.etx
if [ $? -gt 0 ] ; then exit $? ; fi

echo "Test -g flag ..."
../eztext.py -g 2 stdfiles/bquotes1.etx
if [ $? -gt 0 ] ; then exit $? ; fi
