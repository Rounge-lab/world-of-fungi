#!/bin/bash

#SBATCH --job-name   ## Name of the job
#SBATCH --output   ## Name of the output-script (%j will be replaced with job number)
#SBATCH --account    ## The billed account
#SBATCH --time=00:00:00   ## Walltime of the job
#SBATCH --partition=bigmem   ## Selected partition
#SBATCH --mem-per-cpu=   ## Memory allocated to each task
#SBATCH --ntasks=   ## Number of tasks that will be allocated
#SBATCH --nodes=   ## Number of nodes that will be allocated

set -o errexit   ## Exit the script on any error
set -o nounset   ## Treat any unset variables as an error

eukdetect --mode runall --configfile ./configfile.yml --cores    ## Command to be run
