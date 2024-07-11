#!/bin/bash -l
#SBATCH --job-name=metrics
#SBATCH --time=5:0:0
#SBATCH --mem=24g

module load python/3.11.6
source /home/ext-harlin/.venv/bin/activate
cd MRC_redistricting

##### calculate and save biased chain metrics
python -u ./calculate_metrics.py --state NC 
python -u make_hists.py --state NC --s 50

