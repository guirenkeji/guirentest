#!/usr/bin/bash
TIME=`date +%Y-%m-%d-%H:%M:%S`
echo $TIME >> /var/log/dockerport.log
cat /proc/net/nf_conntrack | grep 1521 | grep ESTABLISHED | sort -k 7 | awk '{print $7}' | uniq -c >>  /var/log/dockerport.log
