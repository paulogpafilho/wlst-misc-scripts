"""
This is a  python script to create users in a Weblogic Domain that uses the embedded LDAP.
The script needs to connect to a running Weblogic Admin Server.
This script requires a comma-separated-values (csv) file containing the users you wish to 
create, in the following format:

   username, password, description

Username and passoword are required. 

Passwords must contain at least 8 characters and either one numeric or special character.

The script will try to use the follow default values:

- Csv file name: will match the script file name with .csv extension.
  For example: create_users.csv. If not defined in the environment
  variables, the script will try to look at the same location where the script is
  running.
- Weblogic admin username: the weblogic admin user to connect to the admin server.
  Default value: weblogic
- Weblogic admin user password: admin user password to connect to the admin server.
  Default value: Welcome1
- Weblogic admin server URL: the admin server url and port, in the following format:
  t3://HOSTNAME:PORT. Default value: t3://localhost:7001

You can override the defaults by setting the following environment variables to:

CSV_FILE - The full path to the csv file containing users
WLS_USER - The weblogic admin user used to connect to admin server
WLS_PASS - The weblogic admin user password
WLS_URL - The weblogic admin server URL.

To invoke this script, simply call WLST passing the script full path as argument.
For example:
/home/oracle/MW_HOME/common/bin/wlst.sh create_users.py
"""

import os, sys, fileinput
from weblogic.management.security.authentication import UserEditorMBean

print '---- WLST User Creating Start ----\n'
# Get the current path of the script and build the users cvs file name
# assuming they are in the same directory
dir_name =  os.path.dirname(sys.argv[0])
file_name = os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.csv'
csv_file = os.path.join(dir_name, file_name)

# Location of the csv file, if not set will use users.csv
csv_file = os.environ.get('CSV_FILE', csv_file)
# Weblogic admin user, if not set will use weblogic
wls_user = os.environ.get('WLS_USER', 'weblogic')
# Weblogic admin password, if not set will use Welcome1
wls_password = os.environ.get('WLS_PASS', 'Oracle123')
# Weblogic Admin Server URL, if not set will use t3://localhost:7001
wls_url = os.environ.get('WLS_URL', 't3://localhost:7001')

print 'Users file to process: \'' + csv_file + '\'\n'

# Connects to WLS Admin Server
connect(wls_user, wls_password, wls_url)
# Obtains the AuthenticatorProvider MBean
atnr = cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider("DefaultAuthenticator")

# Read the users file
username = ''
password = ''
description = ''
try:
  print 'Starting users creation\n'
  for line in fileinput.input(csv_file):
    i = line.split(',')
    username = i[0].strip()
    password = i[1].strip()
    description = i[2].strip()
    if not atnr.userExists(username):
      print 'Creating user \'' + username + '\'...'
      try:
        atnr.createUser(username, password, description)
        print 'User \'' + username + '\' created successfully!'
      except weblogic.management.utils.InvalidParameterException, ie:
        print('Error while creating the user\n')
        print str(ie)
        pass
    else:
      print 'User \'' + username + '\' already exists, skipping...\n'
except StandardError, e:
  print 'Unexpected Exception raised: ' + str(e)
  print 'Terminating script...'
print '---- WLST User Creating End ----'