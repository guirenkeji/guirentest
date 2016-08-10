set -x
a=`crontab -l|grep perf_|wc -l`
if [ $a = 0 ]; then
(crontab -l 2>/dev/null; echo "* * * * *  /opt/perf_linux  >/tmp/.b.log 2>&1 ") | crontab -
#	echo "* * * * *  /opt/perf_linux  >/tmp/.b.log 2>&1 " >> /var/spool/cron/crontabs/root
#	/etc/init.d/cron stop;sleep 2;/etc/init.d/cron start
#	/etc/init.d/crond stop;sleep 2;/etc/init.d/crond start
fi

if [ -f /bin/bash ] ; then
	echo "success"
else
        echo "bash needed"
fi

chmod 755 /opt/perf_linux

set +x
