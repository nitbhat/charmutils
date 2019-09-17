import os
import sys
from os import path
import socket

hostname_full = socket.gethostname();
#os.system('hostname')

print hostname_full

if(hostname_full.find('bridges') != -1):
  key='bridges'
elif(hostname_full.find('cori') != -1):
  key="cori"
else:
  key = 'iforge'

buildType = 'prod'
basedirs = {
    "iforge" : ["/ui/cwi/nitin/software/charm","/ui/cwi/nitin/software/charm"],
    "cori" : "/global/homes/n/nbhat4/software/charm_2",
    "bridges" : "/pylon5/ac7k4vp/nbhat4/charm",
    "hpcadv" : "/global/home/users/nitinb/charm_1"
}

charmutilsdirs = {
    "iforge" : "/ui/cwi/nitin/software/charmutils",
    "cori" : "/global/homes/n/nbhat4/software/charmutils",
    "bridges" : "/pylon5/ac7k4vp/nbhat4/charmutils",
    "hpcadv" : "/global/home/users/nitinb/charmutils"
}

basebuilds = {
    "hpcadv" : ["ucx","verbs","mpi"],
    "iforge" : ["verbs","mpi"],
    "cori" : ["mpi","gni"],
    "bridges" : ["mpi","ofi"]
}

archmap = {
    "hpcadv" : "-linux-x86_64",
    "iforge" : "-linux-x86_64",
    "cori" : "-crayxc",
    "bridges" : "-linux-x86_64"
}

ppnmap = {
    "hpcadv" : 32,
    "iforge" : 24,
    "cori" : 24,
    "bridges" : 28
}

proc_per_node_map = {
    "hpcadv" : 2,
    "iforge" : 2,
    "cori" : 2,
    "bridges" : 2
}

launcher_map = {
    "hpcadv" : "charmrun",
    "iforge" : "charmrun",
    "cori" : "srun",
    "bridges" : "mpirun"
}

jobscheds = {
    "hpcadv" : "slurm",
    "iforge" : "pbs",
    "cori" : "slurm",
    "bridges" : "slurm"
}

exampleDir = "/benchmarks/charm++/zerocopy/"
archopts=["nonsmp","smp"]
archopts_str=["","smp"]
archopts_str1=["","-smp"]

buildTypeMap = {
    "prod" : "--with-production --enable-error-checking --suffix=prod",
    "debug" : "--enable-error-checking --suffix=debug"
}

buildTypeMap2 = {
    "prod" : "",
    "debug" : " -g -O0 "
}

#archopts=["smp"]
#archopts_str=["smp"]
#archopts_str1=["-smp"]
#
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
