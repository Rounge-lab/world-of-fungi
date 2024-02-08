#!/bin/bash

#SBATCH --job-name eukdetect   ## Name of the job
#SBATCH --output eukdetect-run1   ## Name of the output-script (%j will be replaced with job number)
#SBATCH --account nn9383k   ## The billed account
#SBATCH --time=10:30:00   ## Walltime of the job
#SBATCH --partition=bigmem   ## Selected partition
#SBATCH --mem-per-cpu=30000   ## Memory allocated to each task
#SBATCH --ntasks=10   ## Number of tasks that will be allocated
#SBATCH --nodes=1   ## Number of nodes that will be allocated

set -o errexit   ## Exit the script on any error
set -o nounset   ## Treat any unset variables as an error

eukdetect --mode runall --configfile /cluster/projects/nn9383k/arfa/eukdetect/EukDetect/eukdetect_configfile.yml --cores 32   ## Command to be run