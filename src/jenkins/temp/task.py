# -*- coding: utf-8 -*-
import os
from analysisxml import find_nodes,get_node_by_keyvalue,read_xml,write_xml,change_node_text
import jconfig
import appcicontroller
from time import sleep
def createtask (name,type,scmurl, poll,shell,string):
    createxml(name, type, scmurl, poll, shell,string)
    try:
        cmd1 =os.popen ('curl -X POST %s/createItem?name=%s  -d"@./temp/%sconfig.xml"  --connect-timeout 10 -H "Content-Type: text/xml"' 
                          %(jconfig.jenkinsserver,name,name)).readlines()
        sleep(3)                  
        if 'return false' in cmd1:
            return "create jenkins task error"
        if not cmd1 == []:
            return "create jenkins task error"
        else:
            if jconfig.trigger==0:
                 appcicontroller.stopjenkinstask(name) 
            return "create jenkins task ok"
    except Exception,e:
            print e   
def updatetask (name,type,scmurl, poll,shell):
    updatexml(name, type, scmurl, poll, shell)
    try:
        cmd1 =os.popen ('curl -X POST %s/job/%s/config.xml  -d"@./temp/%sconfig.xml"  --connect-timeout 10  -H "Content-Type: text/xml"'  %(jconfig.jenkinsserver,name,name)).readlines()
        if jconfig.trigger==0:
                              
            appcicontroller.stopjenkinstask(name)
        if 'return false' in cmd1:
            return "create jenkins task error"
        if not cmd1 == []:
            return "create jenkins task error"
        else:
            return "update jenkins task ok" 
    except Exception,e:
            print "update jenkins configures",e 
#svn和git 模板更新,重新创建一个xml模板文件              
def updatescmtypetask (name,type,scmurl, poll,shell,string):
    createxml(name, type, scmurl, poll, shell,string)
    try:
        cmd1 =os.popen ('curl -X POST %s/job/%s/config.xml  -d"@./temp/%sconfig.xml"  --connect-timeout 10  -H "Content-Type: text/xml"'  %(jconfig.jenkinsserver,name,name)).readlines()
        if jconfig.trigger==0:
                              
            appcicontroller.stopjenkinstask(name)
        if 'return false' in cmd1:
            return "create jenkins task error"
        if not cmd1 == []:
            return "create jenkins task error"
        else:
            return "update jenkins task ok" 
    except Exception,e:
            print "update jenkins configures",e                       
def createxml (name,type,scmurl, poll,shell,string): 
#     name =''
#     type ='svn'
#     scmurl = ''
#     poll = ''
#     shell = ''
    if type == 'svn':
        try:
            tree = read_xml("./temp/svnconfig.xml")
            tscmurl = get_node_by_keyvalue(find_nodes(tree, "scm/locations/hudson.scm.SubversionSCM_-ModuleLocation/remote"), "scmurl")  
            tshell = get_node_by_keyvalue(find_nodes(tree, "builders/hudson.tasks.Shell/command"),"shell")  
            tpoll = get_node_by_keyvalue(find_nodes(tree, "triggers/hudson.triggers.SCMTrigger/spec"),"spec") 
            tstring = get_node_by_keyvalue(find_nodes(tree, "properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition/defaultValue"),"string")  
            change_node_text(tscmurl, scmurl)
            change_node_text(tshell, shell)
            change_node_text(tpoll, poll)
            change_node_text(tstring, string)
            write_xml(tree, "./temp/%sconfig.xml" %(name))
            print ""
        except Exception,e:
            print e
    if type=='git':
            tree = read_xml("./temp/gitconfig.xml")
            tscmurl = get_node_by_keyvalue(find_nodes(tree, "scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url"), "scmurl")  
            tshell = get_node_by_keyvalue(find_nodes(tree, "builders/hudson.tasks.Shell/command"),"shell")  
            tpoll = get_node_by_keyvalue(find_nodes(tree, "triggers/hudson.triggers.SCMTrigger/spec"),"spec")  
            tstring = get_node_by_keyvalue(find_nodes(tree, "properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition/defaultValue"),"string")  
            change_node_text(tscmurl, scmurl)
            change_node_text(tshell, shell)
            change_node_text(tpoll, poll)
            change_node_text(tstring, string)
            write_xml(tree, "./temp/%sconfig.xml" %(name))
            print ""
def updatexml (name,type,scmurl, poll,shell): 

    if type == 'svn':
        try:
            tree = read_xml("./temp/%sconfig.xml" %(name))
            tscmurl = get_node_by_keyvalue(find_nodes(tree, "scm/locations/hudson.scm.SubversionSCM_-ModuleLocation/remote"), "scmurl")  
            tshell = get_node_by_keyvalue(find_nodes(tree, "builders/hudson.tasks.Shell/command"),"shell")  
            tpoll = get_node_by_keyvalue(find_nodes(tree, "triggers/hudson.triggers.SCMTrigger/spec"),"spec") 
#             tstring = get_node_by_keyvalue(find_nodes(tree, "properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition/defaultValue"),"string")  
            change_node_text(tscmurl, scmurl)
            change_node_text(tshell, shell)
            change_node_text(tpoll, poll)
#             change_node_text(tstring, string)
            write_xml(tree, "./temp/%sconfig.xml" %(name))
            print ""
        except Exception,e:
            print e
    if type=='git':
            tree = read_xml("./temp/%sconfig.xml" %(name) )
            tscmurl = get_node_by_keyvalue(find_nodes(tree, "scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url"), "scmurl")   
            tshell = get_node_by_keyvalue(find_nodes(tree, "builders/hudson.tasks.Shell/command"),"shell")  
            tpoll = get_node_by_keyvalue(find_nodes(tree, "triggers/hudson.triggers.SCMTrigger/spec"),"spec")  
#             tstring = get_node_by_keyvalue(find_nodes(tree, "properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition/defaultValue"),"string")  
            change_node_text(tscmurl, scmurl)
            change_node_text(tshell, shell)
            change_node_text(tpoll, poll)
#             change_node_text(tstring, string)
            write_xml(tree, "./temp/%sconfig.xml" %(name))
            print ""
                                
if __name__ == '__main__':
    tt= createtask ('','','','','') 
#      updatetask ()  
    print tt         