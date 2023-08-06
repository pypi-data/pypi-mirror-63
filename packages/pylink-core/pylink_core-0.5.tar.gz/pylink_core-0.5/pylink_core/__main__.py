import os, sys
import argparse
import threading
import time
import webbrowser
from .klink import klinkServe, shutdown
import platform
import subprocess

from datetime import datetime

VERSION = "1.1"

_HELP_TEXT = """
pylink user-path
"""

argv = sys.argv[1:]
parser = argparse.ArgumentParser(description=_HELP_TEXT)
parser.add_argument('user', nargs='?', default=os.getcwd()) # user path that have write permission


parser.add_argument('-port', nargs='?', default=9988, type=int)
args = parser.parse_args(argv)

class pylinkThread(threading.Thread):
  def __init__(self, logOutput):
    self._logOutput = logOutput
    threading.Thread.__init__(self)

  def run(self):
    klinkServe(args, self._logOutput)

  def stop(self):
    shutdown()
logfile = open(os.path.join(args.user, datetime.now().strftime('log_%Y_%m_%d_%H_%M.log')), 'w')
def logOutput(method, *params):
  logfile.write(params[0])
  logfile.flush()

th = pylinkThread(logOutput)
th.start()

isRunning = True
while isRunning:
  userInput = input()
  if userInput == 'stop':
    th.stop()
    logfile.close()
    break
  elif userInput == 'driver':
    if platform.system() == "Windows" and platform.release() == '7':
      infPath = os.path.join(args.user, "pybcdc.inf")
      if '32bit' in platform.architecture():
        p = os.system('%%SystemRoot%%\\Sysnative\\pnputil.exe -i -a %s' %(infPath))
      else:
        p = os.system('pnputil.exe -i -a %s' %(infPath))
    else:
      print("只有windows7用户才需要装驱动哦～")