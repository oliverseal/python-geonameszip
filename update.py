#!/usr/bin/env python
import os, sys, urllib2, terminal, math, time

DOWNLOAD_URL = 'http://download.geonames.org/export/zip/allCountries.zip'
#DOWNLOAD_URL = 'http://www.google.com/'
current_directory = os.path.dirname(os.path.realpath(__file__))

do_import = raw_input('This will download the latest zip file from geonames and import it into the default zipcode database. Please do not abuse this since geonames offers this data _for free_. Continue? Y/n')

if do_import.lower() == 'y':
  file = os.path.join(os.path.join(current_directory, 'allCountries.zip'))

  now = time.time()
  try:
    created_time = os.path.getctime(file)
  except OSError:
    print('Creating file...')
    created_time = now - 90000

  # only download if it's greater than a day
  if now - created_time > 86400:
    def on_data_recieved(bytes_downloaded, chunk_size, total_size):
      complete = round((float(bytes_downloaded)/total_size) * 100, 2)
      complete_string = '{0}%'.format(complete)
      cols = terminal.get_terminal_size()[0]
      progress_bar_total_cols = cols - 16 - len(complete_string)
      progress_bar_complete_cols = math.floor(progress_bar_total_cols*(complete/100))
      progress_bar_gap_cols = progress_bar_total_cols - progress_bar_complete_cols
      progress_bar = ''.ljust(int(progress_bar_complete_cols), '#')
      progress_gap = ''.ljust(int(progress_bar_gap_cols), ' ')
      sys.stdout.write('Downloaded:[{0} {1}{2}]\r'.format(progress_bar, complete_string, progress_gap))
      sys.stdout.flush()

    with open(file, 'wb') as fh:
      response = urllib2.urlopen(DOWNLOAD_URL)
      size_header = response.info().getheader('Content-Length')
      if size_header is not None:
        size = int(size_header.strip())
      else:
        size = 0
      chunk_size = 8192
      complete = 0

      while 1:
        chunk = response.read(chunk_size)
        complete += len(chunk)

        if not chunk:
          break

        fh.write(chunk)
        if size != 0:
          on_data_recieved(complete, chunk_size, size)

  else:
    print('Previously downloaded file is less than 24 hours old -- using it.')



