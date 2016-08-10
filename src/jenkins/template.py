import os
jenkinsconfigfile = u"""<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
    <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>STRING</name>
          <description></description>
          <defaultValue></defaultValue>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.SubversionSCM" plugin="subversion@1.54">
    <locations>
      <hudson.scm.SubversionSCM_-ModuleLocation>
        <remote>%SVNPATH%</remote>
        <local>.</local>
        <depthOption>infinity</depthOption>
        <ignoreExternalsOption>false</ignoreExternalsOption>
      </hudson.scm.SubversionSCM_-ModuleLocation>
    </locations>
    <excludedRegions></excludedRegions>
    <includedRegions></includedRegions>
    <excludedUsers></excludedUsers>
    <excludedRevprop></excludedRevprop>
    <excludedCommitMessages></excludedCommitMessages>
    <workspaceUpdater class="hudson.scm.subversion.UpdateUpdater"/>
    <ignoreDirPropChanges>false</ignoreDirPropChanges>
    <filterChangelog>false</filterChangelog>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers>
    <hudson.triggers.SCMTrigger>
      <spec>%POLL%</spec>
      <ignorePostCommitHooks>false</ignorePostCommitHooks>
    </hudson.triggers.SCMTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>%SHELL%</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>"""
# helloword =u"""
# # -*- coding: UTF-8 -*- 
# import os
# from flask import Flask,request,url_for
# from datetime import datetime
# app = Flask(__name__)
# @app.route('/')
# def helloword():
#     return '%hello%'
# if __name__ == '__main__':
#     app.run(host= '0.0.0.0',port=5004)"""