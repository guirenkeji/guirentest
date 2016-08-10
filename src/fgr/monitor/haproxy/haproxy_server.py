#!/usr/bin/python
import os
import json
import sys
import time
import socket
from datetime import datetime
from sqlalchemy import create_engine,DateTime
# import cx_Oracle
DB ='mysql+mysqlconnector://root:root@localhost:3306/icloud?charset=utf8'
mysqlcursor = create_engine(DB,echo=True)
ts = time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime()) 

if __name__ == '__main__':
#     db = cx_Oracle.connect('dcos/v1g2m60id2499yz@pdbdcos')
#     cursor = db.cursor()
#     pssh_info = os.popen('pssh -h /etc/dcos/haproxy -i "python /data/dcos/dcos/bin/haproxy-client.py"').read().splitlines()
    haproxyweb_totalscur = 0
    haproxyapp_totalscur = 0
#     containernames = cursor.execute('select hostname,containername,haproxy_type from haproxy_current_data').fetchall()
    containernames2 = mysqlcursor.execute('select hostname,containername,haproxy_type from haproxy_current_data').fetchall()
#     cursor.execute('truncate table haproxy_current_data')
#     mysqlcursor.execute('truncate table haproxy_current_data')
#     for i in pssh_info:
#         if i.count('SUCCESS'):
#             pass
#         elif i.count('FAILURE'):
#             pass
#         else:
#             TIME = 'to_date(\'%s\',\'yyyy-mm-dd hh24:mi:ss\')' %i.split()[0]
#             hostname = i.split()[1]
#             ip_address = i.split()[2]
#             containername = i.split()[3]
#             container_port = i.split()[4]
#             haproxy_type = i.split()[5]
#             qcur = int(i.split()[6])
#             rate = int(i.split()[7])
#             scur = int(i.split()[8])
#             byin = int(i.split()[9])
#             byout = int(i.split()[10])
#             checktime = float(i.split()[11])
#             sql = 'insert into haproxy_current_data values (%s,\'%s\',\'%s\',\'%s\',%s,%s,%s,\'%s\',\'%s\',\'%s\')' \
#                 %(  
#                     TIME,
#                     hostname,
#                     containername,
#                     haproxy_type,
#                     qcur,
#                     rate,
#                     scur,
#                     checktime,
#                     ip_address,
#                     container_port
#                 )
#             print sql
#             cursor.execute(sql)
#             mysqlcursor.execute(sql)
#     haproxy_total = cursor.execute('select haproxy_type,sum(session_rate) from haproxy_current_data group by haproxy_type').fetchall()
    haproxy_total2 = mysqlcursor.execute('select haproxy_type,sum(session_rate) from haproxy_current_data group by haproxy_type').fetchall()
#     for j in haproxy_total:
#         tongjisql = 'insert into haproxy_history_data values (%s,%s,\'%s\',%d)' \
#         %(
#             "SEQ_MESOS_DATA.NEXTVAL",
#             TIME,
#             j[0],
#             j[1]
#         )
#         cursor.execute(tongjisql)
   
    for j in haproxy_total2:
        TIME =  datetime.now()
        tongjisql2 = 'insert into haproxy_history_data values (%s,%s,\'%s\',%d)' \
        %(
#             "SEQ_MESOS_DATA.NEXTVAL",
            '1',      
            TIME,
            j[0],
            j[1]
        )
        mysqlcursor.execute(tongjisql2)   
#     db.commit()
#     db.close()
