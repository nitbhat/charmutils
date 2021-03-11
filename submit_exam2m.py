from charm_header import *

num_nodes=1
max_nodes=2
#max_nodes=1

#proj=True
proj=False

stats=False
#stats=True

prev=False
#prev=True

exam2mdir=exam2mdirs[key]
if(prev):
  exam2mdir += "_prev"

while num_nodes <= max_nodes:
  #voxLens = [0.008, 0.01, 0.05]
  #voxLens = [0.025, 0.075]
  voxLens = [0.01, 0.025, 0.05, 0.075]
  #voxLens = [0.01, 0.025, 0.075]
  #voxLens = [0.05]
  for vox in voxLens:

    voxLen = str(vox)

    scriptDir = exam2mdir + "/scripts/generatedScripts/"

    scriptname = "exam2m_mpi_nonsmp_sphere_cube_" + str(num_nodes) + "_" + voxLen

    if(prev):
      scriptname += "_prev"



    if(stats):
      scriptname += "_stats"

    if(proj):
      scriptname += "_proj"

    scriptname += "_script";

    print "sbatch "+scriptDir + scriptname
    os.system("sbatch "+scriptDir + scriptname)
  num_nodes = num_nodes*2
