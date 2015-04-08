# -*- coding: utf-8 -*-
import csv, codecs, sqlite3, os, sys

if os.name == 'nt':
  import ctypes
  from ctypes import wintypes, windll

  CSIDL_COMMON_APPDATA = 35

  _SHGetFolderPath = windll.shell32.SHGetFolderPathW
  _SHGetFolderPath.argtypes = [wintypes.HWND, ctypes.c_int,
                               wintypes.HANDLE, wintypes.DWORD,
                               wintypes.LPCWSTR]
  path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
  _SHGetFolderPath(0, CSIDL_COMMON_APPDATA, 0, 0, path_buf)
  BASE_DIR = path_buf.value
else:
  BASE_DIR = '/var/lib/geonameszip/'

if not os.path.exists(BASE_DIR):
  os.makedirs(BASE_DIR)

DEFAULT_SQLITE3_FILE = os.path.join(BASE_DIR, 'zipcodes.sqlite3')
RESULT_KEYS = ['postal_code', 'country', 'city', 'state', 'state_abbreviation', 'county', 'lat', 'lon']

def import_from_file(source_txt):
  """Imports from a tab-delimited file."""
  conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
  c = conn.cursor()

  try:
    print('Re-creating table "postal_codes".')
    c.execute('drop table postal_codes')
  except:
    print('Creating table "postal_codes".')
  # make the table.
  create_table(conn=conn)
  conn.commit()

  #try:
  if True:
      try:
        source = open(source_txt, 'rb')
        source_rows = UnicodeReader(source, delimiter='\t', quotechar='\"')
      except:
        # no need to recode in python 3
        source = open(source_txt, 'r')
        source_rows = csv.reader(source, delimiter='\t', quotechar='\"')
      rows_updated = 0
      rows_failed = 0
      for row in source_rows:
        try:
          postal_code = row[1]
          country = row[0]
          city = row[2]
          state = row[3]
          state_abbreviation = row[4]
          county = row[5]
          lat = row[9]
          lon = row[10]
          update_postal_code(postal_code, country, city, state, state_abbreviation, county, lat, lon, conn=conn, commit=False, cursor=None)
          rows_updated += 1
        except Exception as exc:
          rows_failed += 1
          print('Error updating row.')
          print(exc)
          continue
        sys.stdout.write('{0} updated ({1} failed)\r'.format(rows_updated, rows_failed))
        sys.stdout.flush()
      print('')

  #except IOError:
  #  print('Unable to open file "{0}".'.format(source_txt))
  #except Exception as exc:
  #  print('Error updating.')
  #  print(exc)
  conn.commit()
  conn.close()


def lookup_postal_code(postal_code, country, conn=None, cursor=None):
  should_close = False
  if conn is None:
    conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
    should_close = True
  if not cursor:
    cursor = conn.cursor()

  try:
    cursor.execute('select postal_code, country, city, state, state_abbreviation, county, lat, lon from postal_codes where postal_code = ? and country = ?', (postal_code,country,))
    result_tuple = cursor.fetchone()
    if should_close:
      conn.close()
    result = dict(zip(RESULT_KEYS, result_tuple))
    return result
  except:
    if should_close:
      conn.close()
    return None

def update_postal_code(postal_code, country, city, state, state_abbreviation, county, lat, lon, conn=None,commit=True, cursor=None):
  should_close = False
  if conn is None:
    conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
    should_close = True
  if not cursor:
    cursor = conn.cursor()
  cursor.execute('insert into postal_codes (postal_code, country, city, state, state_abbreviation, county, lat, lon) values (?, ?, ?, ?, ?, ?, ?, ?)', (postal_code, country, city, state, state_abbreviation, county, lat, lon))
  if commit:
    conn.commit()
  if should_close:
    conn.close()

def create_table(conn=None, cursor=None):
  should_close = False
  if conn is None:
    conn = sqlite3.connect(DEFAULT_SQLITE3_FILE)
    should_close = True
  if not cursor:
    cursor = conn.cursor()
  cursor.execute('create table if not exists postal_codes (postal_code text, country text, city text, state text, state_abbreviation text, county text, lat num, lon num)')
  conn.commit()
  if should_close:
    conn.close()


#### UNICODE decoding stuff:
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
  # csv.py doesn't do Unicode; encode temporarily as UTF-8:
  csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                          dialect=dialect, **kwargs)
  for row in csv_reader:
    # decode UTF-8 back to Unicode, cell by cell:
    yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
  for line in unicode_csv_data:
    yield line.encode('utf-8')

class UTF8Recoder:
  """Iterator that reads an encoded stream and reencodes the input to UTF-8
  """
  def __init__(self, f, encoding):
    self.reader = codecs.getreader(encoding)(f)

  def __iter__(self):
    return self

  def next(self):
    return self.reader.next().encode("utf-8")

class UnicodeReader:
  """A CSV reader which will iterate over lines in the CSV file "f",
  which is encoded in the given encoding.
  """

  def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
    f = UTF8Recoder(f, encoding)
    self.reader = csv.reader(f, dialect=dialect, **kwds)

  def next(self):
    row = self.reader.next()
    return [unicode(s, "utf-8") for s in row]

  def __iter__(self):
      return self
####
