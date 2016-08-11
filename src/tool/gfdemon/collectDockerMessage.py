import time
import os
import subprocess
APP = os.environ['APPNAME']
FROM = os.environ['FROM']
CMD = os.environ['CMD']
COPY = os.environ['COPY']
IP = os.environ['IMAGESERVERIP']

buidtime = time.strftime("%Y-%m-%d.%Hh%Mm%Ss",time.localtime(time.time()))
BUILD_ID = buidtime
BUILD_ID = BUILD_ID.encode()
def collectDockerImageId ():
    modifyDockerfile()
    os.system ('docker build -t %s/%s:%s . >readme' %(IP,APP,BUILD_ID))
    readmeFile = open('readme','r')
    readmeFilelist = readmeFile.readlines()
    content = readmeFilelist[-1]
    content = content.split()
    imageId=content[-1]
#      os.system ('docker build -d tomcattest:1.0.2 .')
#     os.system ('docker build -t tomcattest:1.0.%s . >>readme' %(BUILD_ID))
#     os.system ('docker tag %s %s/%s.%s' %(imageId,IP,dockerimage,BUILD_ID))
    os.system ('docker push %s/%s:%s' %(IP,APP,BUILD_ID))
#     os.system ('docker build -t tomcattest:1.0.%s .' %(BUILD_ID))
#      subprocess.check_call('docker build -d tomcattest:1.0.1 .')
    images=IP+'/'+APP+':'+BUILD_ID
    buildFile=open('build.txt','w')
    buildFile.write(images)
    buildFile.close()

def modifyDockerfile():

#         image = dockerimages
#         copy= 'copy *.war /app/app/'
#         COPY =copy
#         FROM = 'FROM %s' %(image)
#         CMD = ""
        dockerfile ='%s\n%s\n%s' %(FROM,COPY,CMD)
        buildFile=open('Dockerfile','w')
        buildFile.write(dockerfile)
        buildFile.close()

 
run=collectDockerImageId()