import cx_Oracle
from flask import Flask,request,jsonify,render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText,SMALLINT,Sequence
import os
import json
from marathon import MarathonClient
from time import sleep
from pip._vendor.distlib._backport.tarfile import TUREAD
from imageop import scale
from werkzeug import secure_filename
from testjmeterconfig import *
app = Flask(__name__)
engine = create_engine(DB,echo=True)
app.config['UPLOAD_FOLDER'] = 'templates'
app.config['MAX_CONTENT_LENGTH'] = 16<<20  # max upload size < 16M
BaseModel = declarative_base()
c = MarathonClient(marathonip,username=user,password=password)
@app.route('/')
def hello_jmeter():
    return 'Hello jmeter!'
@app.route('/jmeter/<jmeter>')
def jmeterconfig(jmeter):
#      curl -i -X POST -H "Content-Type: application/json" -d '{"taskcasename":"'testcat'","jmxname":"'jmxname'","threads": 5,"rampup": 5,"threadloop": 5,"scale": 5}' 127.0.0.1:5000/jmeter
#     jmeter = 'taskcasename=testcat&jmxname=jmxname&threads=5&rampup=5&threadloop=5&scale=5'
    jmeterlist = jmeter.split('&')
    print jmeterlist
    list = []
    for i in jmeterlist:
        p = i.split('=')
        p = p[1] 
        l = list.append(p)
    if  exist_category(list[0])==True:
        return "0"
    else:
    
        (taskcasename,jmxname,threads,rampup,threadloop,SCALE) =tuple(list)  
#     taskcasename =request.json['taskcasename']
#     jmxname =request.json['jmxname']
#     threads =request.json['threads']
#     rampup =request.json['rampup']
#     threadloop =request.json['threadloop']
#     SCALE = request.json['scale']
        servicesCreate(taskcasename,jmxname,int(threads),int(rampup),int(threadloop),int(SCALE))
    
    
    return 'Hello jmeter!!!' 
@app.route('/jmeter/run/<id>')
def testcaserun(id):
#     c = MarathonClient(marathonip)
#     taskcasename = request.json['taskcasename']
    taskcasename = 'abc2'
    readed = json.load(open('temp.json', 'r'))
    readed['container']['docker']['image'] = dockerimage
    readed['id'] = taskcasename
    json.dump(readed, open('testcaseapp.json', 'w'))  
    os.system ('curl -u dcosadmin:zjdcos01 -X POST -H "Content-Type: application/json" %s/v2/apps -d@testcaseapp.json' %(marathonip))
#     task = c.list_tasks('myjenkins')
    taskcase = get(taskcasename)
    SCALE = taskcase.SCALE
    print SCALE
    sleep(10)
    c.scale_app(taskcasename,instances=SCALE)
    return 'ok'
def get(taskcasename):
    session = get_session()
    taskcase = session.query(TEST_TASK).filter(TEST_TASK.TaskCaseName == taskcasename).one()
    return taskcase 
def count():
    session = get_session()
    num = session.query(TEST_TASK).count()
    return num
#     return taskcase 
def gettaskcasename(id):
    session = get_session()
    taskcase = session.query(TEST_TASK).filter(TEST_TASK.TestTaskId == id).one()
    return taskcase 

def testcasecreate():
    return 'ok'
@app.route('/jmeter/stop/<taskcasename>')
def testcasestop(taskcasename):
#     taskcasename = request.json['taskcasename']
    taskcasename = 'testcat'
    c.scale_app(taskcasename,instances=0)
    return True
@app.route('/jmeter/delete/<taskcasename>')    
def testcasedelete():
#     app_id = request.json['taskcasename']
    app_id = 'testcat'
    c.delete_app(app_id, force=True)
    return True
@app.route('/jmeter/update/<updatecontent>')
def testcaseupdate(updatecontent):
    updatecontentlist = updatecontent.split('&')
    list = []
    for i in updatecontentlist:
        p = i.split('=')
        p = p[1] 
        l = list.append(p)
    (taskcasename,jmxname,threads,rampup,threadloop,SCALE) =tuple(list) 
    task = update(id,taskcasename,jmxname,threads,rampup,threadloop,SCALE)
    return 'ok'
def create_database():
    BaseModel.metadata.create_all(bind=engine)
def drop_database():
    BaseModel.metadata.drop_all(bind=engine)
def get_session():
    
    return Session(bind = engine)
class TEST_TASK(BaseModel):

    __tablename__ = 'TEST_TASK'
    TestTaskId = Column('TestTaskId', Integer,primary_key=True,nullable=False,autoincrement=True)
    TaskCaseName = Column('TaskCaseName', NVARCHAR(200),nullable = False)
    JmxName = Column('JmxName', NVARCHAR(600),nullable = False)
    Threads = Column('Threads', Integer,nullable=False)
    RampUp = Column('RampUp', Integer,nullable=False)
    ThreadLoop = Column('ThreadLoop', Integer,nullable=False)
    SCALE = Column('SCALE', Integer,nullable=False)

def servicesCreate(taskcasename,jmxname,threads,rampup,threadloop,scale):
#     database = get_session()
    session = get_session()
    T = TEST_TASK()
    num = count()+1   
    T.TestTaskId = num 
    T.TaskCaseName = taskcasename
    T.JmxName = jmxname
    T.Threads = threads
    T.RampUp = rampup
    T.ThreadLoop = threadloop
    T.SCALE = scale
    session.add(T)
    session.commit()
    session.close()
def delete(id):
    session = get_session()
    session.query(TEST_TASK).filter(TEST_TASK.TestTaskId == id).delete()
    session.commit()
    session.close()    
def update(id,taskcasename,jmxname,threads,rampup,threadloop,scale):
#     taskcasename ='cc'
    session = get_session()

    task = session.query(TEST_TASK).filter(TEST_TASK.TestTaskId == id).update({'TaskCaseName':taskcasename,'JmxName':jmxname,'Threads':threads,'RampUp':rampup,'ThreadLoop':threadloop,'SCALE':scale})

    session.commit()
    session.close()
@app.route('/jmeter/remoteclient',methods=['POST'])    
def remoteclient():
    taskcasename = request.json['taskcasename']
    taskcasename = taskcasename[1:]
    session = get_session()
    taskcase = session.query(TEST_TASK).filter(TEST_TASK.TaskCaseName == taskcasename).one()
#     jmxname= taskcase.JmxName
    return jsonify({'JmxName':taskcase.JmxName,'Threads':taskcase.Threads,'RampUp':taskcase.RampUp,'ThreadLoop':taskcase.ThreadLoop,'SCALE':taskcase.SCALE})    
def exist_category(name):
    session = get_session()

    c = session.query(TEST_TASK).filter(TEST_TASK.TaskCaseName == name).count()

    session.close()
    return c > 0  
@app.route('/jmeter/jmx', methods=['POST'])
def upload_file():
    file = request.files['file']
    app.config['UPLOAD_FOLDER'] ='c:/tool'
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'upload success' 
@app.route('/jmeter/jmx/tmp/<file>')
def viewfile(file):
    
    return render_template(file)  
if __name__ == '__main__':
#     get("tt")
#     update(id)
#     drop_database()
#     create_database()
#     count()
#     testcasedelete()
#     testcasestop()
#     testcaserun()
#     app.run(host= '10.70.86.66',port=5001)
#     app.run(host= '10.73.144.234',port=5001)
    app.run(host= '0.0.0.0',port=5001)