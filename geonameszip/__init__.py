import csv
import sqlite3

DEFAULT_SQLITE3_FILE = 'zipcodes.sqlite3'

def import_from_file(source_txt):
  """Imports from a tab-delimited file."""
  conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
  # make the table.
  create_table(conn=conn)
  try:
    with open(source_txt, 'rb') as source:
      source_rows = csv.reader(source_txt, delimiter='\t', quotechar='\"')
      for row in source_rows:
        postal_code = row[1]
        country = row[0]
        region = row[2]
        lat = row[3]
        lon = row[4]
        update_postal_code(postal_code, country, region, lat, lon, conn=conn)

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


