"""
This is a  python script to create groups in a Weblogic Domain that uses the embedded LDAP.
The script needs to connect to a running Weblogic Admin Server.
This script requires a comma-separated-values (csv) file containing the groups you wish to 
create, in the following format:

   groupname, group description

Groupname is required.

The script will try to use the follow default values:

- Csv file name: will match the script file name with .csv extension.
  For example: create_groups.csv. If not defined in the environment
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
/home/oracle/MW_HOME/common/bin/wlst.sh create_groups.py
"""
import os, sys, fileinput
from weblogic.management.security.authentication import GroupEditorMBean

print '---- WLST Group Creation Start ----\n'
# Get the current path of the script and build the users cvs file name
# assuming they are in the same directory
dir_name =  os.path.dirname(sys.argv[0])
file_name = os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.csv'
csv_file = os.path.join(dir_name, file_name)

# Location of the csv file, if not set will use delete_users.csv
csv_file = os.environ.get('CSV_FILE', csv_file)
# Weblogic admin user, if not set will use weblogic
wls_user = os.environ.get('WLS_USER', 'weblogic')
# Weblogic admin password, if not set will use Welcome1
wls_password = os.environ.get('WLS_PASS', 'Welcome1')
# Weblogic Admin Server URL, if not set will use t3://localhost:7001
wls_url = os.environ.get('WLS_URL', 't3://localhost:7001')

print 'Groups file to process: \'' + csv_file + '\'\n'

# Connect to WLS Admin Server
connect(wls_user, wls_password, wls_url)
# Obtain the AuthenticatorProvider MBean
atnr = cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider("DefaultAuthenticator")

group = ''
description = ''
try:
  print 'Starting groups creation\n'
  # Read the csv file
  for line in fileinput.input(csv_file):
    # Split the line by comma
    i = line.split(',')
    # Get the group name
    group = i[0].strip()
    # Get the group description
    description = i[1].strip()
    # If the group does not exist
    if not atnr.groupExists(group):
      print 'Creating group \'' + group + '\'...'
      try:
        # Create the group
        atnr.createGroup(group, description)
      except weblogic.management.utils.InvalidParameterException, ie:
        print('Error while creating group')
        print str(ie)
        pass
      print 'Group \'' + group + '\' created successfully!\n'
    else:
      print 'Group \'' + group + '\' already exist, skipping...\n'
except StandardError, e:
  print 'Exception raised: ' + str(e)
  print 'Terminating script...'
print '---- WLST Group Creation End ----'