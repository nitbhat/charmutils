from charm_header import *

def getRunCommand(charmrunbase, execu, run_proc, args, archopt):
  runcommand = charmrunbase + space + "+p"+str(run_proc) + space + execu + space + args + space + extraRun + " ++nodelist ~/nodelist"
  if(archopts=="smp"):
    runcommand += ".smp"

  return runcommand

outputdir = outputbase + expname + "/"

i=0
for archopt in archopts_str:
  scriptname= "script" + "_" + expname + "_" + str(run_proc) + "_" + example + "_" + archopts[i]
  filecontents = scriptbases[i]

  #filecontents += "current directory is $PWD\n";
  filecontents += "~/gennodelist2.pl $PBS_NODEFILE $PBS_JOBID 24\n";

  execu_base =  basedir + basearch + archopt + postdir
  for reg_mode in reg_modes:
    charmrunbase = execu_base + reg_mode + "/" + example + "/" + "charmrun"
    execu = execu_base + reg_mode + "/" + example + "/" + example
    runcommand = getRunCommand(charmrunbase, execu, run_proc, args[i], archopts[i])

    outputfile = expname + "_" + archopts[i] + "_" + reg_mode + "_" + str(run_proc)
    runcommand_out = runcommand + " > " + outputdir + outputfile
    filecontents += runcommand_out + "\n"

  print filecontents
  print "============================"


  script = open(scriptname, "w+");
  script.write(filecontents)
  sys.stdout.flush();
  i += 1

