# -*- coding: UTF-8 -*- 
import os,sys
import redis
from rediscluster import StrictRedisCluster

def main():
    redishostlist = ['192.168.23.133']
    nodeslist = []
    for serverip in redishostlist:

         nodes=[{"host": serverip,"port": i} for i in xrange(6379, 6380)]
         nodeslist.extend(nodes)

    startup_nodes = nodeslist
    try:
        r = StrictRedisCluster(startup_nodes=startup_nodes)
    except Exception, err:
        print err
        print 'failed to connect cluster'
        sys.exit(0)

    #for i in xrange(1000):
    r.set('nima', 'aff')
    print r.get('nima3')

if __name__=='__main__':
    main()