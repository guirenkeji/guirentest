


import os
import subprocess
IP = os.environ['IP']
# IP = '20.26.17.137:5000'
# dockerimage = 'tomcattest:1.0'
DOCKERIMAGE = os.environ['DOCKERIMAGE']
dockerimage = DOCKERIMAGE
BUILD_ID = os.environ['BUILD_ID']
def collectDockerImageId ():
    os.system ('docker build -t %s.%s . >readme' %(dockerimage,BUILD_ID))
    readmeFile = open('readme','r')
    readmeFilelist = readmeFile.readlines()
    content = readmeFilelist[-1]
    content = content.split()
    imageId=content[-1]
#      os.system ('docker build -d tomcattest:1.0.2 .')
#     os.system ('docker build -t tomcattest:1.0.%s . >>readme' %(BUILD_ID))
    os.system ('docker tag %s %s/%s.%s' %(imageId,IP,dockerimage,BUILD_ID))
    os.system ('docker push %s/%s.%s' %(IP,dockerimage,BUILD_ID))
#     os.system ('docker build -t tomcattest:1.0.%s .' %(BUILD_ID))
#      subprocess.check_call('docker build -d tomcattest:1.0.1 .')
    


 
run=collectDockerImageId()