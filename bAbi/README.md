# How to run 

## Setup Everytime
### On Greene:
```bash
# Run to initialize a gpu job
sbatch '/scratch/<Netid>/set_up.sbatch'

# Run to check job status
squeue -u <Netid>

# Change Config to Nodelist
#JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
#          27382870   rtx8000 request_  <Netid>  R       0:02      1 gr006
```

### Login to BurstInstance
### On BurstInstance
```bash
# Run to start singularity
singularity exec --nv\
     --overlay /scratch/<Netid>/pytorch-example/overlay-50G-10M.ext3:ro /scratch/work/public/singularity/cuda11.2.2-cudnn8-devel-ubuntu20.04.sif /bin/bash
```

### On Singularity

```bash
# Run to start environment
source /ext3/env.sh
conda activate base
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```


## Setup For The First Time

### On Greene:
```bash
# Create set_up.sbatch under scratch/<Netid>
cat scratch/<Netid>/set_up.sbatch

# Copy the following setup into set_up.sbatch
'#!/bin/bash
#
#SBATCH --job-name=request_gpu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=3
#SBATCH --gres=gpu:rtx8000:1
#SBATCH --time=05:00:00
#SBATCH --mem=96GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=<Netid>@nyu.edu
#SBATCH --output=request_gpu.out

sleep 8h'

# Run to initialize a gpu job
sbatch '/scratch/<Netid>/set_up.sbatch'

# Run to check job status
squeue -u <Netid>

# Change Config to Nodelist
#JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
#          27382870   rtx8000 request_  <Netid>  R       0:02      1 gr006
```

## Login to BurstInstance
### On BurstInstance
``` bash
# make directory
mkdir /scratch/<NetID>/pytorch-example

# change directory to pytorch-example
cd /scratch/<NetID>/pytorch-example

# check usable overlay
ls /scratch/work/public/overlay-fs-ext3

# choose your overlay and copy it to folder
cp -rp /scratch/work/public/overlay-fs-ext3/overlay-50GB-10M.ext3.gz .

# unzip the file
gunzip overlay-50GB-10M.ext3.gz

# Choose a corresponding Singularity image
/scratch/work/public/singularity/cuda11.2.2-cudnn8-devel-ubuntu20.04.sif

# Run to start singularity
singularity exec --nv\
     --overlay /scratch/<Netid>/pytorch-example/overlay-50G-10M.ext3:rw /scratch/work/public/singularity/cuda11.2.2-cudnn8-devel-ubuntu20.04.sif /bin/bash
```

### On Singularity

```bash
# Run to start environment
source /ext3/env.sh
conda activate base
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# install necessay packages
```

