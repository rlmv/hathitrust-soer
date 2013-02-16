#!/bin/bash

# Kill the rsync running in target dir w/CS if the file is too large.

while true
do
    r=`du -sm ~/Documents/CS/yale | grep -oe [0-9]*`
    echo ping $r
    if (($r > 10000)) # 10 gigs
    then
        pids=`ps -e | grep rsync | grep CS | grep -oe [0-9]*`
        kill -9 $pids
        break
    fi
    sleep 60
done