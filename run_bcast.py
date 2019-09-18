from charm_header import *

num_nodes=1
max_nodes=32
ppn = ppnmap[key]
proc_per_node=proc_per_node_map[key]

print "key is " + key

print " basedir is " + basedirs[key]


def getScriptBeg(num_nodes, mins, jobname):
  if(jobscheds[key] == "pbs"):
    scriptbeg = "#!/bin/bash\n";
    scriptbeg += "#PBS -N " + jobname + "\n";
    scriptbeg += "#PBS -l walltime=00:" + str(mins) + ":00\n";
    scriptbeg += "#PBS -l nodes=" + str(num_nodes) + ":ppn=24\n";
  elif(jobscheds[key] == "slurm" and key=="edison"):
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
  if(key == "iforge"):
    fileContents += "~/gennodelist2.pl $PBS_NODEFILE $PBS_JOBID "+ str(num_nodes * ppn) + " _" + scriptname + "\n";
  elif(key == "golub"):
    # do nothing
    pass
  else:
    nval         = str(getNValue(num_nodes, proc_per_node, archopts[smp_index]))
    tasks_per_node =  str(getTasksPerNodeValue(num_nodes, proc_per_node, archopts[smp_index]))
    cval         = str(getCValue(num_nodes, proc_per_node, archopts[smp_index]))
    fileContents += "#SBATCH -n "+nval+"\n";
    fileContents += "#SBATCH --ntasks-per-node="+tasks_per_node+"\n";
  return fileContents;

def getSmpType(basebuild):
  #if key=="bridges":
  #  return "regular"
  #elif key=="iforge":
  #  if basebuild == "mpi":
  #    return "weird"
  return "regular"

def attachPath(bcastFullDir):
  if key=="iforge" or key=="hpcadv" or key=="golub":
    return bcastFullDir
  else:
    return ""

def getRunCommand(num_nodes, archopt_str, smp_index, basebuild, extraSuffix):
  runComm = ""
  basedir = basedirs[key]
  exampleFullDir = basedir + slash +  basebuild + archmap[key] + archopts_str1[smp_index] + hyphen + suffix + (hyphen if extraSuffix != "" else "") + extraSuffix + exampleDir
  outputDir = charmutilsdirs[key] + slash + "results/" + key + slash + "bcast/";

  # run bcast
  bcastFullDir = exampleFullDir + slash + "bcastPingAll/";
  charmRunDir  = attachPath(bcastFullDir) + launcher_map[key];
  execPath     = bcastFullDir + "/ping_all ";
  pval         = str(getPValue(num_nodes, proc_per_node, archopts[smp_index]))
  nval         = str(getNValue(num_nodes, proc_per_node, archopts[smp_index]))
  cval         = str(getCValue(num_nodes, proc_per_node, archopts[smp_index]))
  args         = " 16 33554432 50 10 0 "
  postargs     = getPostArgs(num_nodes, proc_per_node, archopts[smp_index], getSmpType(basebuild))
  if(key == "iforge"):
    postpostargs = getPostPostArgs(basebuild, archopts[smp_index], ".$PBS_JOBID")
  else:
    postpostargs = getPostPostArgs(basebuild, archopts[smp_index], "_" + scriptname)
  outputFile   = outputDir + "reg_bcast_test_" + str(num_nodes) + "_" + basebuild + ("_" if extraSuffix != "" else "") + extraSuffix + "_" +  archopts[smp_index]


  if(path.exists(outputFile)):
    print "file exists"
    os.remove(outputFile);
  else:
    print "file does not exist"



  if(key == "edison"):
    runComm += charmRunDir + space + "-n " + nval + space + " -c " + cval + space + execPath + space + args + space + postargs + space + postpostargs + " > " + outputFile
  elif(key == "bridges"):
    runComm += charmRunDir + space + "-n " + nval + space + execPath + space + args + space + postargs + space + postpostargs + " > " + outputFile
  elif(key == "iforge"):
    runComm += charmRunDir + space + "+p" + pval + space + execPath + space + args + space + postargs + space + postpostargs + " > " + outputFile
  elif(key == "hpcadv" or key == "golub"):
    if(basebuild == "verbs"):
      runComm += charmRunDir + space + "+p" + pval + space + execPath + space + args + space + postargs + space + postpostargs + " > " + outputFile
    else:
      runComm += "mpirun" + space + "-n " + nval + space + execPath
      runComm += space + args
      print postargs
      runComm += space + postargs
      runComm += space + postpostargs + " > " + outputFile
  return runComm


def getPValue(num_nodes, proc_per_node, mode):
  if mode == "smp":
    if num_nodes == 1:
      return ppn - 1
    else:
      p = (ppn/proc_per_node - 1)*proc_per_node*num_nodes
      return p
  else:
    return ppn * num_nodes

def getNValue(num_nodes, proc_per_node, mode):
  if mode == "smp":
    if num_nodes == 1:
      return 1
    else:
      n = proc_per_node*num_nodes
      return n
  else:
    return ppn * num_nodes

def getCValue(num_nodes, proc_per_node, mode):
  if mode == "smp":
    if num_nodes == 1:
      return ppn
    else:
      c = ppn/proc_per_node
      return c;
  else:
    return 1;

def getTasksPerNodeValue(num_nodes, proc_per_node, mode):
  if mode == "smp":
    if num_nodes == 1:
      return 1
    else:
      return proc_per_node
  else:
    return ppn;



def getPostArgs(num_nodes, proc_per_node, mode, smpType):
  if mode == "smp":
    if smpType== "regular":
      if num_nodes == 1:
        return " ++ppn " + str(ppn - 1) + space + " +pemap 0-"+str(ppn-2)+" +commap "+str(ppn-1)
      else:
        if(ppn == 24):
          return " ++ppn " + str(ppn/proc_per_node - 1) + space + " +pemap 0-10,12-22 +commap 11,23"
        elif(ppn == 28):
          return " ++ppn " + str(ppn/proc_per_node - 1) + space + " +pemap 0-12,14-26 +commap 13,27"
        elif(ppn == 32):
          return " ++ppn " + str(ppn/proc_per_node - 1) + space + " +pemap 0-14,16-30 +commap 15,31"
    else:
      if mode == "smp":
        if num_nodes == 1:
          return " ++ppn " + str(ppn - 1) + space + " +pemap 0-22 +commap 23"
        else:
          postArgStr = " ++ppn " + str(ppn/proc_per_node - 1) + space;
          commArgStr = " +commap ";
          postArgStr += " +pemap "
          index = 0;
          peMapVal = (ppn/proc_per_node - 1)
          while((index + peMapVal - 1) < num_nodes*ppn):
            postArgStr += str(index) + hyphen + str(index + peMapVal - 1) + ",";
            index = index + peMapVal;
            commArgStr += str(index) + ","
            index = index + 1;
          postArgStr += " " + commArgStr
          return postArgStr
  else:
    return ""

def getPostPostArgs(basebuild, mode, append):
  if key == 'iforge':
    if basebuild == 'verbs':
      if mode == 'smp':
        return "++nodelist ~/.nodelist" + append + ".smp"
      else:
        return "++nodelist ~/nodelist" + append
  if key == 'hpcadv' or 'golub':
    if basebuild == 'verbs':
      return "++mpiexec"
  return ""

while num_nodes <= max_nodes:
  smp_index=0
  for archopt_str in archopts_str:
    scriptname = "reg_bcast_test_" + str(num_nodes) + "_" + archopts[smp_index];
    fileContents = getScriptBeg(num_nodes, 30, scriptname);
    fileContents += getScriptEnd(num_nodes, proc_per_node, archopts[smp_index]);

    for basebuild in basebuilds[key]:
      scriptDir = charmutilsdirs[key] + slash + "scripts/" + key + slash + "bcast/";
      extraSuffix= ""
      #if(basebuild == "mpi"):
      #  extraSuffix="ompi"
      #  runComm = getRunCommand(num_nodes, archopt_str, smp_index, basebuild, extraSuffix);
      #  fileContents += runComm + "\n\n\n\n"

      #  if key == "golub":
      #    fileContents += "module unload openmpi/3.1.1-gcc-7.2.0\n"
      #    fileContents += "module load mvapich2/2.3rc2-gcc-7.2.0\n"
      #  if key == "hpcadv":
      #    fileContents += "module unload hpcx/2.4.0-pre\n"
      #    fileContents += "module load impi/2018.4.274\n"

      #  extraSuffix="mvapich"
      #  runComm = getRunCommand(num_nodes, archopt_str, smp_index, basebuild, extraSuffix);
      #  fileContents += runComm + "\n\n\n\n"
      #else:
      runComm = getRunCommand(num_nodes, archopt_str, smp_index, basebuild, extraSuffix);
      fileContents += runComm + "\n\n\n\n"

    print "======================================================="
    print fileContents
    print "======================================================="

    script = open(scriptDir + scriptname, "w+");
    script.write(fileContents)
    sys.stdout.flush();

    #if(archopts[smp_index] == "nonsmp"):
    #  os.system("qsub -S "+scriptDir + scriptname)

    smp_index = smp_index + 1;
  num_nodes = num_nodes*2
