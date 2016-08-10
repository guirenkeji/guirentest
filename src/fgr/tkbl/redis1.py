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

    hosts = ['vq18redis01','vq18redis02','vq18redis03','vq18redis04','vd16redis01','vd16redis02','vd16redis03','vd16redis04']
    metrics = ['Keys','connected_clients','used_memory']
    a = {'Keys':'keys数量','connected_clients':'连接数','used_memory':'内存使用','status':'状态'}
    cursor.execute("truncate table redis")
    db.commit()
    for h in hosts:
        tmp = {}
        for m in metrics:
            r = requests.get("http://10.78.177.50:6071/history/%s/%s/port=16379" %(h,m))
            try:
                text = json.loads(r.text)
                tmp['status'] = 'up'
                if m == 'used_memory':
                    tmp[m] = str(int(text['data'][0]['value'])/1024)+'KB'
                else:
                    tmp[m] = text['data'][0]['value']
            except Exception,e:
                tmp['status'] = 'down'
                metrics_value = '0'
#        print h,tmp
        sql = 'insert into redis values(\'%s\',\'%s\',\'%s\',\'%s\',%s)' \
        %(
                h,
                tmp['Keys'],
                tmp['connected_clients'],
                tmp['used_memory'],
                ts
         )
        cursor.execute(sql)
        print sql
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
