#This script builds example execs so that they are ready to run
from charm_header import *

cwd = os.getcwd()

for basebuild in basebuilds[key]:
  for basedir in basedirs[key]:
    for archopt_str in archopts_str1:
      exampleFullDir = basedir + slash +  basebuild + archmap[key] + archopt_str + hyphen + suffix + exampleDir
      print exampleFullDir
      os.chdir(exampleFullDir)
      os.system("make clean")
      os.system("make -j4")
      os.chdir(cwd)
