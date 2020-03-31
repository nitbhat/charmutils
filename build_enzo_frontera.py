#This script clones charm and builds charm with different options
# clone charm
from charm_header import *

#os.system("git clone charmgit:charm charm");

# cd into it and build charm with options
#os.chdir("charm");

builds=["ucx","impi","mpich","mpichnoucx","ompi","ompinoucx","ucxompi"]

enzo_dir="/scratch1/03808/nbhat4/enzo-e/"

print 'basedir is' + str(basedirs[key])

charm_dir = str(basedirs[key])

buildType="debug2"
# Now change the directory
os.chdir(enzo_dir);

#print 'basebuild is' + str(basebuilds[key])

for build in builds:

  charmArch = frontera_basebuilds[build] + archmap[key]
  if(build == "ucxompi"):
    charmArch += "-ompipmix"

  #charmArch += "-smp"

  if(build != "ucx"):
    charmArch += "-" + build

  charmArch += "-" + buildType


  cleanStr = " make clean "
  env1 = "cp "+charm_dir+"/VERSION " +charm_dir+"/"+charmArch+"/"
  env2 = "export CHARM_HOME="+str(basedirs[key])+"/"+charmArch

  #print preBuildEnv[build]

#  buildStr = "./config Linux-x86_64-g++" + space + " --charm-base " + basedirs[key] + " --charm-arch "+ charmArch
#  #print buildStr
#
  moveStr = "mv ./bin/enzo-p "+ " enzo-p-nonsmp-"+build+"-"+buildType
#  #print moveStr
#
  makeStr = " make -j56 "
#  #print moveStr

  #finalCommand = cleanStr + " && " + preBuildEnv[build] + " && which mpicc && " + env2 + " && " + makeStr + " && " + moveStr
  finalCommand = cleanStr + " && " + preBuildEnv[build] + " && which mpicc && " + env1 + " && " + env2 + " && " + makeStr + " && " + moveStr
  print finalCommand


  #buildStr +=  space + num_proc + buildTypeMap2[buildType]

  #finalCommand = preBuildEnv[build]
  #finalCommand += " && which mpicc && "
  #finalCommand += buildStr

  ##print buildStr
  #print "Final command is:" + finalCommand
  ##os.system(buildStr)
  #os.system(finalCommand)
