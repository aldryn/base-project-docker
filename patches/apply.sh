#!/bin/bash
# patches no longer needed, since we're installing Django==1.6.11.post1 from the divio package server

#echo "Applying CVE-2015-5143"
#(cd `python -c 'import django,os; print(os.path.dirname(os.path.dirname(django.__file__)))'` && patch -p1 -i /app/patches/CVE-2015-5143/session-1.6.x.diff)

#echo "Applying CVE-2015-5144"
#(cd `python -c 'import django,os; print(os.path.dirname(os.path.dirname(django.__file__)))'` && patch -p1 -i /app/patches/CVE-2015-5144/newlines-1.6.x.diff)
