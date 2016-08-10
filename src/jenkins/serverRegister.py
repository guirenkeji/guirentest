# -*- coding: utf-8 -*-
import os
from analysisxml import find_nodes,get_node_by_keyvalue,read_xml,write_xml,change_node_text
import json
import jconfig
import logging
import urllib2
logging.basicConfig(level = logging.DEBUG)
                     
def scmRegister (type,server,user,password): 
    data ={"": "0", "credentials": {"scope": "GLOBAL", "id": "", "username": user, "password": password,"description": "icloudsvn","$class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"}}
    data = json.dumps(data)
    cm1 = os.system("curl -X POST '%s/credential-store/domain/_/createCredentials' --data-urlencode 'json=%s' --connect-timeout 10" %(server,data))
    logging.info(cm1)    
    credentialsParams = getCredis()
    updatexml(type,credentialsParams)
    return 'credis ok'
def updatexml (type,credentialsParams): 

    if type == 'svn':
        try:
            tree = read_xml("temp/svnconfig.xml")
            ts = get_node_by_keyvalue(find_nodes(tree, "scm/locations/hudson.scm.SubversionSCM_-ModuleLocation/credentialsId"), "credentials")  
            change_node_text(ts, credentialsParams)
            write_xml(tree, "temp/svnconfig.xml")
            print ""
        except Exception,e:
            print e
    if type=='git':
            tree = read_xml("/temp/gitconfig.xml")
            ts = get_node_by_keyvalue(find_nodes(tree, "scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/credentialsId"), "credentials")   
            change_node_text(ts, credentialsParams)
#             change_node_text(tstring, string)
            write_xml(tree, "/temp/gitconfig.xml")
            print ""
def getCredis():
       data = urllib2.urlopen('%s/credential-store/domain/_/api/json?pretty=true' %(jconfig.jenkinsserver)).read()
       credis = json.loads(data)
       print credis
       for i in credis['credentials']:
           usercredis = urllib2.urlopen('%s/credential-store/domain/_/credential/%s/api/json?pretty=true' %(jconfig.jenkinsserver,i)).read()
           usercredis = json.loads(usercredis)
           if jconfig.svnuser+'/' in usercredis['displayName']:
                 return i
if __name__ == '__main__':
#      getCredis()
        scmRegister ('svn',jconfig.jenkinsserver,jconfig.svnuser,jconfig.svnpassword)