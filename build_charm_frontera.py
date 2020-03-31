#This script clones charm and builds charm with different options
# clone charm
from charm_header import *

#os.system("git clone charmgit:charm charm");

# cd into it and build charm with options
#os.chdir("charm");

builds=["ucx","impi","mpich","mpichnoucx","ompi","ompinoucx","ucxompi"]

print 'basedir is' + str(basedirs[key])

# Now change the directory
os.chdir(basedirs[key]);

#print 'basebuild is' + str(basebuilds[key])

buildType = "debug2"

for build in builds:
  #print "command to be executed:" + preBuildEnv[build]
  # echo "which mpicc" to verify
  #if(build != "ucx" and build != "impi"):
  #  print "***** build:" + build +" setting PATH to:" + preBuildEnv[build]
  #  os.environ["PATH"] = preBuildEnv[build]
  #else:
  #  print "***** build:" + build +" launching module: " + preBuildEnv[build]
  #  os.system(preBuildEnv[build])

  for archopt_str in archopts_str:
    #os.system("")
    #print(os.environ['PATH'])
    buildStr = "./build" + space + target + space + frontera_basebuilds[build] + archmap[key]

    if(build == "ucxompi"):
      buildStr += " ompipmix "

    buildStr += space + archopt_str + space + "--enable-error-checking --suffix="

    if(buildType =="prod"):
      buildStr += " --with-production "

    if(build != "ucx"):
      buildStr += build + "-"


    if(buildType == "debug"):
      buildStr += "debug "
    elif(buildType == "debug2"):
      buildStr += "debug2 "
    else:
      buildStr += "prod "

    buildStr += " --basedir="+frontera_basedir[build]

    if(build == "ucxompi"):
      buildStr += " --basedir=/work/03808/nbhat4/frontera/ucx/build_1.6.1"

    #if(basebuild == "ucx" and key != "golub"):
    #  for buildbasedir in buildbasedirs[key]:
    #    buildStr += space + " --basedir=" + buildbasedir;

    buildStr +=  space + num_proc + buildTypeMap2[buildType]

    #if(buildType == "debug"):
    #  buildStr +=  " -O0 -g "

    finalCommand = preBuildEnv[build]
    finalCommand += " && which mpicc && "
    finalCommand += buildStr

    #print buildStr
    #print "Final command is:" + finalCommand
    print finalCommand
    #os.system(buildStr)

    #os.system(finalCommand)
