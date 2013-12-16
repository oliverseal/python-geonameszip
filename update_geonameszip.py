#!/usr/bin/env python
import os, sys, urllib2, math, time, zipfile
from geonameszip import update

if len(sys.argv) > 1 and sys.argv[1] == '-f':
  do_import = 'y'
  force = True
else:
  do_import = 'n'
  force = False

now = time.time()
try:
  created_time = os.path.getctime(update.DOWNLOADED_ZIP_FILE)
except OSError:
  created_time = now - 90000

# only download if it's greater than a day
if now - created_time > 86400 and force is False:
  do_import = raw_input('This will download the latest zip file from geonames and import it into the default zipcode database. Please do not abuse this since geonames offers this data _for free_. Continue? Y/n')
elif force is False:
  do_import = 'n'
  print('Previously downloaded file is less than 24 hours old -- using it.')

if do_import.lower() == 'y':
  update.download()

update.import_downloaded_file()
