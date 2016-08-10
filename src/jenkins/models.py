# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText,SMALLINT
import jconfig
# import mysql.connector
from datetime import datetime
import appcicontroller
import time
# conn = mysql.connector.connect(**jconfig.mysql)
DB = jconfig.DB
engine = create_engine(DB,echo=True)
BaseModel = declarative_base()
def create_database():
    BaseModel.metadata.create_all(bind=engine)
def drop_database():
    BaseModel.metadata.drop_all(bind=engine)
def get_session():
    
    return Session(bind = engine)

class JENKINS_TASK(BaseModel):
 
    __tablename__ = 'JENKINS_TASK'
    JENKINS_TASK_ID = Column('JENKINS_TASK_ID', Integer,primary_key=True,nullable=False,autoincrement=True)
    JOB_NAME = Column('JOB_NAME', NVARCHAR(200),nullable = False)
    CODE_REPO_TYPE = Column('CODE_REPO_TYPE', NVARCHAR(300),nullable = False)
    SCMURL = Column('SCMURL', NVARCHAR(600),nullable = False)
    POLL = Column('POLL', NVARCHAR(200),nullable = False)
    SHELL = Column('SHELL', NVARCHAR(500),nullable = False)
    PROGRESSBAR = Column('PROGRESSBAR', NVARCHAR(300),nullable = False)
    STATUS = Column('STATUS', NVARCHAR(300),nullable = False)
    CREATEDATE = Column('CREATEDATE', DateTime,nullable=False)
    UPDATE_TIME = Column('UPDATE_TIME', DateTime,nullable=False)

# class JENKINSTASKREPOS(BaseModel):
#  
#     __tablename__ = 'JENKINSTASKREPOS'
#     JENKINSTASKREPOSID = Column('JENKINSTASKREPOSID', Integer,primary_key=True,nullable=False,autoincrement=True)
#     JOBNAME = Column('JOBNAME', NVARCHAR(300),nullable = False)
#     BUILDID = Column('BUILDID', NVARCHAR(300),nullable = False)
#     STATUS = Column('STATUS', NVARCHAR(300),nullable = False)
#     CREATEDATE = Column('CREATEDATE', DateTime,nullable=False)
#     UPDATEDATA = Column('UPDATEDATA', DateTime,nullable=False)

class JENKINS_CI(BaseModel):
 
    __tablename__ = 'JENKINS_CI'
    JENKINSCIID = Column('JENKINSCIID', Integer,primary_key=True,nullable=False,autoincrement=True)
    JOBNAME = Column('JOBNAME', NVARCHAR(300),nullable = False)
    BUILDID = Column('BUILDID', NVARCHAR(300),nullable = False)
    CREATEDATE = Column('CREATEDATE', DateTime,nullable=False)
    UPDATEDATA = Column('UPDATEDATA', DateTime,nullable=False)
    LOGS = Column('LOGLIST', NVARCHAR(500))        
#     PackageType = Column('packagetype', NVARCHAR(30),nullable = False)
def servicesCreate(taskname,type,scmurl,poll,CREATEDATE,UPDATE_TIME):
    session = get_session()
    SHELL ='0'
    PROGRESSBAR = '0'
    STATUS = '0'
    T = JENKINS_TASK()
    T.JOB_NAME = taskname
    T.CODE_REPO_TYPE = type
    T.SCMURL = scmurl
    if poll==None:
        poll=''
    T.POLL = poll
    T.PROGRESSBAR = PROGRESSBAR
    T.SHELL = SHELL
    T.STATUS = STATUS
    T.CREATEDATE = CREATEDATE
    T.UPDATE_TIME = UPDATE_TIME
    session.add(T)
    session.commit()
    session.close()
def delete(id):
    session = get_session()
    try:
        d1 = session.query(JENKINS_TASK).filter(JENKINS_TASK.JOB_NAME == id).delete()
    except Exception,e:
        print 'd1 delete error' 
    try:       
        d2 = session.query(JENKINS_CI).filter(JENKINS_CI.JOBNAME == id).delete()
    except Exception,e:
        print 'd2 delete error' 
    session.commit()
    session.close()
    return id 
# taskname,scmurl,poll,CREATEDATE,UPDATE_TIME   
def update(taskname,type,scmurl,poll,CREATEDATE,UPDATE_TIME):
    session = get_session()
 
    task = session.query(JENKINS_TASK).filter(JENKINS_TASK.JOB_NAME == taskname).update({'CODE_REPO_TYPE':type,'SCMURL':scmurl,'POLL':poll,'CREATEDATE':CREATEDATE,'UPDATE_TIME':UPDATE_TIME})
 
    session.commit()
    session.close()
def updatetaskstatus(jobname,buildid,status):
    session = get_session()
 
    task = session.query(JENKINS_TASK).filter(JENKINS_TASK.JOB_NAME == jobname).update({'STATUS':status})
    task1 = session.query(JENKINS_CI).filter(JENKINS_CI.JOBNAME == jobname).update({'BUILDID':buildid,'UPDATEDATA':datetime.now()})
 
    session.commit()
    session.close()    
# def PackageCreate(projectname,packagename):
# #     database = get_session()
#     session = get_session()
#     T = JENKINSTASKREPOS()
#     num = count()+1
#     T.STATUS = 0   
#     T.JENKINSTASKREPOSID = num 
#     T.PROJECTNAME = projectname
#     T.PACKAGENAME = packagename
#     T.CREATEDATE = datetime.now()
#     session.add(T)
#     session.commit()
#     session.close()    
#     return 'Hello jenkins!!!' 
# def count():
#     session = get_session()
#     num = session.query(JENKINSTASKREPOS).count()
#     return num
# def getjenkinsrepostaskid(id):
#     session = get_session()
#     id =int(id)
#     jenkinsrepostask = session.query(JENKINSTASKREPOS).filter(JENKINSTASKREPOS.JENKINSTASKREPOSID == id).one()
#     return jenkinsrepostask     
def savelog(jobname,buildid,log):
    session = get_session()
    T = JENKINS_CI()
    T.JOBNAME = jobname
    T.BUILDID = buildid
    T.LOGS = log
    T.CREATEDATE = datetime.now()
    session.add(T)
    session.commit()
    session.close()    
    return 'save log ok!!!'  
def savetask(jobname):
    session = get_session()
    T = JENKINS_CI()
    T.JOBNAME = jobname
    T.BUILDID = '0'
    T.CREATEDATE = datetime.now()
    T.UPDATEDATA = datetime.now()
    session.add(T)
    session.commit()
    session.close()    
    return 'save log ok!!!'
def getservertaskinfo ():

    sql = "SELECT app_id,code_repo_type,code_repo_url,trigger_time,create_time,last_update_time FROM cfg_app_public"
    data = sqlquery(sql)
#       ('cc','svn','svn://20.26.19.69/home/svn/svn_repository/Program/script/helloword','*/5 * * *','2016-04-20 00:00:00','2016-04-20 00:00:33'),('cc','svn','svn://20.26.19.69/home/svn/svn_repository/Program/script/helloword','*/5 * * *','2016-04-20 00:00:00','2016-04-20 00:00:33'),
#     data = [('cc5','svn','svn://20.26.19.70/home/svn/svn_repository/Program/script/helloword','*/8 * * * *','2016-04-20 00:00:00',datetime(2016, 4, 20, 0, 0, 47)),('cc8','svn','svn://20.26.19.70/home/svn/svn_repository/Program/script/helloword','*/8 * * * *','2016-04-20 00:00:00',datetime(2016, 4, 20, 0, 0, 47))]
    APPLIST = []
    tasknamelist = getjenkinstaskinfo()
    for i in data :
        APPLIST.append(str(i[0]))
        if str(i[0]) not in tasknamelist:
            #数据库存入 taskname,type, scmurl, poll, CREATEDATE, UPDATE_TIME
            servicesCreate(str(i[0]),str(i[1]),str(i[2]),str(i[3]),i[4],i[5])
            #插入jenkinsci表
            if str(i[1])=='svn' or str(i[1])=='git':
                
                savetask(str(i[0]))
            #name,type,scmurl, poll 创建jenkins任务
            appcicontroller.createjenkinstask(str(i[0]),str(i[1]),str(i[2]),str(i[3]))              
            print str(i[0])+ '      '+'save app'
        else:
            sql1 = "SELECT UPDATE_TIME,SCMURL,POLL,CODE_REPO_TYPE FROM jenkins_task where JOB_NAME='%s'"  %(i[0])
            j = sqlquery(sql1)

            if  not  str(i[5])== j[0][0]:
                
                if str(i[1])==j[0][3]:
                    if not str(i[2])== j[0][1] or not str(i[3])==j[0][2] or not str(i[1])==j[0][3]:
                        #taskname,type, scmurl, poll, CREATEDATE, UPDATE_TIME
                        update(str(i[0]),str(i[1]),str(i[2]),str(i[3]),i[4],i[5])
                        appcicontroller.updatajenkinstask(str(i[0]),str(i[1]),str(i[2]),str(i[3]))
                else:
                    update(str(i[0]),str(i[1]),str(i[2]),str(i[3]),i[4],i[5])
                    appcicontroller.updatajenkinstaskmodel(str(i[0]),str(i[1]),str(i[2]),str(i[3]))   
    runjenkinstask (APPLIST)
def getjenkinstaskinfo (): 
        tasknamelist=[] 
        session = get_session()
        data1 = session.query(JENKINS_TASK.JOB_NAME,JENKINS_TASK.SCMURL,JENKINS_TASK.POLL).all()
#         sql = "SELECT JOB_NAME,SCMURL,POLL FROM jenkinstask"
#         data1 = sqlquery(sql)
        for x in  data1:
            tasknamelist.append(x[0])
        session.close()    
        return tasknamelist       
def runjenkinstask (APPLIST): 
        tasknamelist=[]       
        sql2 = "SELECT JOB_NAME,SCMURL,POLL FROM jenkins_task"
        data2 = sqlquery(sql2)
        for x in  data2:
            if not  x[0]  in APPLIST:
                delete(x[0])
                appcicontroller.deletejenkinstask(x[0])
                
                print x[0]+'   '+'del x'


def gettaskstatus ():
    session = get_session()
    data = session.query(JENKINS_TASK.JOB_NAME,JENKINS_TASK.STATUS).all()
    for i in data:
        jobstatusdata = appcicontroller.getjobstatus(i[0])
        updatetaskstatus(i[0], jobstatusdata[0],jobstatusdata[1])
    
    return 'taskinfo' 
#     get
def sqlquery (sql):
#     cur = conn.cursor()
    conn = engine.execute(sql)
    data = conn.fetchall()
    conn.close()
    return data 
if __name__ == '__main__':
#     getservertaskinfo ()
    gettaskstatus()
     
#     create_database()
   
#     drop_database()