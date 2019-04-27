#This script clones charm and builds charm with different options
# clone charm
from charm_header import *

#os.system("git clone charmgit:charm charm");

# cd into it and build charm with options
#os.chdir("charm");

print 'basedir is' + str(basedirs[key])

# Now change the directory
os.chdir(basedirs[key]);

print 'basebuild is' + str(basebuilds[key])

for basebuild in basebuilds[key]:
  for archopt_str in archopts_str:
    buildStr = "./build" + space + target + space + basebuild + archmap[key]
    buildStr += space + archopt_str + space + options + space + num_proc
    print buildStr
    os.system(buildStr)
