#! /usr/bin/env python

# ================
# filename: ipcheck.py
# author: Ganesh N. Sivalingam
# mail: g dot n dot sivalingam at gmail dot com
# github: https://github.com/gnsiva
# website: (tba)
# licence: GPLv2
# ================

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

# Storing command line arguments
printReport = opts.printreport
emailNewIp = not opts.noemail
dropboxNewIp = not opts.nodropbox
dropboxFile = opts.dbfile

#================================================================
# Globals
"""All of the associated files are to be kept in the same directory
as the script. The following gets their full paths.
"""
programDirectory = os.path.abspath(os.path.dirname(__file__))

current_ip_fn = os.path.join(programDirectory,'current_ip')
apppw_fn = os.path.join(programDirectory,'apppw')
emailaddr_fn = os.path.join(programDirectory,'emailaddr')
recipients_fn = os.path.join(programDirectory,'recipients')

#================================================================
# Functions

def findIp():
    """Gets external IP from internet (via icanhazip.com)
    in format 'xxx:xxx:xxx:xxx\n'.
    This may break if the server is taken down, should be easy
    enough to replace with a different service"""
    url = urllib.URLopener()

    resp = url.open('http://icanhazip.com/')
    ipadr = resp.readline()
    return ipadr

def createMessage(ipadr):
    msg = \
"""IP address has changed
The new address is:
%s""" %ipadr.rstrip('\n')
    return msg

def checkIp(ipadr):
    """Check whether same IP as last time
    returns True if IP has changed
    """

    # Open current_ip file, if doesn't exist make one
    try:
        rfid = open(current_ip_fn, 'r')
    except:
        rfid = open(current_ip_fn, 'w')
        rfid.close()
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
    """Gets email address, password and recipients list
    from file in the same folder as the script.
    One address per line for recipients.
    Files:
    emailaddr
    recipients
    apppw (password)
    """
    #Addresses and password
    fromaddr = open(emailaddr_fn,'r').readline().rstrip('\n')
    toaddrs  = [x.rstrip('\n') for x in open(recipients_fn,'r').readlines() if len(x) > 1]
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
    """Writes IP address to a file in dropbox
    Default is ~/Dropbox/ip
    Can be changed with CLI arguments
    """

    oFile = open(filename,'wb')
    print >> oFile, ipadr.rstrip('\n')
    oFile.close()

    if printReport:
        print 'Saved to Dropbox file:', dropboxFile


#================================================================
# Main

if __name__ == '__main__':
    ipadr = findIp()
    msg = createMessage(ipadr)


    if checkIp(ipadr):
        if printReport:
            print 'Different IP'

        if emailNewIp:
            sendEmail(msg)
        if dropboxNewIp:
            writeToDropboxFile(ipadr,dropboxFile)

        if printReport:
            print msg
    else:
        if printReport:
            print 'IP unchanged\n(%s)' %ipadr.rstrip('\n')

