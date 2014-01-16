#!/usr/bin/python



# See whats printed (program name is first (0'th) argv)
# for arg in sys.argv:
#     print arg


helpString = \
"""IP checker program:
Allows regular checks of external IP address (using cron)
and when the IP changes it can email the new IP and/or
save it in a Dropbox file to ensure you always have and
up to date IP to connect to your network.
"""

import optparse,os

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

print opts.printreport
print opts.noemail

print opts.nodropbox
print opts.dbfile


print '================'
print os.getcwd()
print os.path.dirname(os.path.relpath(__file__))
print os.path.dirname(__file__)
