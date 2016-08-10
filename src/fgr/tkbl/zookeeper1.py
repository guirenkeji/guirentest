#!/usr/bin/python
# -*- coding: utf-8 -*- 
import cx_Oracle
import requests
import json
import time

def main():
    db = cx_Oracle.connect('dcos/v1g2m60id2499yz@pdbdcos')
    cursor = db.cursor()
    sqls = []
    TIME = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    ts = 'to_date(\'%s\',\'yyyy-mm-dd hh24:mi:ss\')' %TIME

    hosts = ['vq20pzkp01','vq20pzkp02','vd20pzkp01','vd20pzkp02','pc-zjjazk01']
#    metrics = ['zk_ephemerals_count','zk_max_latency','zk_num_alive_connections','zk_server_state','zk_watch_count','zk_znode_count']
    metrics = ['zk_ephemerals_count','zk_num_alive_connections','zk_server_state']
    a = {'zk_ephemerals_count':'ZNODE量','zk_num_alive_connections':'连接数','zk_server_state':'状态'}
    cursor.execute("truncate table zookeeper")
    db.commit()
    for h in hosts:
        tmp = {}
        for m in metrics:
            r = requests.get("http://10.78.177.50:6071/history/%s/%s" %(h,m))
            text = json.loads(r.text)
            if m == 'zk_server_state' and text['data'][0]['value'] == 2:
                tmp['status'] = "leader"
            elif m == 'zk_server_state' and text['data'][0]['value'] == 1:
                tmp['status'] = "follower"
            else:
                tmp[m] = text['data'][0]['value']
        sql = 'insert into zookeeper values(\'%s\',\'%s\',\'%s\',\'%s\',%s)' \
        %(
                h,
                tmp['zk_ephemerals_count'],
                tmp['zk_num_alive_connections'],
                tmp['status'],
                ts
        )
        cursor.execute(sql)
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
