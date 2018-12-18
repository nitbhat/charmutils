#This script clones charm and builds charm with different options
# clone charm
from charm_header import *

os.system("git clone charmgit:charm charm");

# cd into it and build charm with options
os.chdir("charm");

import charm_header.py

for archopt in archopts_str:
  buildStr = "./build" + space + target + space+ basearch + archopt + options + num_proc + debug_opts
  print buildStr
  os.system(buildStr);
