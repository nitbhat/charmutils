import os
import sys

basebuild="ofi"
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


archopts=["nonsmp","smp"]
archopts_str=["","-smp"]

space=" "
target="charm++"
basearch = basebuild+"-linux-x86_64"
options = " --with-production --enable-error-checking "
build_proc=16
num_proc = " -j"+str(build_proc) + " "
debug_opts=""

postdir="/examples/charm++/zerocopy/direct_api/"

reg_modes=["reg","prereg","unreg"]
example="pingpong"
run_proc = 2
expname="directvsregrdma"

filecontents=""

args=["32 33554432 1000 100","32 33554432 1000 100 ++ppn 1 +pemap 0 +commap 1"]
