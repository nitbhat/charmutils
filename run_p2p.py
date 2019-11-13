from charm_header import *

num_nodes=1
max_nodes=2
ppn = ppnmap[key]
proc_per_node=proc_per_node_map[key]


def getScriptBeg(num_nodes, mins, jobname, smp_index):
  if(jobscheds[key] == "pbs"):
    scriptbeg = "#!/bin/bash\n";
    scriptbeg += "#PBS -N " + jobname + "\n";
    scriptbeg += "#PBS -l walltime=00:" + str(mins) + ":00\n";
    scriptbeg += "#PBS -l nodes=" + str(num_nodes) + ":ppn=";
    scriptbeg += str(getTasksPerNodeValue(num_nodes, proc_per_node, archopts[smp_index], "p2p")) + "\n";
    if(key == "golub"):
      scriptbeg += "#PBS -q secondary\n";
      scriptbeg += "#PBS -j oe\n";
  elif(jobscheds[key] == "slurm" and key=="cori"):
    scriptbeg = "#!/bin/bash -l\n";
    scriptbeg += "#SBATCH -q regular\n";
    scriptbeg += "#SBATCH -t 00:" + str(mins) + ":00\n";
    scriptbeg += "#SBATCH -N "+ str(num_nodes) + "\n";
  elif(jobscheds[key] == "slurm" and key=="bridges"):
    scriptbeg = "#!/bin/bash\n";
    scriptbeg += "#SBATCH -p RM\n";
    scriptbeg += "#SBATCH -t 00:" + str(mins) + ":00\n";
    scriptbeg += "#SBATCH -N "+ str(num_nodes) + "\n";
  elif(jobscheds[key] == "slurm" and key=="hpcadv"):
    scriptbeg = "#!/bin/bash\n";
    scriptbeg += "#SBATCH -p thor\n";
    scriptbeg += "#SBATCH -t 00:" + str(mins) + ":00\n";
    scriptbeg += "#SBATCH -N "+ str(num_nodes) + "\n";
  return scriptbeg

def getScriptEnd(num_nodes,proc_per_node, mode):
  fileContents = "";
  if(key=="edison" or key=="bridges" or key=="hpcadv"):
    nval         = str(getNValue(num_nodes, proc_per_node, archopts[smp_index], "p2p"))
    tasks_per_node =  str(getTasksPerNodeValue(num_nodes, proc_per_node, archopts[smp_index], "p2p"))
    cval         = str(getCValue(num_nodes, proc_per_node, archopts[smp_index], "p2p"))
    fileContents += "#SBATCH -n "+nval+"\n";
    fileContents += "#SBATCH --ntasks-per-node="+tasks_per_node+"\n";
  elif(key == "iforge"):
    fileContents += "~/gennodelist2.pl $PBS_NODEFILE $PBS_JOBID "+ str(num_nodes * ppn) + " _" + scriptname + "\n";
  elif(key == "golub"):
    fileContents += "module unload mvapich2/2.3-intel-18.0\n";
    fileContents += "module load mvapich2/2.3rc2-gcc-7.2.0 \n";
  return fileContents;

def getSmpType(basebuild):
  #if key=="bridges":
  #  return "regular"
  #elif key=="iforge":
  #  if basebuild == "mpi":
  #    return "weird"
  return "regular"

def attachPath(bcastFullDir):
  #if key=="iforge":
    return bcastFullDir
  #else:
  #  return ""

def getRunCommand(num_nodes, archopt_str, smp_index, basebuild):
  runComm = ""
  exampleFullDir = basedirs[key] + slash +  basebuild + archmap[key]
  if(key == "hpcadv" and basebuild == "ucx"):
    exampleFullDir += "-ompipmix"
  exampleFullDir += archopts_str1[smp_index] + hyphen + suffix + exampleDir
  outputDir = charmutilsdirs[key] + slash + "results/" + key + slash + "p2p/";

  # run bcast
  bcastFullDir = exampleFullDir + slash + "p2pPingpong/";
  print "bcastFullDir is " + bcastFullDir
  charmRunDir  = attachPath(bcastFullDir) + launcher_map[key];
  print "charmRunDir is " + charmRunDir
  execPath     = bcastFullDir + "megaZCPingpong ";
  pval         = str(getPValue(num_nodes, proc_per_node, archopts[smp_index], "p2p"))
  nval         = str(getNValue(num_nodes, proc_per_node, archopts[smp_index], "p2p"))
  cval         = str(getCValue(num_nodes, proc_per_node, archopts[smp_index], "p2p"))
  args         = ""
  postargs     = getPostArgs(num_nodes, proc_per_node, archopts[smp_index], getSmpType(basebuild), "p2p")
  postpostargs = str(getPostPostArgs(basebuild, archopts[smp_index], "_" + scriptname))
  outputFile   = outputDir + "reg_p2p_test_" + str(num_nodes) + "_" + basebuild + "_" + archopts[smp_index]

  if(key == "edison"):
    runComm += charmRunDir + space + "-n " + nval + space + " -c " + cval + space + execPath + space + args + space + postargs + space + postpostargs + " > " + outputFile
  elif(key == "bridges"):
    runComm += charmRunDir + space + "-n " + nval + space + execPath + space + args + space + postargs + space + postpostargs + " > " + outputFile
  elif(key == "iforge" or key == "hpcadv"):
    runComm += charmRunDir + space + "+p" + pval + space
    runComm += execPath + space + args + space

    print "mode is " + str(archopts[smp_index])
    print "postargs is " + str(postargs)
    runComm += postargs + space
    runComm += postpostargs + " > " + outputFile
  elif(key == "golub"):
    if basebuild == 'verbs':
      runComm += charmRunDir + space + "+p" + pval + space
      runComm += execPath + space + args + space

      print "mode is " + str(archopts[smp_index])
      print "postargs is " + str(postargs)
      runComm += postargs + space
      runComm += postpostargs + " > " + outputFile
    else:
      runComm += "mpirun" + space + "-n " + nval + space + execPath + space + args + space + postargs + space + postpostargs + " > " + outputFile

  return runComm


def getPValue(num_nodes, proc_per_node, mode, app):
  return 2;

def getNValue(num_nodes, proc_per_node, mode, app):
  return 2;

def getCValue(num_nodes, proc_per_node, mode, app):
  if mode == "smp":
    return 2;
  else:
    return 1;

def getTasksPerNodeValue(num_nodes, proc_per_node, mode, app):
  if num_nodes == 1:
    return 2
  else:
    return 1

def getPostArgs(num_nodes, proc_per_node, mode, smpType, app):
  print "getPostArgs :" + "num_nodes = " + str(num_nodes) + ", proc_per_node = " + str(proc_per_node) + ", mode = " + mode + ",  smpType = "+ smpType + ", app = " + app
  if mode  == "smp":
    if smpType== "regular":
      if num_nodes == 1:
        return " ++ppn 1" + space + "+pemap 0,2"+ " +commap 1,3"
      else:
        return " ++ppn 1" + space + "+pemap 0"+ " +commap 1"
  return ""

def getPostPostArgs(basebuild, mode, append):
  if key == 'iforge':
    if basebuild == 'verbs':
      if mode == 'smp':
        return "++nodelist ~/nodelist" + append + ".smp"
      else:
        return "++nodelist ~/nodelist" + append
  elif key == 'golub' and basebuild == 'verbs':
    return "++mpiexec "
  return ""

while num_nodes <= max_nodes:
  smp_index=0
  for archopt_str in archopts_str:
    scriptname = "reg_p2p_test_" + str(num_nodes) + "_" + archopts[smp_index];
    fileContents = getScriptBeg(num_nodes, 30, scriptname, smp_index);
    fileContents += getScriptEnd(num_nodes, proc_per_node, archopts[smp_index]);

    for basebuild in basebuilds[key]:
      scriptDir = charmutilsdirs[key] + slash + "scripts/" + key + slash + "p2p/";
      runComm = getRunCommand(num_nodes, archopt_str, smp_index, basebuild);
      fileContents += runComm + "\n\n\n\n"

    print "======================================================="
    print fileContents
    print "======================================================="

    print "File name is :" + scriptDir + scriptname
    script = open(scriptDir + scriptname, "w+");
    script.write(fileContents)
    sys.stdout.flush();

    #if(archopts[smp_index] == "nonsmp"):
    #  os.system("qsub -S "+scriptDir + scriptname)
    submitComm = "sbatch "+ scriptDir + scriptname;
    print "command is " + submitComm
    os.system(submitComm)

    smp_index = smp_index + 1;
  num_nodes = num_nodes*2
