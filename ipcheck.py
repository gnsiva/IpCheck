#! /usr/bin/env python
import urllib
import smtplib
from datetime import datetime

#================================================================
# Functions

def findIP():
    url = urllib.URLopener()

    resp = url.open('http://icanhazip.com/')
    html = resp.readline()
    msg = 'Home IP is \n' + html
    return msg, html

def checkIP(ipadr):
    #Check whether same IP as last time, if not then don't email.
    rfid = open('current_ip', 'r')
    old_ip = rfid.readline()
    rfid.close()
    if ipadr != old_ip:
        wfid = open('current_ip', 'w')
        wfid.write(ipadr)
        return True
    else:
        return False

def sendEmail(msg):
    #Addresses
    fromaddr = 'g.n.sivalingam@gmail.com'
    toaddrs  = ['g.n.sivalingam@gmail.com','manpageexplorer@gmail.com']

    # Credentials (if needed)
    username = 'g.n.sivalingam@gmail.com'
    password = open('apppw','r').readline()

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    for toad in toaddrs:
        server.sendmail(fromaddr, toad, msg)
    server.quit()

    print 'Sent to', toaddrs

#================================================================
# Main

msg, ipadr = findIP()
print msg
if checkIP(ipadr):
    print 'Different IP, send email'
    sendEmail(msg)
else:
    print 'Same IP, dont send'
