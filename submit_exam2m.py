from charm_header import *

num_nodes=32
max_nodes=32

proj=True

while num_nodes <= max_nodes:
  #voxLens = [0.008, 0.01, 0.05]
  #voxLens = [0.025, 0.075]
  voxLens = [0.01, 0.025, 0.05, 0.075]
  for vox in voxLens:

    voxLen = str(vox)

    scriptDir = "/global/cscratch1/sd/nbhat4/ExaM2M/scripts/generatedScripts/"

    scriptname = "exam2m_mpi_nonsmp_sphere_cube_" + str(num_nodes) + "_" + voxLen


    if(proj):
      scriptname += "_proj"

    scriptname += "_script";

    print "sbatch "+scriptDir + scriptname
    os.system("sbatch "+scriptDir + scriptname)
  num_nodes = num_nodes*2
