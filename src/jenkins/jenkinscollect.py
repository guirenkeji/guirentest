# -*- coding: UTF-8 -*- 
import os
from flask import Flask,request,url_for,jsonify
import jenkinsapi
from marathon import MarathonClient
import template
from jenkinsapi.jenkins import Jenkins 
import appinteration
import jconfig
import appcicontroller
import appclientcontroller
import models
import cron
import xml.etree.ElementTree
# from flask_socketio import SocketIO
import logging
jenkinsserver = jconfig.jenkinsserver
app = Flask(__name__)
@app.route('/')
def hello_Jenkins():
    return 'Hello icloud ci server!'

@app.route('/logging')
def root():
    app.logger.info('info log')
    app.logger.warning('warning log')
    return 'hello'
def get_server_instance():
    server = Jenkins(jenkinsserver)
#     server = Jenkins('http://127.0.0.1:8080')
    return server



# @app.route('/jenkins/job/<taskcasename>')
def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        print 'Job Name:%s' %(job_instance.name)
        print 'Job Description:%s' %(job_instance.get_description())
        print 'Is Job running:%s' %(job_instance.is_running())
        print 'Is Job enabled:%s' %(job_instance.is_enabled())


@app.route('/jenkins/job/stop/<taskcasename>')        
def disable_job():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    job_name = 'createImage'
    if (server.has_job(job_name)):
        job_instance = server.get_job(job_name)
        job_instance.disable()
        print 'Name:%s,Is Job Enabled ?:%s' %(job_name,job_instance.is_enabled()) 
def get_plugin_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for plugin in server.get_plugins().values():
        print dir(plugin)
        print "Short Name:%s" %(plugin.shortName)
        print "Long Name:%s" %(plugin.longName)
        print "Version:%s" %(plugin.version)
        print "URL:%s" %(plugin.url)
        print "Active:%s" %(plugin.active)
        print "Enabled:%s" %(plugin.enabled) 
@app.route('/jenkins/reposrelease/run/<id>')             
# def job_build(id):
#     # Refer Example #1 for definition of function 'get_server_instance'
#     server = get_server_instance()
#     jenkinsrepostask = models.getjenkinsrepostaskid(id)
#     jenkinsparams={'PROJECTNAME':jenkinsrepostask.ProjectName,'PACKAGENAME':jenkinsrepostask.PackageName}
#     if 'crm' in jenkinsrepostask.ProjectName:
#         
#          server.build_job('crm-release',params=jenkinsparams)
#     if 'sjyyt' in  jenkinsrepostask.ProjectName:
#          server.build_job('zjst-release',params=jenkinsparams)  
#     return 'ok'
def createjob():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
#     server.create_job('jobname', xml)
@app.route('/jenkins/job/delete/<taskcasename>')
def deletejob():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    server.delete_job('jobname2')

    
@app.route('/jenkins/job/')    
def createjobconfig(name,type,scmurl, poll,shell):

    typestatus = 0
    server = get_server_instance()
    if type == 'svn':
        config = template.jenkinsconfigfile
        config = config.replace('%SVNPATH%',scmurl)
        config = config.replace('%POLL%',poll )
        config = config.replace('%SHELL%', shell)
        config = config.split('\n')
        list = []
        sl = '\n'
        for i in config:
            list.append(i.strip())
        config = sl.join(list)
         
        print  config
#     config = xml.etree.ElementTree.fromstring(config)    
    return config
@app.route('/jenkins/job/update/<taskcasename>')
def updatejobconfig(name,type,scmurl,poll,shell):
#     scmurl = 'svn://20.26.19.69/home/svn/svn_repository/Program/script/release'
#     poll = 'H/5 * * * *'
#     shell = 'sleep 5 dir 1111 666 /home/test.sh\n'+"/home/test.sh"
    typestatus = 0
    server = get_server_instance()
    job = server.get_job(name)
    config = template.jenkinsconfigfile
    config = config.replace('%SVNPATH%',scmurl)
    config = config.replace('%POLL%',poll )
    config = config.replace('%SHELL%', shell)
    config = config.split('\n')
 
    list = []
    sl = '\n'
    for i in config:
        list.append(i.strip())
    config = sl.join(list)
      
    print config
#     root = xml.etree.ElementTree.fromstring(config) 
    job.update_config(config)
    print 'ok'   

# with app.test_request_context():
#     print  url_for('createjobconfig', next="dd")
#     url_for('downloadrepospackagefile', next="sysname") 

@app.route('/jenkins/reposrelease/1/<content>')    
def appinterationdemo(content):    
    taskstatus = appinteration.demo(content)
    return taskstatus
#  rest api 接口
@app.route('/ci/client/1.0/scm/data',methods=['POST'])    
def appinterationscmci():
    appname = request.json['JOB_NAME']
    build_id = request.json['build_id']
#     content = request.args
    data = appcicontroller.jenkinsscminfo(appname,build_id)
    data=data
    return jsonify({'data': data})
#应用构建日志接口
@app.route('/v1.0/ci/buildlog',methods=['POST'])    
def apptaskbuildlog():
    #icloud app_id json请求
    job_name = request.json['app_id']
    logdata = appcicontroller.jobnametasklog(job_name)

    return logdata
#手动启动构建任务
@app.route('/v1.0/ci/manualstart',methods=['POST'])    
def appmanualstarttask():
    name = request.json['name']
    appcicontroller.startjenkinstask(name)

    return 'manualstart ok'
@app.route('/v1.0/ci/manualtrigger',methods=['POST'])    
def appmanualtriggertask():
    name = request.json['app_id']
    appcicontroller.triggerjenkinstask(name)

    return 'manualtrigger ok'
@app.route('/ci/client/1.0/log',methods=['POST'])    
def appinterationslog_client():
    jobname = request.json['jobname']
    jobbuildid = request.json['jobbuildid']
    log = request.json['log']
    models.savelog(jobname,jobbuildid,log)
    return 'jenkins jenkinsloginfo_client ok '
@app.route('/ci/client/1.0/status',methods=['POST'])    
def appinterationstatus_client():
    jobname = request.json['jobname']
    data = models.gettaskstatus(jobname)
    data=data
    return 'jenkins jenkinsloginfo_client ok '
@app.route('/ci/client/1.0/updatestatus',methods=['POST'])    
def appinterationupdatestatus_client():
    jobname = request.json['jobname']
    data = models.updatetaskstatus(jobname)
    data=data
    return 'jenkins jenkinsloginfo_client ok '
@app.route('/ci/client/1.0/uploadfile',methods=['POST'])    
def appInterationUpload_client():
    app_id = request.json['JOB_NAME']
    data = {'icloudUrl':'http://'+jconfig.icloudIP+':'+jconfig.icloudport+'/iCloud/fileUpload/uploadFile.dox?token=5846be1f777c486b89c2e4e70a199d2a','icloudIP':jconfig.icloudIP,'icloudport':jconfig.icloudport}
    return jsonify(data=data)

@app.route('/jenkins/reposrelease/3/<content>')    
def appinterationbinding(content):
    taskstatus = appinteration.serveicebinding (content)
    return taskstatus
@app.route('/jenkins/reposrelease/4/<content>')    
def appinterationissue(content):
    taskstatus = appinteration.releasemarathon(content)
    return taskstatus

@app.route('/jenkins/testrelease',methods=['POST'])
def jenkinsreleaseapi():
# curl -i -X POST -H "Content-Type: application/json" -d '{"url":"'testcat'"}' 20.26.17.145:5002/jenkins/testrelease
    server = get_server_instance()
    url =request.json['URL']
    jenkinsparams = {'URL':url}
    server.build_job('qqd-release',params=jenkinsparams)
    return 'HELLO DCOS!!!'
#client服务注册
@app.route('/v2/serverclient/register',methods=['POST'])
def serverRegister():
    data = request.json['data']
    data = data+'/n'
#     hostname = data.split('/')[-1]
    register = open('register','r')
    registerlist = register.readlines()
    register.close()
    if data not in registerlist:
        registernew = open('register','a')
        registernew.writelines(data)
        registernew.close()
    
    return 'register_ok'

#icloud服务请求，客户端分发
@app.route('/v2/serverclient/download',methods=['POST'])
def serverclientAPI():
    app.logger.info('info log')
    app.logger.warning('warning log')
    url = request.json['url']
#     url = 'http://10.73.130.87:8080/iCloud/download/download.dox?filename=edcb54656ff1475993a5781b5463aaea.war&outFilename=test.war'
    register = open('register','r')
    registerlist = register.readlines()
    register.close()
    for i in registerlist:
           if not i=="\n":
           
           
               appclientcontroller.httpdownloadpost(i.split(':')[1].strip(),url)
               print i.split(':')[1].strip()
    return 'app_download ok'

# with app.test_request_context():
#    
#      url_for('appinterationscm', next='/')
if __name__ == '__main__':
#     get_plugin_details()
#     app.run(host= '0.0.0.0',port=5013)
#     cron.run()
#     serverclientAPI()
    handler = logging.FileHandler('appci.log')
    app.logger.addHandler(handler)
    app.run(host= '0.0.0.0',port=jconfig.myport)