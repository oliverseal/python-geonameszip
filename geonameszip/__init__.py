# -*- coding: utf-8 -*-
import csv, sqlite3, os

current_directory = os.path.dirname(os.path.realpath(__file__))
DEFAULT_SQLITE3_FILE = os.path.join(current_directory, 'zipcodes.sqlite3')

def utf_8_encoder(unicode_csv_data):
  for line in unicode_csv_data:
    yield line.encode('utf-8')

def import_from_file(source_txt):
  """Imports from a tab-delimited file."""
  conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
  try:
    # make the table.
    create_table(conn=conn)
  except sqlite3.OperationalError:
    # table probably existed
    print('Updating table postal_codes.')

  try:
    with open(source_txt, 'rb') as source:
      source_rows = csv.reader(utf_8_encoder(source), delimiter='\t', quotechar='\"')
      for row in source_rows:
        try:
          print(row)
          postal_code = unicode(row[1], 'utf-8')
          country = unicode(row[0], 'utf-8')
          region = unicode(row[2], 'utf-8')
          lat = unicode(row[3], 'utf-8')
          lon = unicode(row[4], 'utf-8')
          update_postal_code(postal_code, country, region, lat, lon, conn=conn)
        except IndexError:
          continue

  except IOError:
    print('Unable to open file "{0}".'.format(source_txt))


def lookup_postal_code(postal_code, conn=None):
  should_close = False
  if conn is None:
    conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
    should_close = True
  c = conn.cursor()
  try:
    c.execute('select postal_code, country, region, lat, lon from postal_codes where postal_code = ?', (postal_code,))
    result = c.fetchone()
    if should_close:
      conn.close()
    return result
  except:
    if should_close:
      conn.close()
    return None

def update_postal_code(postal_code, country, region, lat, lon, conn=None):
  should_close = False
  if conn is None:
    conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
    should_close = True
  c = conn.cursor()
  c.execute('insert into postal_codes (postal_code, country, region, lat, lon) values (?, ?, ?, ?, ?)', (postal_code, country, region, lat, lon))
  conn.commit()
  if should_close:
    conn.close()

def create_table(conn=None):
  should_close = False
  if conn is None:
    conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
    should_close = True
  c = conn.cursor()
  c.execute('create table postal_codes (postal_code, country, region, lat, lon)')
  conn.commit()
  if should_close:
    conn.close()


