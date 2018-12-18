#This script builds example execs so that they are ready to run
from charm_header import *

cwd = os.getcwd()

for archopt in archopts_str:
  buildDirStr =  basedir + basearch + archopt + postdir
  os.chdir(buildDirStr)
  os.system("make -j4")
  os.chdir(cwd)
