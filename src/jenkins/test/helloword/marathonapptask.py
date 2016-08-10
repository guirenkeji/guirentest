import os
import json
from marathon import MarathonClient
from time import sleep
import jconfig
# marathonip = jconfig.marathonip
# user = jconfig.user
# password = jconfig.password
# c = MarathonClient(marathonip,username=user,password=password)
def servermarathon():    
        STRING = os.environ['STRING']
        content = STRING
        contentlist = content.split('&')
        list = []
        for i in contentlist:
            p = i.split('=')
            p = p[1] 
            l = list.append(p)
        (maurl,mau,map) =tuple(list)
        marathonip = maurl
        user = mau
        password = map
        c = MarathonClient(marathonip,username=user,password=password)
        buildFile=open('build.txt','r')
        dockerimage = buildFile.readline()
        buildFile.close()
        readed = json.load(open('temp.json', 'r'))
        readed['container']['docker']['image'] = dockerimage
        name = readed['id'] 
        json.dump(readed, open('app.json', 'w')) 
        
        try:
           c.delete_app(name,force=True)
           print 'delete'
        except :
            pass
          
        sleep(3)
        u= mau+':'+map
        cmd1 = os.system ('curl -u %s -X POST -H "Content-Type: application/json" %s/v2/apps -d@app.json' %(u,marathonip))
# SCALE =2
# SCALE = int(SCALE)
# c = MarathonClient(marathonip)
# c.scale_app(name,SCALE,force=True)
if __name__ == '__main__':
    servermarathon()
