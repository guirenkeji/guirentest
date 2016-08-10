import os
import json
import logging
logging.basicConfig(level=logging.DEBUG)
d = {
  "schedule": "R/2016-6-14T15:10:00+08:00/PT1M",\
  "retries": 3,\
  "name": "job-1",\
  "container": {\
    "type": "DOCKER",\
    "image": "20.26.25.150:5000/jdk7:t1.3",\
    "network": "BRIDGE",\
    "volumes": [\
      {\
        "containerPath": "/root/app/571/task/ord_task_tl_schema_timeout/log/",\
        "hostPath": "/logs/",\
        "mode": "RW"\
      }\
    ]\
  },\
  "owner": "18258829588@139.com",\
  "ownerName": "test",\
  "description": "This is a test!",\
  "cpus": "0.5",\
  "mem": "512",\
  "uris": [],\
  "command": "/usr/bin/sh /root/start.sh"\
}

# logging.basicConfig(level = logging.DEBUG)
def createFile(temple_local_filename,schedule=None,name=None,image=None,command=None):


    for i in range(1,201):
        i=str(i)
#         d["schedule"]="11.00"
        d["container"]["image"]='20.26.25.150:5000/jdk7:t1.4'
        d["name"]="1-803job-"+i
#         docker ps -a |grep  Exited|awk '{print $0}'|xargs docker rm -f
        d["command"]="sh /root/start.sh" 
        data= json.dumps(d)
        logging.info(data)
        for l in range(151,152):
            l='25.'+str(l)
            logging.info(l)
            cmd =os.popen("curl -X POST http://20.26.%s:4400/scheduler/iso8601 -H Content-Type:application/json -d'%s'" %(l,data) ).readlines()
            logging.info(cmd)        
        logging.info(i)         
def deleteJob():


    for i in range(1,201):
        i=str(i)
        i="1-803job-"+i
        for l in range(151,152):
            l='25.'+str(l)
            cmd =os.popen("curl -L -X DELETE  http://20.26.%s:4400/scheduler/job/%s -H Content-Type:application/json" %(l,i) ).readlines()
            logging.info(cmd)        
        print i  
            
if __name__ == '__main__':
#     createFile("data.py")
    deleteJob()