import os
import sys

archopts=["nonsmp","smp"]
archopts_str=["","-smp"]

space=" "
target="charm++"
basearch = "ofi-linux-x86_64"
options = " --with-production --enable-error-checking "
build_proc=16
num_proc = " -j"+str(build_proc) + " "
debug_opts=""

basedir="/pylon5/ac7k4vp/nbhat4/charm/"
postdir="/examples/charm++/zerocopy/direct_api/"

outputbase="/pylon5/ac7k4vp/nbhat4/results/zc_exp/"

reg_modes=["reg","prereg","unreg"]
example="pingpong"
run_proc = 2
expname="directvsregrdma"

scriptbases=[
"#!/bin/bash\n\
#SBATCH -N 2\n\
#SBATCH -p RM\n\
#SBATCH -t 0:10:00\n\
#SBATCH --ntasks-per-node 1\n",

"#!/bin/bash\n\
#SBATCH -N 2\n\
#SBATCH -p RM\n\
#SBATCH -t 0:10:00\n\
#SBATCH --ntasks-per-node 2\n"]

filecontents=""

args=["32 33554432 1000 100","32 33554432 1000 100 ++ppn 1 +pemap 0 +commap 1"]
