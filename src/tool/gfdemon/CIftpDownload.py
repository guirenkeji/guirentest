#!/usr/bin/env python

import ftplib 

ftp = ftplib.FTP()  
FTPIP= "10.70.41.126"
FTPPORT= 21
USERNAME= "joy"
USERPWD= "go2hell"
ftp.connect(FTPIP, FTPPORT)  
ftp.login(USERNAME,USERPWD)  
ftp.set_pasv(0)
CURRTPATH= "/Temp/dnt/zsh"
ftp.cwd(CURRTPATH)  
DownLocalFilename="hadoop.tar"
f = open(DownLocalFilename, 'wb')   
DownRemoteFilename="hadoop.tar"
ftp.retrbinary('RETR ' + DownRemoteFilename , f.write , 1024)  
f.close()  
ftp.close()