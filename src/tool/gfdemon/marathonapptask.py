import os
import json
from marathon import MarathonClient
from time import sleep
IP = '20.26.17.137:5000'
marathonip = 'http://20.26.17.133:8080'
DOCKERIMAGE = os.environ['DOCKERIMAGE']
dockerimage = DOCKERIMAGE
dockerimage = IP+'/'+dockerimage
BUILD_ID = os.environ['BUILD_ID']
JOB_NAME = os.environ['JOB_NAME']
SCALE=os.environ['SCALE']

dockerimage = dockerimage+'.'+BUILD_ID
appname = JOB_NAME

readed = json.load(open('temp.json', 'r'))
print readed
readed['container']['docker']['image'] = dockerimage
readed['id'] = appname

print readed

json.dump(readed, open('app.json', 'w')) 
c = MarathonClient(marathonip)

try:
   c.delete_app(appname,force=True)
except :
    pass
  
sleep(3) 

# c.delete_app("test-2",force=True)
os.system ('curl -X POST -H "Content-Type: application/json" %s/v2/apps -d@app.json' %(marathonip))

SCALE = int(SCALE)
c = MarathonClient('http://20.26.17.133:8080')
c.scale_app(appname,SCALE,force=True)
