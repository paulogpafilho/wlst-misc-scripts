"""
This is a  python script to edit users properties in a Weblogic Domain that uses the embedded LDAP.
The script needs to connect to a running Weblogic Admin Server.
This script requires a comma-separated-values (csv) file containing the user's properties to be 
edited in the following format:

  username, c, departmentnumber, displayname, employeenumber, employeetype, 
  facsimiletelephonenumber, givenname, homephone, homepostaladdress, l, mail, mobile, pager, 
  postaladdress, postofficebox, preferredlanguage, st, street, telephonenumber, title

Username is the only required value, others are optional.

The script will try to use the follow default values:

- Csv file name: will match the script file name with .csv extension.
  For example: edit_user_properties.csv. If not defined in the environment
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
/home/oracle/MW_HOME/common/bin/wlst.sh edit_user_properties.py
"""
import os, sys, fileinput
from weblogic.management.security.authentication import UserEditorMBean

print '---- WLST User Edit Start ----\n'
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
wls_password = os.environ.get('WLS_PASS', 'Welcome1')
# Weblogic Admin Server URL, if not set will use t3://localhost:7001
wls_url = os.environ.get('WLS_URL', 't3://localhost:7001')

print 'Users file to process: \'' + csv_file + '\'\n'

# Connect to WLS Admin Server
connect(wls_user, wls_password, wls_url)

# Obtain the AuthenticatorProvider MBean
atnr = cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider("DefaultAuthenticator")

props = ['c', 'departmentnumber', 'displayname', 'employeenumber', 'employeetype', 
  'facsimiletelephonenumber', 'givenname', 'homephone', 'homepostaladdress', 'l', 'mail', 'mobile', 'pager', 
  'postaladdress', 'postofficebox', 'preferredlanguage', 'st', 'street', 'telephonenumber', 'title']

username = ''
try:
  print 'Starting users deletion \n'
  # Read the csv file
  for line in fileinput.input(csv_file):
    # Split the file by comma
    ln = line.split(',')
    # get the username and trims the trailings spaces
    username = ln[0].strip()
    # Check if user exists in the LDAP
    if atnr.userExists(username):
      print 'Setting user \'' + username + '\' properties...'
      try:
        for j, jval in enumerate(props):  
          # Check if the property is not blank        
          if ln[j+1].strip() != '':
            # Change the user property in the LDAP
            atnr.setUserAttributeValue(username, jval, ln[j+1].strip())
      except weblogic.management.utils.InvalidParameterException, ie:
        print('Error while editing \'' + username  + '\' properties')
        print str(ie)
        pass
      print 'User \'' + username + '\' properties edited successfully!\n'
    else:
      print 'User \'' + username + '\' does not exist, skipping...\n'
except StandardError, e:
  print 'Exception raised: ' + str(e)
  print 'Terminating script...'
print '---- WLST User Edit End ----'