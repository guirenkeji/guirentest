# -*- coding: UTF-8 -*- 
import os
from jenkinsapi.jenkins import Jenkins 
import jenkinscollect
from time import sleep
import jconfig

scmurl = jconfig.scmurl
poll = jconfig.poll
IP= jconfig.IP
serverip1=jconfig.serverip1
serverip2=jconfig.serverip2
def demo (content):
    config = jenkinscollect.createjobconfig()
    print content
    contentlist = content.split('&')
    print contentlist
    list = []
    for i in contentlist:
        p = i.split('=')
        p = p[1] 
        l = list.append(p)
    (type,id,name,filename,svnurl,jsonfilename) =tuple(list)  
    server = jenkinscollect.get_server_instance()
    image= ''
    if type=='war':
#         scmurl = 'svn://20.26.19.69/home/svn/svn_repository/Program/script/helloword'
        params = 'name'+'='+name+'&'+'images'+'='+image
        params = params.encode('utf-8')
#         shell = "rm -rf helloword.py\ncp temphelloword.py helloword.py\nsed -i 's/%hello%/%s/g' helloword.py" %(msg)
        shell = 'rm -rf *.war\nrm -rf *.json\nwget %s/%s\nwget %s/%s\nmv *.war %s.war\npython2.7 collectDockerMessage.py' %(serverip1,filename,serverip2,jsonfilename,name)

    if type == 'svn':
        url = svnurl.replace('+','/')
        topath = ''
        params = 'name'+'='+name+'&'+'images'+'='+image
        shell = 'rm -rf *.war\nrm -rf *.json\nant all\nwget %s/%s' %(serverip2,jsonfilename)
    if type == 1:
       topath = ''
       params = 'filename'+'='+filename
       shell = 'wget %s/%s\npscp -h host %s %s' %(serverip1,filename,filename,topath)
    jenkinsparams={'STRING':params}
    try:
       print config
       server.create_job(name,config)
    except Exception,e:
        print e
    if type=='svn':
        config = jenkinscollect.updatejobconfig(name,url, poll, shell)
        repeat (name,jenkinsparams)
        shell = 'python2.7 collectDockerMessage.py'
        config = jenkinscollect.updatejobconfig(name,scmurl, poll, shell)
    else:
        config = jenkinscollect.updatejobconfig(name,scmurl, poll, shell) 
    server.build_job(name,jenkinsparams)
    sleep(8)
    job = server.get_job(name)
    lastbuild = job.get_last_build()
    laststatus = lastbuild.get_status()
    while( laststatus==None):
        sleep(2)
        lastbuild = job.get_last_build()
        laststatus=lastbuild.get_status()
        print laststatus 
        if not laststatus==None:
            break
    return laststatus
    
def repeat (name,jenkinsparams):
    server = jenkinscollect.get_server_instance()
    server.build_job(name,jenkinsparams)
    sleep(8)
    job = server.get_job(name)
    lastbuild = job.get_last_build()
    laststatus = lastbuild.get_status()
    while( laststatus==None):
        sleep(2)
        lastbuild = job.get_last_build()
        laststatus=lastbuild.get_status()
        print laststatus 
        if not laststatus==None:
            break
    return laststatus
def psshpackname (content):
#     ${PACKAGENAME} ${TOPATH}
    contentlist = content.split('&')
    list = []
    for i in contentlist:
        p = i.split('=')
        p = p[1] 
        l = list.append(p)
    (id,name,packname,TOPATH) =tuple(list) 
    shell = 'rm -rf *.war\nwget %s/%s\npscp -h host %s %s '%(IP,packname,packname,TOPATH) 
    server = jenkinscollect.get_server_instance()
    config = jenkinscollect.updatejobconfig(name,scmurl, poll, shell)
    params = 'packname'+'='+packname
    params = params.encode('utf-8')
    jenkinsparams={'PARAMS':params}
    server.build_job(name,jenkinsparams)
    job = server.get_job(name)
    lastbuild = job.get_last_build()
    laststatus = lastbuild.get_status()
    return laststatus
def serveicebinding (content):
    
    contentlist = content.split('&')
    list = []
    for i in contentlist:
        p = i.split('=')
        p = p[1] 
        l = list.append(p)
    (id,name,packname) =tuple(list) 
    shell = 'rm -rf app.json\nwget %s/%s'%(IP,packname) 
    server = jenkinscollect.get_server_instance()
    config = jenkinscollect.updatejobconfig(name,scmurl, poll, shell)
    params = 'packname'+'='+packname 
    jenkinsparams={'PARAMS':params}
    server.build_job(name,jenkinsparams)
    job = server.get_job(name)
    lastbuild = job.get_last_build()
    laststatus = lastbuild.get_status()
    return laststatus
def releasemarathon (content):
    shell = 'set\npython2.7 marathonapptask.py'
#     config = jenkinscollect.updatejobconfig(scmurl, poll, shell)
    contentlist = content.split('&')
    print contentlist
    list = []
    for i in contentlist:
        p = i.split('=')
        p = p[1] 
        l = list.append(p)
    (id,name,maurl,mau,map) =tuple(list)
    server = jenkinscollect.get_server_instance()
    config = jenkinscollect.updatejobconfig(name,scmurl, poll, shell)
    maurl = maurl.replace('+','/')
    params = 'maurl'+'='+maurl+'&'+'mau'+'='+mau+'&'+'map'+'='+map
    params = params.encode('utf-8')
    jenkinsparams={'STRING':params}
    server.build_job(name,jenkinsparams)
    sleep(2)
    job = server.get_job(name)
    lastbuild = job.get_last_build()
    laststatus = lastbuild.get_status()
    print laststatus
    while( laststatus==None):
        sleep(2)
        lastbuild = job.get_last_build()
        laststatus=lastbuild.get_status()
        print laststatus 
        if not laststatus==None:
            break
    return laststatus
if __name__ == '__main__':
#     maurl = maurl.replace('+','/')
#     params = 'maurl'+'='+maurl+'&'+'mau'+'='+mau+'&'+'map'+'='+map
#     params = params.encode('utf-8')
#     from marathonapptask import servermarathon
#     servermarathon(params)

    demo()