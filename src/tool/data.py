#!/usr/bin/python
import os
import socket

if __name__ == '__main__':
    SERVER_NAME = socket.gethostname()
    SERVER_IP_ADDR = socket.gethostbyaddr(SERVER_NAME)[2][0]
    SERVER_STATUS = 1
    if SERVER_NAME[1] == "s":
        DATACENTER_NAME = "sd"
    ContainerInfo = {}
    Info = os.popen("docker ps | egrep -v 'CONTAINER|mesos:1|haproxy|zookeeper|marathon' | awk '{print $2}' | awk -F '/' '{print $2}' | awk -F ':' '{print $1}' | sort | uniq -c").read().splitlines()
    DATACENTER = {}
    for i in Info:
        CONTAINER_COUNTS = i.split()[0]
        APPLICATION_CATAGORY = i.split()[1]
        print SERVER_NAME,DATACENTER_NAME,SERVER_IP_ADDR,APPLICATION_CATAGORY,CONTAINER_COUNTS,SERVER_STATUS