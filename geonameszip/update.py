#!/usr/bin/env python
import os, sys, math, time, zipfile
import geonameszip
try:
    import urllib2 as urllib
except ImportError:
    from urllib import request as urllib

DOWNLOAD_URL = 'http://download.geonames.org/export/zip/allCountries.zip'

if os.name == 'nt':
  import ctypes
  from ctypes import wintypes, windll

  CSIDL_COMMON_APPDATA = 35

  _SHGetFolderPath = windll.shell32.SHGetFolderPathW
  _SHGetFolderPath.argtypes = [wintypes.HWND, ctypes.c_int,
                               wintypes.HANDLE, wintypes.DWORD,
                               wintypes.LPCWSTR]
  path_buf = wintypes.create_unicode_buffer(wintypes.MAX_PATH)
  _SHGetFolderPath(0, CSIDL_COMMON_APPDATA, 0, 0, path_buf)
  BASE_DIR = path_buf.value
else:
  BASE_DIR = '/var/lib/geonameszip/'

if not os.path.exists(BASE_DIR):
  os.makedirs(BASE_DIR)

DOWNLOADED_ZIP_FILE = os.path.join(BASE_DIR, 'allCountries.zip')
EXTRACTED_TEXT_FILE = os.path.join(BASE_DIR, 'allCountries.txt')

def download():
  def on_data_recieved(bytes_downloaded, chunk_size, total_size):
    complete = round((float(bytes_downloaded)/total_size) * 100, 2)
    complete_string = '{0}%'.format(complete)
    cols = get_terminal_size()[0]
    progress_bar_total_cols = cols - 16 - len(complete_string)
    progress_bar_complete_cols = math.floor(progress_bar_total_cols*(complete/100))
    progress_bar_gap_cols = progress_bar_total_cols - progress_bar_complete_cols
    progress_bar = ''.ljust(int(progress_bar_complete_cols), '#')
    progress_gap = ''.ljust(int(progress_bar_gap_cols), ' ')
    sys.stdout.write('Downloaded:[{0} {1}{2}]\r'.format(progress_bar, complete_string, progress_gap))
    sys.stdout.flush()

  with open(DOWNLOADED_ZIP_FILE, 'wb') as fh:
    print('Downloading {0}'.format(DOWNLOAD_URL))
    response = urllib.urlopen(DOWNLOAD_URL)
    try:
      size_header = response.info().getheader('Content-Length')
    except:
      size_header = response.info()['Content-Length']

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

def import_downloaded_file():
  now = time.time()
  try:
    created_time = os.path.getctime(EXTRACTED_TEXT_FILE)
  except OSError:
    created_time = now - 90000

  # if the text file is old, re-extract over it.
  print(DOWNLOADED_ZIP_FILE)
  try:
    if now - created_time > 86400:
      zip = zipfile.ZipFile(DOWNLOADED_ZIP_FILE, 'r')
      zip.extractall(BASE_DIR)
  except:
    # re-download file.
    print('Invalid zip. Re-downloading.')
    download()
    import_downloaded_file()
    return

  print('Updating... please wait.')
  geonameszip.import_from_file(EXTRACTED_TEXT_FILE)


### TERMINAL STUFF
import os
import shlex
import struct
import platform
import subprocess


def get_terminal_size():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        print("default")
        tuple_xy = (80, 25)      # default value
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass


def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])
