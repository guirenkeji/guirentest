# -*- coding: UTF-8 -*-
import os
#######################ver2.0版本###############################
#icloud服务地址
icloudIP = '10.73.148.236'
icloudport = '8080'
#客户端服务端口号
serverclientport = 5015
#client下载节点IP地址在register文本统一手动输入ip地址
client = '0.0.0.0'
#jenkins服务地址
jenkinsserver = 'http://127.0.0.1:8080/jenkins'
#jenkinscollect服务地址
myserverip = '10.73.148.25'
myport = 5013
#mysql数据库配置
DB ='mysql+mysqlconnector://root:root@localhost:3306/icloud?charset=utf8'
#0关闭持续集成任务自动触发，1开启持续集成任务自动触发
trigger=0
#svn权限配置
svnuser = 'admin4'
svnpassword = '12345'

####################### ver1.0 版本 ############################
#icloud 下载地址
serverip1='http://20.26.17.145:8081/iCloud/upload'
#icloud json 下载地址
serverip2='http://20.26.17.145:8081/iCloud/json' 
scmurl = 'svn://20.26.19.69/home/svn/svn_repository/Program/script/helloword'
poll = 'H/5 * * * *'
#jenkinscollect
shell = 'sleep 5'
IP='127.0.0.1'   
# DB ='mysql+mysqlconnector://root:root@127.0.0.1:3306/dcos?charset=utf8'
# DB = 'oracle+cx_oracle://icloud:icloud@20.26.2.26/cloud'