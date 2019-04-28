#!/bin/bash -l
#SBATCH -q debug
#SBATCH -N 2
#SBATCH -n 2
#SBATCH --ntasks-per-node 1
#SBATCH -t 00:30:00

cd /global/homes/n/nbhat4/software/charm/mpi-crayxc-smp-prod/examples/charm++/zerocopy/benchmarks/p2pPingpong
make
srun -n 2 -c 2 ./megaZCPingpong ++ppn 1 +pemap 0 +commap 1 > /global/homes/n/nbhat4/software/charmutils/results/edison/p2p/mpi_pingpong_smp_2

cd /global/homes/n/nbhat4/software/charm/gni-crayxc-smp-prod/examples/charm++/zerocopy/benchmarks/p2pPingpong
make
srun -n 2 -c 2 ./megaZCPingpong ++ppn 1 +pemap 0 +commap 1 > /global/homes/n/nbhat4/software/charmutils/results/edison/p2p/gni_pingpong_smp_2



