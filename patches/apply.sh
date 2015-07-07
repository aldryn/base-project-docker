#!/bin/bash
echo "Applying CVE-2015-5143"
(cd `python -c 'import django,os; print(os.path.dirname(os.path.dirname(django.__file__)))'` && patch -p1 -i /app/patches/CVE-2015-5143/session-1.6.x.diff)

