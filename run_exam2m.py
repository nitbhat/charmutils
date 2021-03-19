from charm_header import *

num_nodes=32
max_nodes=64
ppn = ppnmap[key]
proc_per_node=proc_per_node_map[key]

proj=True
stats=False
prev=False
debug=False

print "key is " + key
print " basedir is " + basedirs[key]

exam2mdir=exam2mdirs[key]

if(prev):
  exam2mdir += "_prev"

buildName = "build"
if(debug):
  buildName += "_debug"
if(proj):
  buildName += "_proj"




def getScriptBeg(num_nodes, mins, jobname, outputName):
  if(jobscheds[key] == "pbs"):
    scriptbeg = "#!/bin/bash\n";
    scriptbeg += "#PBS -N " + jobname + "\n";
    scriptbeg += "#PBS -l walltime=00:" + str(mins) + ":00\n";
    scriptbeg += "#PBS -l nodes=" + str(num_nodes) + ":ppn=24\n";
  elif(jobscheds[key] == "slurm" and key=="cori"):
    scriptbeg = "#!/bin/bash -l\n";
    scriptbeg += "#SBATCH -q regular\n";
    scriptbeg += "#SBATCH -t 00:" + str(mins) + ":00\n";
    scriptbeg += "#SBATCH -N "+ str(num_nodes) + "\n";
    scriptbeg += "#SBATCH --output="+ outputName + "\n";
    scriptbeg += "#SBATCH --constraint=haswell" + "\n";
    scriptbeg += "#SBATCH --job-name=" + jobname + "\n";
  elif(jobscheds[key] == "slurm" and key=="frontera"):
    scriptbeg = "#!/bin/bash -l\n";
    scriptbeg += "#SBATCH -p normal\n";
    scriptbeg += "#SBATCH -t 00:" + str(mins) + ":00\n";
    scriptbeg += "#SBATCH -N "+ str(num_nodes) + "\n";
    scriptbeg += "#SBATCH --output="+ outputName + "\n";
    scriptbeg += "#SBATCH --job-name=" + jobname + "\n";
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

def getRunCommand(num_nodes, voxLen):

  runComm = ""
  execDir = exam2mdir + "/" + buildName

  execDir += "/Main/"

  outputDir = exam2mdir + "/../exam2mOutputFiles/projResults/";
  traceroot = "exam2m_mpi_nonsmp_sphere_cube_" + str(num_nodes) + "_" + voxLen + "_projdir";

  execName = "exam2m ";
  args = exam2mdir + "/../exam2mInputFiles/sphere_full_48M.exo " + exam2mdir + "/../exam2mInputFiles/unitcube_48M.exo " + voxLen + " "
  #args = exam2mdir + "/../exam2mInputFiles/sphere_full_48M.exo " + exam2mdir + "/../exam2mInputFiles/unitcube_48M.exo "

  postargs = ""
  if(stats):
    postargs += "+printTetStats +printVoxCount"

  if(proj):
    postargs += " +traceroot " + outputDir + traceroot

  postpostargs = ""

  execPath = execDir + execName

  smp_index = 0;

  # run bcast
  pval         = str(getPValue(num_nodes, proc_per_node, archopts[smp_index]))
  nval         = str(getNValue(num_nodes, proc_per_node, archopts[smp_index]))
  cval         = str(getCValue(num_nodes, proc_per_node, archopts[smp_index]))

  runComm += "srun -n " + nval + space + " -c " + cval + space + execPath + space + args + space + postargs + space + postpostargs
  #runComm += "mpirun -n " + nval + space + execPath + space + args + space + postargs + space + postpostargs
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
  voxLens = [0.01, 0.025, 0.05, 0.075]
  #voxLens = [0.01, 0.025, 0.075]
  #voxLens = [0.05]
  for vox in voxLens:
    voxLen = str(vox)
    smp_index=0
    scriptname = "exam2m_mpi_nonsmp_sphere_cube_" + str(num_nodes) + "_" + voxLen

    if(debug):
      scriptname += "_debug"

    if(prev):
      scriptname += "_prev"

    if(stats):
      scriptname += "_stats"

    folderName = "newResults"

    if(proj):
      scriptname += "_proj"
      folderName = "projResults"

    scriptname += "_script";


    outputDir = exam2mdir + "/../exam2mOutputFiles/" + folderName + "/"


    outputName = outputDir + "exam2m_mpi_nonsmp_sphere_cube_" + str(num_nodes) + "_" + voxLen

    if(debug):
      outputName += "_debug"
    if(prev):
      outputName += "_prev"
    if(stats):
      outputName += "_stats"
    if(proj):
       outputName += "_proj"

    outputName += "_result_%j.out";

    fileContents = getScriptBeg(num_nodes, 5, scriptname, outputName);
    fileContents += getScriptEnd(num_nodes, proc_per_node, archopts[0]);

    fileContents += "export LD_LIBRARY_PATH=" + exam2mdir + "/external/" + buildName + "/mpi-nonsmp"

    #if(proj):
    #  fileContents += "-proj"

    fileContents += "/tpls/lib:$LD_LIBRARY_PATH" + "\n";

    fileContents += "cd " + exam2mdir + "/" + buildName + "\n"

    if(proj):
      #fileContents += "-proj" + "\n"
      outputDir = exam2mdir + "/../exam2mOutputFiles/projResults/";
      traceroot = "exam2m_mpi_nonsmp_sphere_cube_" + str(num_nodes) + "_" + voxLen + "_projdir" + "\n"
      fileContents += "mkdir " + outputDir + traceroot + "\n";

    fileContents += "\n";
    fileContents += "mkdir output_" + str(num_nodes) + "_" + voxLen + "\n";
    fileContents += "cd output_" + str(num_nodes) + "_" + voxLen + "\n";



    scriptDir = exam2mdir + "/scripts/generatedScripts/"
    extraSuffix= ""
    runComm = getRunCommand(num_nodes, voxLen);

    fileContents += runComm + "\n\n\n\n"

    print "======================================================="
    print fileContents
    print "======================================================="

    script = open(scriptDir + scriptname, "w+");
    script.write(fileContents)
    sys.stdout.flush();

    #os.system("sbatch "+scriptDir + scriptname)

  num_nodes = num_nodes*2
