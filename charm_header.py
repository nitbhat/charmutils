import os
import sys

key = 'iforge'
basedirs = {
    "iforge" : "/ui/cwi/nitin/software/charm",
    "edison" : "/global/homes/n/nbhat4/software/charm",
    "bridges" : "/pylon5/ac7k4vp/nbhat4/charm"
}

charmutilsdirs = {
    "iforge" : "/ui/cwi/nitin/software/charmutils",
    "edison" : "/global/homes/n/nbhat4/software/charmutils",
    "bridges" : "/pylon5/ac7k4vp/nbhat4/charmutils"
}

basebuilds = {
    "iforge" : ["verbs","mpi"],
    "edison" : ["mpi","gni"],
    "bridges" : ["mpi","ofi"]
}

archmap = {
    "iforge" : "-linux-x86_64",
    "edison" : "-crayxc",
    "bridges" : "-linux-x86_64"
}

ppnmap = {
    "iforge" : 24,
    "edison" : 24,
    "bridges" : 28
}

proc_per_node_map = {
    "iforge" : 2,
    "edison" : 2,
    "bridges" : 2
}

launcher_map = {
    "iforge" : "charmrun",
    "edison" : "srun",
    "bridges" : "mpirun"
}

jobscheds = {
    "iforge" : "pbs",
    "edison" : "slurm",
    "bridges" : "slurm"
}

exampleDir = "/examples/charm++/zerocopy/benchmarks/"

archopts=["nonsmp","smp"]
archopts_str=["","smp"]
archopts_str1=["","-smp"]

hyphen="-"
slash="/"
space=" "
target="charm++"
suffix="prod"
#basearch = basebuild+"-linux-x86_64"
options = " --with-production --enable-error-checking --suffix="+suffix
build_proc=16
num_proc = " -j"+str(build_proc) + " "
debug_opts=""



#buildmodes = ["smp","nonsmp"]


#basebuild="verbs"
#basedir="/home/nbhat4/scratch/charm/" #golub

#basedir="/ui/cwi/nitin/software/charm/"

header_skip_lines=26

#outputbase="/home/nbhat4/scratch/results/zc_exp/" #golub
#outputbase="/ui/cwi/nitin/software/charmutils/results/iforge/zc_exp/" #iforge
#outputbase="/Users/nitinbhat/Work/software/charmutils/results/iforge/zc_exp/" #iforge

#scriptbases=[
#"#!/bin/bash\n\
##PBS -l walltime=00:10:00\n\
##PBS -l nodes=2:ppn=1\n\
##PBS -N myjob\n\
##PBS -j oe\n",
#"#!/bin/bash\n\
##PBS -l walltime=00:20:00\n\
##PBS -l nodes=2:ppn=2\n\
##PBS -N myjob\n\
##PBS -j oe\n"]
#
extraRun=""

basedir="/pylon5/ac7k4vp/nbhat4/charm/"
outputbase="/pylon5/ac7k4vp/nbhat4/charmutils/results/bridges_ofi/zc_exp/"

scriptbases=[
"#!/bin/bash\n\
#SBATCH -N 2\n\
#SBATCH -p RM\n\
#SBATCH -t 0:20:00\n\
#SBATCH --ntasks-per-node 1\n",

"#!/bin/bash\n\
#SBATCH -N 2\n\
#SBATCH -p RM\n\
#SBATCH -t 0:30:00\n\
#SBATCH --ntasks-per-node 1\n"]

#


postdir="/examples/charm++/zerocopy/direct_api/"

reg_modes=["reg","prereg","unreg"]
example="pingpong"
run_proc = 2
expname="directvsregrdma"

filecontents=""

args=["32 33554432 1000 100","32 33554432 1000 100 ++ppn 1 +pemap 0 +commap 1"]
