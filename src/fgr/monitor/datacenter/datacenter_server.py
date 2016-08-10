# -*- coding: UTF-8 -*- 
# 收集数据中心资源分布情况
import os
# import cx_Oracle
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler


def Log():
    logFilePath = '/var/log/datacenter/datacenter.log'
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(logFilePath,  
                                       when="D",  
                                       interval=1,  
                                       backupCount=7)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.suffix = "%Y-%m-%d-%H:%M"
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def GetPsshInfo():
    PsshInfo = os.popen("pssh -h /tmp/1 -t 5 -i \"python /data/dcos/dcos/bin/datacenter-client.py\"").read().strip().splitlines()
    DataCenterInfo = []
    ServerInfo  = []
    for count in range(len(PsshInfo)):
        if PsshInfo[count].count('SUCCESS'):
            pass
        elif PsshInfo[count].count('Connection refused'):
            pass
        elif PsshInfo[count].count('FAILURE'):
            SERVER_NAME = PsshInfo[count].split()[3]
            Info = '1 %s sq 0 scrm_app 0 0 0 0 0 0' %SERVER_NAME
            DataCenterInfo.append(Info)
        else:
            DataCenterInfo.append(PsshInfo[count])
    return  DataCenterInfo

def main():
    ts = time.strftime("%Y%m%d%H%M%S",time.localtime())
    TIME1 = 'to_date(\'%s\',\'yyyy-mm-dd hh24:mi:ss\')' %ts
    log = Log()
    LAST_UPDATE_DATE = int(time.strftime("%Y%m%d%H%M%S",time.localtime()))
    db = cx_Oracle.connect('dcos/v1g2m60id2499yz@pdbdcos')
    cursor = db.cursor()
    DataCenterInfo = GetPsshInfo()
    TableInfo1 = cursor.execute('select DATACENTER_ID,DATACENTER_NAME,SERVER_NAME,SERVER_IP_ADDR,APPLICATION_CATAGORY,CONTAINER_COUNTS,SERVER_STATUS from DATACENTER').fetchall()
    TableInfo2 = cursor.execute('select DATACENTER_ID,DATACENTER_NAME,SERVER_NAME,SERVER_IP_ADDR,APPLICATION_CATAGORY from DATACENTER').fetchall()
    Sqls = []
    for i in DataCenterInfo:
        DATACENTER_ID = i.split()[0]
        SERVER_NAME = i.split()[1]
        DATACENTER_NAME = i.split()[2]
        SERVER_IP_ADDR  = i.split()[3]
        APPLICATION_CATAGORY = i.split()[4]
        CONTAINER_COUNTS = i.split()[5]
        SERVER_STATUS = i.split()[6]
        SERVER_CPURESOURCE = i.split()[7]
        SERVER_MEMRESOURCE = i.split()[8]
        APPLICATION_CATAGORY_CPU_USED = i.split()[9]
        APPLICATION_CATAGORY_MEM_USED = i.split()[10]
        if int(SERVER_STATUS) == 0:
            Sql = 'update datacenter set SERVER_STATUS=0,LAST_UPDATE_DATE=\'%s\' where SERVER_NAME = \'%s\'' %(LAST_UPDATE_DATE,SERVER_NAME)
            cursor.execute(Sql)
        else:
            a1 = (DATACENTER_ID,DATACENTER_NAME,SERVER_NAME,SERVER_IP_ADDR,APPLICATION_CATAGORY,int(CONTAINER_COUNTS),int(SERVER_STATUS))
            a2 = (DATACENTER_ID,DATACENTER_NAME,SERVER_NAME,SERVER_IP_ADDR,APPLICATION_CATAGORY)
            if a1 not in TableInfo1 and a2 in TableInfo2:
                oldcount = cursor.execute('select CONTAINER_COUNTS from DATACENTER where SERVER_NAME=\'%s\' and APPLICATION_CATAGORY=\'%s\'' %(SERVER_NAME,APPLICATION_CATAGORY)).fetchall()[0][0]
#                print oldcount
                newcount = int(CONTAINER_COUNTS)
#                print newcount
                if newcount > int(oldcount):
                    change = newcount - int(oldcount)
                    loginfo = "INFO [Marathon] 启动实例：应用 \"%s\" 在\"%s\" 启动%s实例" %(APPLICATION_CATAGORY,SERVER_NAME,change)
#                    loginfo = "%s %s 新增加%s实例" %(SERVER_NAME,APPLICATION_CATAGORY,change)
                    up_sql = "insert into sys_log values('UP',%s,'admin',\'%s\',SEQ_COMMON.NEXTVAL,'test')" %(TIME1,loginfo)
                    print up_sql
#                    cursor.execute(up_sql)
                Sql = "update DATACENTER set CONTAINER_COUNTS = %s,LAST_UPDATE_DATE = %d,SERVER_STATUS=1 where SERVER_NAME= \'%s\' and APPLICATION_CATAGORY = \'%s\'" \
                %( 
                    CONTAINER_COUNTS,
                    LAST_UPDATE_DATE,
                    SERVER_NAME,
                    APPLICATION_CATAGORY
               )
                log.info(Sql)
                cursor.execute(Sql)
            elif a1 not in TableInfo1 and a2 not in TableInfo2:
                Sql = "insert into DATACENTER values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%s,%s,%s,%s,%s,%s,%d)" \
                %( 
                    DATACENTER_ID,
                    DATACENTER_NAME,
                    SERVER_NAME,
                    SERVER_IP_ADDR,
                    APPLICATION_CATAGORY,
                    CONTAINER_COUNTS,
                    SERVER_STATUS,
                    SERVER_CPURESOURCE,
                    SERVER_MEMRESOURCE,
                    APPLICATION_CATAGORY_CPU_USED,
                    APPLICATION_CATAGORY_MEM_USED,
                    LAST_UPDATE_DATE
                )
                log.info(Sql)
                cursor.execute(Sql)
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
