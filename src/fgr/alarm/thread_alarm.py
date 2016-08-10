#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
# import cx_Oracle
import time 
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
from sqlalchemy import create_engine,DateTime
DB ='mysql+mysqlconnector://root:root@localhost:3306/icloud?charset=utf8'
mysqlcursor = create_engine(DB,echo=True)
def alarm_users():
    fd = open('/opt/dcos/alarm/alarm_users')
    fd_info = fd.read().splitlines()
    fd.close()
    users = []
    for i in fd_info:
        if i.startswith('#'):
            pass
        else:
            users.append(i.split()[0])
    return users

def sms(message):
    db=cx_Oracle.connect('mon','mon','zjmon')
    cursor = db.cursor() 
    users = alarm_users()
    for phone in users:
        sql = "insert into app_sm values ('188', \'%s\',\'%s\')" %(phone,message)
        cursor.execute(sql)
    db.commit()
    db.close()

def voice(voice_info):
    db=cx_Oracle.connect('hp_dbspi','hp_dbspi123','zjydkfxy1')
    cursor = db.cursor()
    sql="insert into icdmain.iptca_interface_voice(id,alarmtext,tel1,tel2,tel3,indb_time)  \
    values(to_char(dbmon.iptca.nextval),\'%s\',15158116209,18658162272,15158116209,sysdate)" %voice_info
    cursor.execute(sql)
    db.commit()
    db.close()

def alarm_control(alarm_type,log):
    alarm_type = alarm_type
    alarm_control_info = cursor.execute('select ts from alarm_control where alarm_tag = \'%s\'' %alarm_type).fetchall()
    if len(alarm_control_info) != 0:
        old_alarm_ts = int(float(alarm_control_info[0][0]))
        if new_alarm_ts - old_alarm_ts > 800:
            logInfo = "新的告警时间大于告警抑制表中前一个告警时间的1800秒，触发一次新的告警"
            log.info(logInfo)
            cursor.execute('delete from alarm_control where alarm_tag = \'%s\'' %alarm_type)
            db.commit()
            return 1
        else:
            logInfo = "新的告警小于告警抑制表中前一个告警时间的1800秒，告警被抑制，不将触发告警"
            log.info(logInfo)
            return 0
    else:
        logInfo = "告警抑制表中没有相应的记录，触发告警"
        log.info(logInfo)
        return 1

if __name__ == "__main__": 
    ########初始化事件###############################################################################
    ts = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    new_alarm_ts = int(time.time())

    ########初始化日志程序###########################################################################
    logFilePath = '/var/log/alarm/alarm.log'
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

    ########初始化数据库#############################################################################
    db = cx_Oracle.connect('dcos/v1g2m60id2499yz@pdbdcos')
    cursor = db.cursor()
    cursor.execute('insert into container_alarm_history_data select * from container_alarm_data')

    ########为了防止临时的为0的容器产生积累的告警数，讲5分钟内没有到达3次的线程告警数删除############
    cursor.execute('delete from CONTAINER_ALARM_DATA where container_create_time < sysdate - 5/1440')
    db.commit()

    ########初始化告警表中的容器线程数到达法制的记录数###############################################
    alarm_info = cursor.execute('select * from container_alarm_data').fetchall()
    alarm_count = len(alarm_info)
    container_type = alarm_info[0][3].split('_')[0]

    if alarm_count > 10:
        message = "%s %s有10个以上的实例线程数大于30,处于过载" %(ts,container_type)
        alarm_type = "total_thread"
        alarm_code = alarm_control(alarm_type,log)
        if alarm_code == 1:
            sms(message)
            voice(message)
            log.info(str(alarm_info))
            sql = 'insert into alarm_control values(\'%s\',\'%s\')' \
            %(
                new_alarm_ts,
                alarm_type
            )
            cursor.execute(sql)
        else:
            pass
        cursor.execute('truncate table container_alarm_data')
        db.commit()
    else:
        for i in alarm_info:
            if i[5] > 2:
                message = '%s %s SJYYT %s应用 %s 当前线程数为%s' %(ts,i[0],i[3],i[1],i[6])
                sms(message)
                voice(message)
                log.info(i)
                cursor.execute('delete from container_alarm_data where container_name = \'%s\'' %i[1])
                db.commit()
    db.close()
