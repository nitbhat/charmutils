#This script clones charm and builds charm with different options
# clone charm
from charm_header import *

#os.system("git clone charmgit:charm charm");

# cd into it and build charm with options
#os.chdir("charm");

#print 'basedir is' + str(basedirs[key])

# Now change the directory
#os.chdir(basedirs[key]);

import glob


print "application directory is " + appdirs[key]
os.chdir(appdirs[key])
suffix="prod"


#print 'basebuild is' + str(basebuilds[key])

for basebuild in basebuilds[key]:
  for archopt_str in archopts_str:
    archStr  = str(basedirs[key]) + "/" + basebuild + archmap[key]
    mode = "nonsmp"
    if(archopt_str != ""):
      archStr += "-" + archopt_str
      mode = "smp"

    archStr += "-" + suffix

    charmHome = archStr
    buildStr = "make clean test CHARM_HOME=" + charmHome

    outputDir = appdirs[key] + "/output"

    print outputDir

    os.chdir(outputDir)
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    print "dirs is " + str(dirs)
    latest = sorted(dirs, key=lambda x: os.path.getctime(x), reverse=True)[0]
    #l_subdirs = [d for d in os.listdir(outputDir) if os.path.isdir(d)]
    #latest_subdir = max(all_subdirs, key=os.path.getmtime)

    outputDir += latest
    tarFile = key + "_" + basebuild + "_" + mode+ ".tar.gz"
    tarCommand = "tar -czvf " + tarFile + " " + outputDir


    #print archStr
    print buildStr
    os.system(buildStr)
    print latest
    print tarCommand
    os.system(tarCommand)
    os.chdir(appdirs[key])

    compareCommand = "./scripts/evaluateOutput.sh " + tarFile
    print compareCommand
