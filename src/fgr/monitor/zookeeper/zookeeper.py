#!/usr/bin/python
import os
# import cx_Oracle
import socket
import json
import re

dcos_zookeeper = ['10.78.182.10','10.78.182.11','10.78.217.10','10.78.217.11','10.70.216.39']

pattern = re.compile('Mode: leader|Mode: follower') 
db = cx_Oracle.connect('dcos/v1g2m60id2499yz@pdbdcos')
cursor = db.cursor()
for i in dcos_zookeeper: 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ip = i
        port = 2181
        zk_type = "dcos"
        status2 = "up"
        client.connect((ip,port))
        client.send("status")
        response = client.recv(4096)
        match = pattern.search(response)
        if match:
            status1 = match.group().split(':')[1].strip()
        sql = "insert into zookeeper values (\'%s\',\'%s\',%d,\'%s\',\'%s\')" %(ip,zk_type,port,status2,status1)
        cursor.execute(sql)
        db.commit()
        db.close()
        client.close()
    except Exception,e:
        ip = i
        port = 2181
        zk_type = "scrm"
        status2 = "down"
        status1 = "error"
        sql = "insert into zookeeper values (\'%s\',\'%s\',%d,\'%s\',\'%s\')" %(ip,zk_type,port,status2,status1)
        db.commit()
        db.close()
        client.close()
