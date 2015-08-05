#!/bin/bash

# Runs all scripts in the /migrate/* folder
set -e

for SCRIPT in /migrate/*.sh
	do
		if [ -f $SCRIPT -a -x $SCRIPT ]
		then
			echo " ---->  Running $SCRIPT..."
			$SCRIPT
			echo " <----  Done $SCRIPT"
		fi
	done
