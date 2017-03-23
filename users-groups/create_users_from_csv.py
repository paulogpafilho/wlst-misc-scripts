"""
This is a  python script to create users in WLS DefaultAuthenticator/EmbeddedLDAP
This script requires a csv file containing the users to be created in WLS with the following format:
username, password, description
You can also set the following environment variables:
CSV_FILE - The full path to the csv file containing users and passwords
WLS_USER - The weblogic admin user used to connect to admin server
WLS_PASS - The weblogic admin user password
WLS_URL - The weblogic admin server URL. Should be in the format t3://HOST:PORT
To invoke this script, simply call WLST passing the script as argument.
For example:
/home/oracle/MW_HOME/common/bin/wlst.sh create_users_from_csv.py
"""
import os, sys, fileinput
from weblogic.management.security.authentication import UserEditorMBean

print '---- WLST User Creating Start ----'
print ''
# Get the current path of the script and build the users cvs file - assuming they are in the same directory
dir_name =  os.path.dirname(sys.argv[0])
file_loc = os.path.join(dir_name, 'create_users.csv')
# Location of the csv file, if not set will use users.csv
csv_file = os.environ.get('CSV_FILE', file_loc)
# Weblogic admin user, if not set will use weblogic
wls_user = os.environ.get('WLS_USER', 'weblogic')
# Weblogic admin password, if not set will use Welcome1
wls_password = os.environ.get('WLS_PASS', 'Oracle123')
# Weblogic Admin Server URL, if not set will use t3://localhost:7001
wls_url = os.environ.get('WLS_URL', 't3://localhost:7001')

print 'Users file to process: \'' + csv_file + '\''
print ''

# Connects to WLS Admin Server
connect(wls_user, wls_password, wls_url)
# Obtains the AuthenticatorProvider MBean
atnr = cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider("DefaultAuthenticator")

# Read the users file
username = ''
password = ''
description = ''
try:
  print 'Starting users creation'
  print '' 
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
        print('Error while creating the user')
        print str(ie)
        pass
      print ''
    else:
      print 'User \'' + username + '\' already exists, skipping...'
      print ''
except StandardError, e:
  print 'Unexpected Exception raised: ' + str(e)
  print 'Terminating script...'
print '---- WLST User Creating End ----'