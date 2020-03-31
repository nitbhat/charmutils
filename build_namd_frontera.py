#This script clones charm and builds charm with different options
# clone charm
from charm_header import *

#os.system("git clone charmgit:charm charm");

# cd into it and build charm with options
#os.chdir("charm");

builds=["ucx","impi","mpich","mpichnoucx","ompi","ompinoucx","ucxompi"]

namd_dir="/scratch1/03808/nbhat4/namd"

print 'basedir is' + str(basedirs[key])

buildType="debug"
# Now change the directory
os.chdir(namd_dir);

#print 'basebuild is' + str(basebuilds[key])
mode = "smp"

for build in builds:

  charmArch = frontera_basebuilds[build] + archmap[key]
  if(build == "ucxompi"):
    charmArch += "-ompipmix"

  charmArch += "-" + mode

  if(build != "ucx"):
    charmArch += "-" + build
  charmArch += "-" + buildType

  #print preBuildEnv[build]

  buildStr = "./config Linux-x86_64-g++" + space + " --charm-base " + basedirs[key] + " --charm-arch "+ charmArch

  if(buildType == "debug"):
    buildStr += " --with-debug"
  #print buildStr

  newDir = " Linux-x86_64-g++-"+ mode + "-" + build + "-" + buildType

  moveStr = "mv Linux-x86_64-g++ "+ newDir
  #print moveStr

  makeStr = " make -j56 -C " + newDir
  #print moveStr

  finalCommand = preBuildEnv[build] + " && which mpicc && " + buildStr + " && " + moveStr + " && " + makeStr
  print finalCommand


  #buildStr +=  space + num_proc + buildTypeMap2[buildType]

  #finalCommand = preBuildEnv[build]
  #finalCommand += " && which mpicc && "
  #finalCommand += buildStr

  ##print buildStr
  #print "Final command is:" + finalCommand
  ##os.system(buildStr)
  os.system(finalCommand)
