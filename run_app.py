#This script clones charm and builds charm with different options
# clone charm
from charm_header import *

#os.system("git clone charmgit:charm charm");

# cd into it and build charm with options
#os.chdir("charm");

#print 'basedir is' + str(basedirs[key])

# Now change the directory
#os.chdir(basedirs[key]);



print ("key is " + str(key))
os.chdir(appdirs[key])
suffix="prod"

print ("app dir is" + str(appdirs[key]))

print ('basebuild is' + str(basebuilds[key]))

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



    print (buildStr)
    os.system(buildStr)

    outputDir = appdirs[key] + "/output/"
    print (outputDir)
    os.chdir(outputDir)
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    print ("dirs is " + str(dirs))
    latest = sorted(dirs, key=lambda x: os.path.getctime(x), reverse=True)[0]
    #l_subdirs = [d for d in os.listdir(outputDir) if os.path.isdir(d)]
    #latest_subdir = max(all_subdirs, key=os.path.getmtime)

    outputFinal = outputDir + latest
    tarFile = key + "_" + basebuild + "_" + mode+ ".tar.gz"
    tarCommand = "tar -czvf " + tarFile + " " + outputFinal


    #print archStr
    print (latest)
    print (tarCommand)
    os.system(tarCommand)
    os.chdir(appdirs[key])

    currentDir = os.getcwd()

    print("Current directory is " + currentDir)

    compareCommand = appdirs[key] + "/scripts/evaluateOutput.sh " + outputDir + tarFile
    print (compareCommand)
    os.system(compareCommand)
