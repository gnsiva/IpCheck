#! /usr/bin/python
import urllib
import smtplib
import os,optparse
from datetime import datetime

#================================================================
# Command line interface
helpString = \
"""IP checker program:
Allows regular checks of external IP address (using cron)
and when the IP changes it can email the new IP and/or
save it in a Dropbox file to ensure you always have and
up to date IP to connect to your network.
"""

parser = optparse.OptionParser(description=helpString,version='%prog version 0.9')

parser.add_option('-p','--printreport',dest='printreport',default=False,action='store_true',
                  help='Print run report (should be disabled for cron usuage)')

parser.add_option('-e','--noemail',dest='noemail',default=False,action='store_true',
                  help='Do not email IP changes')


parser.add_option('-d','--nodropbox',dest='nodropbox',default=False,action='store_true',
                  help='Do not save IP in Dropbox folder (default is ~/Dropbox/ip)')

parser.add_option('--dbfile',dest='dbfile',default='%s/Dropbox/ip' %os.path.expanduser('~'),
                  help='Use alternate file for Dropbox save functionality (e.g. /home/user/Dropbox/ip)')

(opts,args) = parser.parse_args()

# Storing Options
printReport = opts.printreport
emailNewIp = not opts.noemail
dropboxNewIp = not opts.nodropbox
dropboxFile = opts.dbfile

#================================================================
# Globals
programDirectory = os.path.dirname(__file__)

current_ip_fn = os.path.join(programDirectory,'current_ip')
apppw_fn = os.path.join(programDirectory,'apppw')
emailaddr_fn = os.path.join(programDirectory,'emailaddr')
recipients_fn = os.path.join(programDirectory,'recipients')

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
    rfid = open(current_ip_fn, 'r')
    old_ip = rfid.readline()
    rfid.close()
    if ipadr != old_ip:
        wfid = open(current_ip_fn, 'w')
        wfid.write(ipadr)
        return True
    else:
        return False

def sendEmail(msg):
    #Addresses and password
    fromaddr = open(emailaddr_fn,'r').readline().rstrip('\n')
    toaddrs  = [x.rstrip('\n') for x in open(recipients_fn,'r').readlines()]
    password = open(apppw_fn,'r').readline()

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(fromaddr,password)
    for toad in toaddrs:
        server.sendmail(fromaddr, toad, msg)
    server.quit()

    if printReport:
        print 'Sent to', toaddrs

def writeToDropboxFile(ipadr,filename):
    # TODO - add try catch to make sure file opened correctly

    oFile = open(filename,'wb')
    print >> oFile, ipadr.rstrip('\n')
    oFile.close()

    if printReport:
        print 'Saved to Dropbox file:', dropboxFile


#================================================================
# Main

msg, ipadr = findIP()

if printReport:
    print msg

if checkIP(ipadr):
    if printReport:
        print 'Different IP'

    if emailNewIp:
        sendEmail(msg)
    if dropboxNewIp:
        writeToDropboxFile(ipadr,dropboxFile)
else:
    if printReport:
        print 'IP unchanged'

#================================================================
# Bash alias for remote access
#alias athenaRemote="ssh -XY -p 9999 gns@$(cat ~/Dropbox/ip)"
#alias <yournickname>="ssh -XY <username>@$(cat <yourDropboxFileLocation>)"
