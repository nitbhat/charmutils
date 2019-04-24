from charm_header import *

num_nodes=1
max_nodes=32
ppn = 24
proc_per_node=2


def getPbsScriptBeg(num_nodes, mins, jobname):
  scriptbeg = "#!/bin/bash\n";
  scriptbeg += "#PBS -N " + jobname + "\n";
  scriptbeg += "#PBS -l walltime=00:" + str(mins) + ":00\n";
  scriptbeg += "#PBS -l nodes=" + str(num_nodes) + ":ppn=24\n";
  #scriptbeg += "#PBS -j oe\n";
  return scriptbeg

def getPValue(num_nodes, proc_per_node, mode):
  if mode == "smp":
    if num_nodes == 1:
      return ppn - 1
    else:
      p = (ppn/proc_per_node - 1)*proc_per_node*num_nodes
      return p
  else:
    return ppn * num_nodes

def getPostArgs(num_nodes, proc_per_node, mode):
  if mode == "smp":
    if num_nodes == 1:
      return " ++ppn " + str(ppn - 1) + space + " +pemap 0-22 +commap 23"
    else:
      return " ++ppn " + str(ppn/proc_per_node - 1) + space + " +pemap 0-10,12-22 +commap 11,23"
  else:
    return ""

def getPostPostArgs(basebuild, mode, append):
  if key == 'iforge':
    if basebuild == 'verbs':
      if mode == 'smp':
        return "++nodelist ~/nodelist" + append + ".smp"
      else:
        return "++nodelist ~/nodelist" + append
  return ""

while num_nodes <= max_nodes:
  smp_index=0
  for archopt_str in archopts_str:
    scriptname = "bcast_test_" + str(num_nodes) + "_" + archopts[smp_index];
    fileContents= getPbsScriptBeg(num_nodes, 30, scriptname);

    fileContents += "~/gennodelist2.pl $PBS_NODEFILE $PBS_JOBID "+ str(num_nodes * ppn) + " _" + scriptname + "\n"
    for basebuild in basebuilds[key]:
      exampleFullDir = basedirs[key] + slash +  basebuild + archmap[key] + archopts_str1[smp_index] + hyphen + suffix + exampleDir
      outputDir = charmutilsdirs[key] + slash + "results/" + key + slash + "bcast/";
      scriptDir = charmutilsdirs[key] + slash + "scripts/" + key + slash + "bcast/";

      # run bcast
      bcastFullDir = exampleFullDir + slash + "bcastPingAll/";
      charmRunDir  = bcastFullDir + "/charmrun ";
      execPath     = bcastFullDir + "/ping_all ";
      pval         = str(getPValue(num_nodes, proc_per_node, archopts[smp_index]))
      args         = " 16 33554432 10 4 0 "
      postargs     = getPostArgs(num_nodes, proc_per_node, archopts[smp_index])
      postpostargs = getPostPostArgs(basebuild, archopts[smp_index], "_" + scriptname)
      outputFile   = outputDir + "reg_bcast_test_" + str(num_nodes) + "_" + basebuild + "_" + archopts[smp_index]

      runComm = charmRunDir + space + "+p" + pval + space + execPath + space + args + space + postargs + space + postpostargs + " > " + outputFile
      fileContents += runComm + "\n\n\n\n"

      # run RO Bcast
      roBcastFullDir = exampleFullDir + slash + "readonlyBcast/";
      charmRunDir  = roBcastFullDir + "/charmrun ";
      execPath1    = roBcastFullDir + "/readonlyBcast ";
      execPath2    = roBcastFullDir + "/readonlyZCBcast ";
      pval         = str(getPValue(num_nodes, proc_per_node, archopts[smp_index]))
      postargs     = getPostArgs(num_nodes, proc_per_node, archopts[smp_index])
      postpostargs = getPostPostArgs(basebuild, archopts[smp_index], "_" + scriptname)
      outputFile   = outputDir + "ro_bcast_test_" + str(num_nodes) + "_" + basebuild + "_" + archopts[smp_index]

      two_power = 4;
      while (two_power <= 25):
        ro_size = 2**two_power;
        args         = str(ro_size);
        runComm1 = charmRunDir + space + "+p" + pval + space + execPath1 + space + args + space + postargs + space + postpostargs + (" > " if (two_power == 4) else " >> ") + outputFile
        runComm2 = charmRunDir + space + "+p" + pval + space + execPath2 + space + args + space + postargs + space + postpostargs + " >> " + outputFile
        fileContents += runComm1 + "\n"
        fileContents += runComm2 + "\n\n\n\n"
        two_power = two_power + 1
    #print "======================================================="
    #print fileContents
    #print "======================================================="
    script = open(scriptDir + scriptname, "w+");
    script.write(fileContents)
    sys.stdout.flush();
    smp_index = smp_index + 1;
  num_nodes = num_nodes*2


#
#def getRunCommand(charmrunbase, execu, run_proc, args, archopt):
#  runcommand = charmrunbase + space + "+p"+str(run_proc) + space + execu + space + args + space + extraRun + " ++nodelist ~/nodelist"
#  if(archopts=="smp"):
#    runcommand += ".smp"
#
#  return runcommand
#
#outputdir = outputbase + expname + "/"
#
#i=0
#for archopt in archopts_str:
#  scriptname= "script" + "_" + expname + "_" + str(run_proc) + "_" + example + "_" + archopts[i]
#  filecontents = scriptbases[i]
#
#  #filecontents += "current directory is $PWD\n";
#  filecontents += "~/gennodelist2.pl $PBS_NODEFILE $PBS_JOBID 24\n";
#
#  execu_base =  basedir + basearch + archopt + postdir
#  for reg_mode in reg_modes:
#    charmrunbase = execu_base + reg_mode + "/" + example + "/" + "charmrun"
#    execu = execu_base + reg_mode + "/" + example + "/" + example
#    runcommand = getRunCommand(charmrunbase, execu, run_proc, args[i], archopts[i])
#
#    outputfile = expname + "_" + archopts[i] + "_" + reg_mode + "_" + str(run_proc)
#    runcommand_out = runcommand + " > " + outputdir + outputfile
#    filecontents += runcommand_out + "\n"
#
#  print filecontents
#  print "============================"
#
#
#  script = open(scriptname, "w+");
#  script.write(filecontents)
#  sys.stdout.flush();
#  i += 1
#
