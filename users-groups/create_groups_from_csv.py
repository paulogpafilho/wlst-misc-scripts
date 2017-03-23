"""
This is a  python script to create groups in a Weblogic Domain
This script requires a csv file containing the groups to be created in the following format:
  groupname, group description
You can also set the following environment variables:

CSV_FILE - The full path to the csv file containing groups
WLS_USER - The weblogic admin user used to connect to admin server
WLS_PASS - The weblogic admin user password
WLS_URL - The weblogic admin server URL. Should be in the format t3://HOST:PORT

To invoke this script, simply call WLST passing the script as argument.
For example:
/home/oracle/MW_HOME/common/bin/wlst.sh create_groups_from_csv.py
"""
import os, sys, fileinput
from weblogic.management.security.authentication import GroupEditorMBean

print '---- WLST Group Creation Start ----'
print ''
# Get the current path of the script and build the users cvs file - assuming they are in the same directory
dir_name =  os.path.dirname(sys.argv[0])
file_loc = os.path.join(dir_name, 'create_groups.csv')

# Location of the csv file, if not set will use delete_users.csv
csv_file = os.environ.get('CSV_FILE', file_loc)
# Weblogic admin user, if not set will use weblogic
wls_user = os.environ.get('WLS_USER', 'weblogic')
# Weblogic admin password, if not set will use Welcome1
wls_password = os.environ.get('WLS_PASS', 'Oracle123')
# Weblogic Admin Server URL, if not set will use t3://localhost:7001
wls_url = os.environ.get('WLS_URL', 't3://localhost:7001')

print 'Groups file to process: \'' + csv_file + '\''
print ''

# Connects to WLS Admin Server
connect(wls_user, wls_password, wls_url)
# Obtains the AuthenticatorProvider MBean
atnr = cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider("DefaultAuthenticator")

group = ''
description = ''
try:
  print 'Starting groups creation'
  print ''
  # Read the groups file
  for line in fileinput.input(csv_file):
    i = line.split(',')
    group = i[0].strip()
    description = i[1].strip()
    if not atnr.groupExists(group):
      print 'Creating group \'' + group + '\'...'
      try:
        atnr.createGroup(group, description)
      except weblogic.management.utils.InvalidParameterException, ie:
        print('Error while creating group')
        print str(ie)
        pass
      print 'Group \'' + group + '\' created successfully!'
      print ''
    else:
      print 'Group \'' + group + '\' already exist, skipping...'
      print ''
except StandardError, e:
  print 'Exception raised: ' + str(e)
  print 'Terminating script...'
print '---- WLST Group Creation End ----'