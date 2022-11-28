#!/bin/bash
#
#SBATCH --job-name=t5-3b
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=6:00:00
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jl13072@nyu.edu
#SBATCH --output=t5-3b.out

module purge

singularity exec --nv \
     --overlay /scratch/jl13072/pytorch-example/overlay-50G-10M.ext3:ro \
     /scratch/work/public/singularity/cuda11.2.2-cudnn8-devel-ubuntu20.04.sif \
     /bin/bash \
     -c "source /ext3/env.sh; conda activate base; export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python; 
     python /scratch/jl13072/Spatial-Reasoners-Ver2.0/bAbi/scripts/test.py \
     t5-3b;
     python /scratch/jl13072/Spatial-Reasoners-Ver2.0/bAbi/scripts/analyze.py \
     t5-3b;
"