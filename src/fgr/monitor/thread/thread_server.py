#!/usr/bin/python
import os
# import cx_Oracle
import time

def gettime():
    TIME1 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return TIME1

def logging(context):
    filename = '/var/log/ContainerToOracle.log'
    fd = file(filename,'a')
    TIME = gettime()
    context = str(context)
    loginfo = '%s %s' %(TIME,context)
    fd.write(loginfo)
    fd.write('\n')
    fd.close()

def autoScale():
    ts = time.strftime("%Y%m%d%H%M%S",time.localtime())
    DATA_COLLECT_TIME = 'to_date(\'%s\',\'yyyy-mm-dd hh24:mi:ss\')' %ts
    web_thread_number = cursor.execute('select SUM(container_thread_run) from container_current_data where container_type=\'sjyyt-web\'').fetchall()
    app_thread_number = cursor.execute('select SUM(container_thread_run) from container_current_data where container_type=\'sjyyt-app\'').fetchall()
    command1 = 'curl -u dcosadmin:zjdcos01 -i http://10.78.178.57:5000/v1.0/dcos -H "Content-Type: application/json" -X POST -d \'{"app_id":"sjyyt-web","type":"thread","value":%d,"time":\"%s\"}\'' %(int(web_thread_number[0][0]),ts)
    command2 = 'curl -u dcosadmin:zjdcos01 -i http://10.78.178.57:5000/v1.0/dcos -H "Content-Type: application/json" -X POST -d \'{"app_id":"sjyyt-app","type":"thread","value":%d,"time":\"%s\"}\'' %(int(app_thread_number[0][0]),ts) 
    sqlweb = 'insert into container_thread_history values(%s,\'sjyyt-web\',%d,%s)' %(DATA_COLLECT_TIME,int(web_thread_number[0][0]),"SEQ_TOTAL_THREAD.NEXTVAL")
    sqlapp = 'insert into container_thread_history values(%s,\'sjyyt-app\',%d,%s)' %(DATA_COLLECT_TIME,int(app_thread_number[0][0]),"SEQ_TOTAL_THREAD.NEXTVAL")
    logging(command1)
    logging(command2)
    os.system(command1)
    os.system(command2)
#    cursor.execute(sqlweb)
#    cursor.execute(sqlapp)
#    db.commit()

def getthreadinfo():
    psshinfo = os.popen("pssh -h /etc/dcos/slave -t 400  -i \"python /data/dcos/dcos/bin/thread-client.py\"").read().strip().splitlines()
    threadinfo = []
    for count in range(len(psshinfo)):
        if psshinfo[count].count('SUCCESS'):
            pass
        elif psshinfo[count].count('FAILURE'):
            pass
        else:
            threadinfo.append(psshinfo[count])
    return  threadinfo

def parasesql():
    sqls=[]
    threadinfo = getthreadinfo()
    alarm_container = cursor.execute('select container_name from container_alarm_data').fetchall()
    cursor.execute('truncate table container_current_data')
    for info in threadinfo:
        splitinfo = info.split()
        container_name = splitinfo[0]
        TIME2 = gettime()
        DATA_COLLECT_TIME = 'to_date(\'%s\',\'yyyy-mm-dd hh24:mi:ss\')' %TIME2
        sql1 = 'insert into container_current_data values(\'%s\',\'%s\',%s,\'%s\',%s,%s,%d,%s,%s,%s,%s)'\
         %(
                splitinfo[0],
                splitinfo[1],
                DATA_COLLECT_TIME,
                splitinfo[3],
                splitinfo[4],
                splitinfo[5],
                int(splitinfo[6]),
                splitinfo[7],
                splitinfo[8],
                splitinfo[9],
                splitinfo[10]
         )
        sqls.append(sql1)
        if (int(splitinfo[9]) > 50 or int(splitinfo[9]) == 0 and (splitinfo[1],) not in alarm_container):
            alarm_times = 0
            sql2 = 'insert into container_alarm_data values(\'%s\',\'%s\',%s,\'%s\',%s,%d,%s)'\
             %(
                    splitinfo[0],
                    splitinfo[1],
                    DATA_COLLECT_TIME,
                    splitinfo[3],
                    splitinfo[4],
                    alarm_times,
                    splitinfo[9],
             )
            sqls.append(sql2)
        elif (int(splitinfo[9]) > 50 or int(splitinfo[9]) == 0 and (splitinfo[1],) in alarm_container):
            alarm_times = cursor.execute('select alarm_time from container_alarm_data where container_name = \'%s\'' %splitinfo[1]).fetchall()[0][0] + 1
            sql2 = 'update container_alarm_data set alarm_time=%d,container_thread_run=%d where container_name = \'%s\'' %(int(alarm_times),int(splitinfo[9]),splitinfo[1])
            sqls.append(sql2)
    logging(sqls)
    return sqls

def insertdata():
    sqls = parasesql()
    for i in sqls:
        cursor.execute(i)
    cursor.execute('insert into container_history_data select * from container_current_data')
    db.commit()
    
def storeThreadHistory():
    ts = time.strftime("%Y%m%d%H%M%S",time.localtime())
    DATA_COLLECT_TIME = 'to_date(\'%s\',\'yyyy-mm-dd hh24:mi:ss\')' %ts
    totalThreadInfo = cursor.execute("select container_type,SUM(container_thread_run) from container_current_data group by container_type").fetchall()
    for i in totalThreadInfo:
        containerType = i[0]
        totalThread = i[1]
        sql = "insert into container_thread_history values(%s,\'%s\',%d,%s)" %(DATA_COLLECT_TIME,containerType,int(totalThread),"SEQ_TOTAL_THREAD.NEXTVAL")
        cursor.execute(sql)
    db.commit()

        
if __name__ == "__main__": 
#     db = cx_Oracle.connect('dcos/v1g2m60id2499yz@pdbdcos')
    cursor = db.cursor()
    insertdata() 
    autoScale()
    storeThreadHistory()
    db.close()
