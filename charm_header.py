import os
import sys
from os import path
import socket

hostname_full = socket.gethostname();
os.system('hostname')

print ("host name is " +hostname_full)

if(hostname_full.find('bridges') != -1):
  key='bridges'
elif(hostname_full.find('cori') != -1):
  key="cori"
elif(hostname_full.find('golub') != -1):
  key="golub"
elif(hostname_full.find('hpcadv') != -1):
  key="hpcadv"
elif(hostname_full.find('frontera') != -1):
  key="frontera"
elif(hostname_full.find('courage') != -1):
  key="courage"
elif(hostname_full.find('MacBook') != -1):
  key="macbook"
else:
  key = 'iforge'

buildType = 'prod'

basedirs = {
    "iforge" : "/ui/cwi/nitin/software/charm",
    "cori" : "/project/projectdirs/m2609/nitin/charm",
    "bridges" : "/pylon5/ac7k4vp/nbhat4/charm",
    "hpcadv" : "/global/home/users/nitinb/charm",
    "golub" : "/home/nbhat4/scratch/charm",
    "frontera" : "/scratch1/03808/nbhat4/charm",
    "courage" : "/scratch/nitin/charm_1",
    "macbook" : "/Users/nitinbhat/Work/software/charm"
}

charmutilsdirs = {
    "iforge" : "/ui/cwi/nitin/software/charmutils",
    "cori" : "/project/projectdirs/m2609/nitin/charmutils",
    "bridges" : "/pylon5/ac7k4vp/nbhat4/charmutils",
    "hpcadv" : "/global/home/users/nitinb/charmutils",
    "golub" : "/home/nbhat4/scratch/charmutils",
    "frontera" : "/work/03808/nbhat4/frontera/charmutils",
    "courage" : "/scratch/nitin/charmutils",
    "macbook" : "/Users/nitinbhat/Work/software/charmutils"
}

appdirs = {
    "iforge" : "",
    "cori" : "/project/projectdirs/m2609/nitin/particleExercise",
    "bridges" : "/pylon5/ac7k4vp/nbhat4/particleExercise",
    "hpcadv" : "",
    "golub" : "/home/nbhat4/scratch/charmutils",
    "courage" : "/scratch/nitin/particleExercise",
    "macbook" : "/Users/nitinbhat/Work/software/particleSimulation",
    "frontera" : "/scratch1/03808/nbhat4/particleExercise"
}

exam2mdirs = {
    "cori" : "/global/cscratch1/sd/nbhat4/ExaM2M/",
    "frontera" : "/scratch1/03808/nbhat4/ExaM2M/"
}





basebuilds = {
    "hpcadv" : ["ucx","mpi","verbs"],
    "frontera" : ["ucx","mpi"],
    "iforge" : ["verbs","mpi"],
    "cori" : ["mpi","gni"],
    "bridges" : ["mpi","ofi"],
    "golub" : ["ucx","mpi","verbs"],
    "macbook" : ["netlrts","mpi"],
    "courage" : ["netlrts","mpi"]
}

buildbasedirs = {
"hpcadv" : ["/global/home/users/nitinb/ucx-1.6.1/build", "/global/home/users/nitinb/openmpi-4.0.1/build"]
}

archmap = {
    "hpcadv" : "-linux-x86_64",
    "frontera" : "-linux-x86_64",
    "iforge" : "-linux-x86_64",
    "cori" : "-crayxc",
    "bridges" : "-linux-x86_64",
    "golub" : "-linux-x86_64",
    "macbook": "-darwin-x86_64",
    "courage" : "-linux-x86_64"
}

ppnmap = {
    "hpcadv" : 32,
    "frontera" : 56,
    "iforge" : 24,
    "cori" : 32,
    "edison" : 24,
    "bridges" : 28,
    "golub" : 24
}

proc_per_node_map = {
    "hpcadv" : 2,
    "frontera" : 2,
    "iforge" : 2,
    "cori" : 2,
    "bridges" : 2,
    "golub" : 2
}

launcher_map = {
    "hpcadv" : "charmrun",
    "iforge" : "charmrun",
    "cori" : "srun",
    "bridges" : "mpirun",
    "golub" : "charmrun",
}

jobscheds = {
    "hpcadv" : "slurm",
    "iforge" : "pbs",
    "cori" : "slurm",
    "bridges" : "slurm",
    "golub" : "pbs",
    "frontera" : "slurm",
}

preBuildEnv = {
  "ucx" : "module load impi/19.0.5",
  "impi" : "module load impi/19.0.5",
  "mpich" : "export PATH=/work/03808/nbhat4/frontera/mpich-3.3.2/build/bin:$PATH && export LD_LIBRARY_PATH=/work/03808/nbhat4/frontera/mpich-3.3.2/build/lib:$LD_LIBRARY_PATH",
  "mpichnoucx" : "export PATH=/work/03808/nbhat4/frontera/mpich-3.3.2/build_noucx/bin:$PATH && export LD_LIBRARY_PATH=/work/03808/nbhat4/frontera/mpich-3.3.2/build_noucx/lib:$LD_LIBRARY_PATH",
  "ompi" : "export PATH=/work/03808/nbhat4/frontera/ompi/build/bin:$PATH && export LD_LIBRARY_PATH=/work/03808/nbhat4/frontera/ompi/build/lib:$LD_LIBRARY_PATH",
  "ompinoucx" : "export PATH=/work/03808/nbhat4/frontera/ompi/build_noucx/bin:$PATH && export LD_LIBRARY_PATH=/work/03808/nbhat4/frontera/ompi/build_noucx/lib:$LD_LIBRARY_PATH",
  "ucxompi" : "export PATH=/work/03808/nbhat4/frontera/ompi/build/bin:$PATH && export LD_LIBRARY_PATH=/work/03808/nbhat4/frontera/ompi/build/lib:$LD_LIBRARY_PATH"
  #"mpich" : "/work/03808/nbhat4/frontera/mpich-3.3.2/build/bin:$PATH",
  #"mpichnoucx" : "/work/03808/nbhat4/frontera/mpich-3.3.2/build_noucx/bin:$PATH",
  #"ompi" : "/work/03808/nbhat4/frontera/ompi/build/bin:$PATH",
  #"ompinoucx" : "/work/03808/nbhat4/frontera/ompi/build_noucx/bin:$PATH",
  #"ucxompi" : "/work/03808/nbhat4/frontera/ompi/build/bin:$PATH"

}

frontera_basedir = {
  "ucx" : "/work/03808/nbhat4/frontera/ucx/build_1.6.1",
  "impi" : "$TACC_IMPI_DIR/intel64/",
  "mpich" : "/work/03808/nbhat4/frontera/mpich-3.3.2/build",
  "mpichnoucx" : "/work/03808/nbhat4/frontera/mpich-3.3.2/build_noucx",
  "ompi" : "/work/03808/nbhat4/frontera/ompi/build",
  "ompinoucx" : "/work/03808/nbhat4/frontera/ompi/build_noucx",
  "ucxompi" : "/work/03808/nbhat4/frontera/ompi/build"
}

frontera_basebuilds = {
  "ucx" : "ucx",
  "impi" : "mpi",
  "mpich" : "mpi",
  "mpichnoucx" : "mpi",
  "ompi" : "mpi",
  "ompinoucx" : "mpi",
  "ucxompi" : "ucx"
}



exampleDir = "/benchmarks/charm++/zerocopy"
archopts=["nonsmp","smp"]
archopts_str=["","smp"]
archopts_str1=["","-smp"]

buildTypeMap = {
    "prod" : "--with-production --enable-error-checking --suffix=prod",
    "debug" : "--enable-error-checking --suffix=debug",
    "debug2" : "--enable-error-checking --suffix=debug2 "
}

buildTypeMap2 = {
    "prod" : "",
    "debug" : " -g ",
    "debug2" : " -g -O0 "
}

skipHeaderLineMap = {
    "ofi" : 20,
    "mpi" : 10
}

smpSkipLinesModifierMap = {
    "mpi" : 2,
    "ofi" : 3
}

#archopts=["smp"]
#archopts_str=["smp"]
#archopts_str1=["-smp"]
#
hyphen="-"
slash="/"
space=" "
target="charm++"
#target="ChaNGa"
suffix="prod"
#basearch = basebuild+"-linux-x86_64"
options = " --with-production --enable-error-checking --suffix="+suffix
build_proc=16
num_proc = " -j"+str(build_proc) + " "
debug_opts=""



##buildmodes = ["smp","nonsmp"]
#
#
##basebuild="verbs"
##basedir="/home/nbhat4/scratch/charm/" #golub
#
##basedir="/ui/cwi/nitin/software/charm/"
#
#
##outputbase="/home/nbhat4/scratch/results/zc_exp/" #golub
##outputbase="/ui/cwi/nitin/software/charmutils/results/iforge/zc_exp/" #iforge
##outputbase="/Users/nitinbhat/Work/software/charmutils/results/iforge/zc_exp/" #iforge
#
##scriptbases=[
##"#!/bin/bash\n\
###PBS -l walltime=00:10:00\n\
###PBS -l nodes=2:ppn=1\n\
###PBS -N myjob\n\
###PBS -j oe\n",
##"#!/bin/bash\n\
###PBS -l walltime=00:20:00\n\
###PBS -l nodes=2:ppn=2\n\
###PBS -N myjob\n\
###PBS -j oe\n"]
##
#extraRun=""
#
#basedir="/pylon5/ac7k4vp/nbhat4/charm/"
#outputbase="/pylon5/ac7k4vp/nbhat4/charmutils/results/bridges_ofi/zc_exp/"
#
#scriptbases=[
#"#!/bin/bash\n\
##SBATCH -N 2\n\
##SBATCH -p RM\n\
##SBATCH -t 0:20:00\n\
##SBATCH --ntasks-per-node 1\n",
#
#"#!/bin/bash\n\
##SBATCH -N 2\n\
##SBATCH -p RM\n\
##SBATCH -t 0:30:00\n\
##SBATCH --ntasks-per-node 1\n"]
#
##
#
#
#postdir="/examples/charm++/zerocopy/direct_api/"
#
#reg_modes=["reg","prereg","unreg"]
#example="pingpong"
#run_proc = 2
#expname="directvsregrdma"
#
#filecontents=""
#
#args=["32 33554432 1000 100","32 33554432 1000 100 ++ppn 1 +pemap 0 +commap 1"]
#
##Util Methods
#
#def getOutputFile(num_nodes, archopt_str, smp_index, basebuild, extraSuffix):
#  outputDir = charmutilsdirs[key] + slash + "results/" + key + slash + "bcast/";
#  outputFile   = outputDir + "reg_bcast_test_" + str(num_nodes) + "_" + basebuild + ("_" if extraSuffix != "" else "") + extraSuffix + "_" +  archopts[smp_index]
#  return outputFile
#
