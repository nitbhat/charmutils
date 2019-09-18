from charm_header import *
import numpy as np

num_nodes=1
max_nodes=32
ppn = ppnmap[key]
proc_per_node=proc_per_node_map[key]

#regular, bcast send reg, bcast post reg
def parseFromOutputFileNumpy(filename, basebuild, archopt_str):
  header_skip_lines = skipHeaderLineMap[basebuild]

  if(archopt_str == "smp"):
    header_skip_lines += smpSkipLinesModifierMap[basebuild]

  data = np.genfromtxt(filename, dtype=[int, int, float, float, float, float, float, float, float, float, float], skip_header=header_skip_lines, skip_footer=1, delimiter=",", usecols=(0, 2, 4, 6, 9))
  return data


#Testing Data

#data = parseFromOutputFileNumpy('/pylon5/ac7k4vp/nbhat4/charmutils/results/bridges/bcast/reg_bcast_test_1_ofi_smp', 'ofi', 'smp')
#print data

myBaseBuild = "mpi"
myArchOpt = ""

smp_index=0
for archopt_str in archopts_str:
  for basebuild in basebuilds[key]:
    if(myBaseBuild == basebuild and myArchOpt == archopt_str):
      print "Basebuild:" + basebuild + "    Archopt:" + archopt_str
      print "======================================================="

      num_nodes=1
      database = []
      while num_nodes <= max_nodes:
        extraSuffix= ""
        outputFile = getOutputFile(num_nodes, archopt_str, smp_index, basebuild, extraSuffix)

        print outputFile
        data = parseFromOutputFileNumpy(outputFile, basebuild, archopt_str)
        database.append(data);
        print "Num Nodes: " + str(num_nodes) + "  done, and size is " + str(len(data))

        num_nodes = num_nodes*2
      print "All data elems added and size is " + str(len(database))
    print "======================================================="
  smp_index = smp_index + 1;

msg_size = 1048576
row_index = 15
node_index = 0
for data in database:
  num_nodes = 2**node_index;
  myRow = data[row_index]
  print str(num_nodes) + "," + str((ppn * num_nodes)) + "," + str(myRow[1]) + "," + str(myRow[2]) + "," + str(myRow[3]) + "," + str(myRow[4])
  node_index += 1
