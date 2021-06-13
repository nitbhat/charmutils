from charm_header import *
num_nodes=2
max_nodes=8
ppn = ppnmap[key]
proc_per_node=proc_per_node_map[key]

print "key is " + key

print " basedir is " + basedirs[key]




while num_nodes <= max_nodes:
  smp_index=0
  for archopt_str in archopts_str:
    scriptname = "reg_bcast_test_" + str(num_nodes) + "_" + archopts[smp_index];
    outputDir = charmutilsdirs[key] + slash + "results/" + key + slash + "bcast/";

    for basebuild in basebuilds[key]:
      scriptDir = charmutilsdirs[key] + slash + "scripts/" + key + slash + "bcast/";

      print "sbatch "+scriptDir + scriptname
      os.system("sbatch "+scriptDir + scriptname)

    smp_index = smp_index + 1;
  num_nodes = num_nodes*2
