# -*- coding: UTF-8 -*- 
import redis
# from rediscluster import StrictRedisCluster
r = redis.StrictRedis(host='192.168.23.133',port=6379)
r.set('guo3','shuai3')
# r.get('guo')

print r['guo'],r.get('guo')         
print r.keys()
# print r.dbsize()         #当前数据库包含多少条数据       
# r.delete('guo')
# print r.save()               #执行“检查点”操作，将数据写回磁盘。保存时阻塞
# r.get('guo');
# r.flushdb()        #清空r中的所有数据

# 
# from rediscluster import StrictRedisCluster
#  
# startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]
# rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
# rc.set("foo", "xiaorui.cc")

