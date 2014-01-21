================================================================
= IP Check
= Author: Ganesh N. Sivalingam

IP Check is a program for automatically notifying you of changes in
your external IP address. This allows you to connect to services on
your machine such as ssh and subsonic, if the server is on and 
accessible then you will be kept up to date on its address!
It can email you changes in IP and/or save changes to a file in
Dropbox so you will always have access.

Run the following for help on available options:
python ipcheck.py -h



================================================================
= Setup/Installation

***It is recommended that you create a new gmail account for this
program to reduce security risks.***

1. Add a file called "emailaddr" in this directory and put the email 
address you want to send IP changes FROM on the first line. 

2. Create a file called "apppw" in this directory and put the 
password for the email account in there on the first line.

3. Create a file called "recipients" also in this directory. In this 
file put all the email addresses you wish to send the IP address to
one per line.

4. Run the script to test it works. From this directory run:
you@yourcomputer$ python ipcheck.py -p
A file called current_ip should be updated to your external IP,
your recipients should receive an email with the IP and as long as
you have Dropbox installed in the default directory a file called "ip"
will be added containing your IP.

5. Add to cron so that the computer automatically runs the script 
periodically.
To add something to crontab enter:
you@yourcomputer$ crontab -e

To make the script run every 5 minutes enter this at the bottom of the
file:

*/5 * * * * python /absolute/path/to/this/directory/ipcheck.py


