# -*- coding: UTF-8 -*- 
import os
from jenkinsapi.jenkins import Jenkins 
import jenkinscollect
from time import sleep
import jconfig
# import appinteration
import urllib2 
import json
import chardet
import models
from temp import task

class workerror(RuntimeError):
   def __init__(self, arg):
      self.args = arg


def jenkinsscminfo(job_name,build_id):
#     job_name = 'test'
#     bulid_id = '10'
    server = jenkinscollect.get_server_instance()
    job=server.get_job(job_name)
#     api = job.python_api_url("http://127.0.0.1:8080/job/test/7")
    data = urllib2.urlopen('%s/job/%s/%s/api/json?pretty=true' %(jconfig.jenkinsserver,job_name,build_id)).read()
    print  data
   
    print type(data)
    data =  json.loads(data)
    data = data['changeSet']['items']
    datalist=[]
    for i in data:
        i.pop('paths')
        datalist.append(i)
#         print datalist
    return datalist
def createjenkinstask (name,type,scmurl, poll):
   
    shell = "sh build.sh"
    port = str(jconfig.myport)
    string = 'serverip='+jconfig.myserverip+'&'+'port='+port
#     server = jenkinscollect.get_server_instance()
    createtask = task.createtask(name,type,scmurl, poll,shell,string)
    try:
        
        if createtask == 'create jenkins task error':
            raise RuntimeError
    except workerror,e:
        print e
    
    return createtask



def updatajenkinstask (name,type,scmurl, poll):
    shell = "sh build.sh"
#     server = jenkinscollect.get_server_instance()
    updatetask = task.updatetask(name,type,scmurl, poll,shell)
    return updatetask
#svn和git模板更新
def updatajenkinstaskmodel (name,type,scmurl, poll):
    shell = "sh build.sh"
    port = str(jconfig.myport)
    string = 'serverip='+jconfig.myserverip+'&'+'port='+port
#     server = jenkinscollect.get_server_instance()
    updatajenkinstaskmodel = task.updatescmtypetask(name,type,scmurl, poll,shell,string)
    return updatajenkinstaskmodel
def deletejenkinstask (name):
    server = jenkinscollect.get_server_instance()
    server.delete_job(name)
#开启构建任务    
def startjenkinstask (name):
    server = jenkinscollect.get_server_instance()
    jobname = server.get_job(name)
    jobname.enable()
    return 'enablejenkinstask'
#手动触发构建
def triggerjenkinstask (name):
    server = jenkinscollect.get_server_instance()
    jobname = server.get_job(name)
    jobname.enable()
    server.build_job(name)
    sleep(10)
    jobname.disable()
    return 'enablejenkinstask'
def stopjenkinstask (name):
    server = jenkinscollect.get_server_instance()
    jobname = server.get_job(name)
    jobname.disable()
    return 'disablejenkinstask'
def getjobstatus (name):
    server = jenkinscollect.get_server_instance()
    jobname = server.get_job(name)
    build = jobname.get_last_build()
    buildid = build.buildno
    getjobstatus =  build.get_status()
    return (buildid,getjobstatus)

#构建日志获取
def jobnametasklog (job_name):
#     job_name = 'test'
#     bulid_id = '10'
    server = jenkinscollect.get_server_instance()
    job=server.get_job(job_name)
    build_id =job.get_last_build()
    buildno = build_id.buildno
    
    data = urllib2.urlopen('%s/job/%s/%s/consoleText' %(jconfig.jenkinsserver,job_name,buildno)).read()
    
    logdata = data.decode('gb2312').encode('utf8')
    print logdata
    return logdata
    
def monitorjenkinsloginfo_client (jobname):
    server = jenkinscollect.get_server_instance()
    job = server.get_job(jobname)
    lastbuild = job.get_last_build()
    laststatus = lastbuild.get_status()
    while( laststatus==None):
        sleep(2)
        lastbuild = job.get_last_build()
        laststatus=lastbuild.get_status()
        print laststatus 
        if not laststatus==None:
            break
    models.updatetaskstatus(jobname, laststatus)   
    return laststatus
def monitorjenkinstatusinfo (jobname):
    server = jenkinscollect.get_server_instance()
    job = server.get_job(jobname)
    lastbuild = job.get_last_build()
    laststatus = lastbuild.get_status()
    while( laststatus==None):
        sleep(5)
        lastbuild = job.get_last_build()
        laststatus=lastbuild.get_status()
        print laststatus 
        print lastbuild
        if not laststatus==None:
            break
#     models.updatetaskstatus(jobname, laststatus)  
    print laststatus,lastbuild
    return laststatus
def analysistempxml (name,type,scmurl, poll,shell):
    if type == 'svn':
        
        print 'svn'

    if type=='git':
        print 'git'
    
if __name__ == '__main__':
#     monitorjenkinstatusinfo_client ('test')
    jobnametasklog('demo')     
#      getjenkinsjobstatus("cc4")