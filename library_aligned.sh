#!/bin/bash

#SBATCH --job-name=lib_aligned
#SBATCH --mem=10G
#SBATCH --time=6:00:00

module load python/3.latest
srun ./library_aligned.py "$@"

