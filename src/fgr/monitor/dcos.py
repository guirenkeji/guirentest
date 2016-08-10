#!/usr/bin/python
# -*- coding: utf-8 -*- 
# author zhushaohua
# 收集数据中心mararhon和mesos的信息
import os
import json
import socket
import time
# import cx_Oracle

if __name__ == "__main__":
    db = cx_Oracle.connect('dcos/v1g2m60id2499yz@pdbdcos')
    cursor = db.cursor()
    sqls = []
    TIME = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    DATA_COLLECT_TIME = 'to_date(\'%s\',\'yyyy-mm-dd hh24:mi:ss\')' %TIME
    
    mesos_master_ip = os.popen('mesos resolve zk://10.78.182.10:2181,10.78.182.11:2181,10.78.217.10:2181,10.78.217.11:2181,10.78.216.39:2181/mesos').read().strip()
    mesos_metrics = json.loads(os.popen("curl http://%s/metrics/snapshot 2>> /dev/null" %mesos_master_ip).read())
    mesos_general_info = json.loads(os.popen("curl http://%s/state.json 2>>/dev/null" %mesos_master_ip).read())
       
    frameworksinfo = json.loads(os.popen('curl http://%s/state.json 2>>/dev/null' %mesos_master_ip).read())['frameworks']
    a = ['10.78.182.12:8080','10.78.182.12:8081','10.78.182.12:8082','10.78.182.13:8080','10.78.182.13:8081','10.78.182.13:8082','10.78.220.118:8080','10.78.220.118:8081']
    #for i in range(len(frameworksinfo)):
    for i in a:
        #marathon_ip = frameworksinfo[i]['hostname']
        marathon = json.loads(os.popen("curl -u dcosadmin:zjdcos01 http://%s/v2/apps 2>>/dev/null" %i).read())['apps']
        
        #########mesos metrics info##################################
        CLUSTER_NAME = str(mesos_general_info['cluster'])
        CLUSTER_RUNTIME_ID = int(mesos_general_info['elected_time'])
#        CPU_USED = int(cursor.execute('select sum(marathon_cpu) from marathon_current_data').fetchall()[0][0])
        CPU_USED = int(mesos_metrics['master/cpus_used'])
        CPU_TOTAL = int(mesos_metrics['master/cpus_total'])
        DISK_TOTAL = int(mesos_metrics['master/disk_total'])
        DISK_USED = int(mesos_metrics['master/disk_used'])
        MEM_TOTAL = int(mesos_metrics['master/mem_total'])
#        MEM_USED = int(cursor.execute('select sum(marathon_mem) from marathon_current_data').fetchall()[0][0])
        MEM_USED = int(mesos_metrics['master/mem_used'])
        SLAVES_INACTIVE = int(mesos_metrics['master/slaves_inactive'])
        SLAVES_CONNECTED = int(mesos_metrics['master/slaves_connected'])
        SLAVES_ACTIVE = int(mesos_metrics['master/slaves_active'])
        SLAVES_DISCONNECTED = int(mesos_metrics['master/slaves_disconnected'])
        TASKS_ERROR = int(mesos_metrics['master/tasks_error'])
        TASKS_FAILED = int(mesos_metrics['master/tasks_failed'])
#        TASKS_RUNNING = int(cursor.execute('select sum(instance_count) from marathon_current_data').fetchall()[0][0])
        TASKS_RUNNING = int(mesos_metrics['master/tasks_running'])
        TASKS_STAGING = int(mesos_metrics['master/tasks_staging'])
        
        sql1='insert into mesos_data values(%s,\'%s\',%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)'  \
        %(
            "SEQ_MESOS_DATA.NEXTVAL",
            CLUSTER_NAME,
            DATA_COLLECT_TIME,
            CPU_TOTAL,
            CPU_USED,           
            DISK_TOTAL,          
            DISK_USED,         
            MEM_TOTAL,          
            MEM_USED,          
            SLAVES_ACTIVE,       
            SLAVES_INACTIVE,     
            SLAVES_CONNECTED,    
            SLAVES_DISCONNECTED, 
            TASKS_ERROR,
            TASKS_FAILED,        
            TASKS_RUNNING,       
            TASKS_STAGING
        )
        
        sql2='update mesos_current_data set CLUSTER_NAME=\'%s\',DATA_COLLECT_TIME=%s,CPU_TOTAL=%d,CPU_USED=%d,DISK_TOTAL=%d,DISK_USED=%d,MEM_TOTAL=%d,MEM_USED=%d,SLAVES_ACTIVE=%d,SLAVES_INACTIVE=%d,SLAVES_CONNECTED=%d,SLAVES_DISCONNECTED=%d,TASKS_ERROR=%d,TASKS_FAILED=%d,TASKS_RUNNING=%d,TASKS_STAGING=%d' \
            %(
                CLUSTER_NAME,
                DATA_COLLECT_TIME,
                CPU_TOTAL,
                CPU_USED,           
                DISK_TOTAL,          
                DISK_USED,         
                MEM_TOTAL,          
                MEM_USED,          
                SLAVES_ACTIVE,       
                SLAVES_INACTIVE,
                SLAVES_CONNECTED,    
                SLAVES_DISCONNECTED, 
                TASKS_ERROR,
                TASKS_FAILED,        
                TASKS_RUNNING,       
                TASKS_STAGING
            )
        
        sqls.append(sql1)
        sqls.append(sql2)
        
        ##########marathon metrics info###############################################
        apps = cursor.execute('select app_id from marathon_current_data').fetchall()
        for i in marathon:
            app_id = i['id'].replace('/','')
            instances_count = i['instances']
            marathon_mem = i['mem'] * instances_count
            marathon_cpu = i['cpus'] * instances_count
            sql_insert = 'insert into marathon_data values(%s,%s,\'%s\',%d,%d,%d)' \
            %(
                'SEQ_MARATHON_DATA.NEXTVAL',
                DATA_COLLECT_TIME,
                app_id,
                instances_count,
                marathon_mem,
                marathon_cpu
            )
            sqls.append(sql_insert)
            if (app_id,) in apps:
                sql_update = "update marathon_current_data set DATA_COLLECT_TIME=%s,app_id=\'%s\',instance_count=%d,marathon_mem=%d,marathon_cpu=%d where app_id = \'%s\'" \
                %(
                    DATA_COLLECT_TIME,
                    app_id,
                    instances_count,
                    marathon_mem,
                    marathon_cpu,
                    app_id
                )
                sqls.append(sql_update)
            else:
                sql_insert = 'insert into marathon_current_data values(%s,\'%s\',%d,%d,%d)' \
                %(
                    DATA_COLLECT_TIME,
                    app_id,
                    instances_count,
                    marathon_mem,
                    marathon_cpu
                )                
                sqls.append(sql_insert)

    for sql in sqls:
        #print sql
        cursor.execute(sql)
    db.commit()
    db.close()
