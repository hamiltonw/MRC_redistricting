#!/bin/bash -l
#SBATCH --job-name=metrics
#SBATCH --time=5:0:0
#SBATCH --mem=24g
#SBATCH -A svillar3

module load python/3.11.6
source /home/ext-harlin/.venv/bin/activate
cd MRC_redistricting

##### calculate and save biased chain metrics
python -u ./calculate_metrics.py --state NC 
python -u make_hists.py --state NC --s 50

##### histograms
#python -u ./make_hists.py --party Dem --sb 1 --state TX --n 1
#python -u ./make_hists.py --party Rep --sb 1 --state TX --n 1

#python -u ./make_hists.py --party Dem --sb 1 --state NC --n 1
#python -u ./make_hists.py --party Rep --sb 1 --state NC --n 1

#python -u ./make_hists.py --party Dem --sb 1 --state WI --n 1
#python -u ./make_hists.py --party Rep --sb 1 --state WI --n 1

#python -u ./make_hists.py --party Dem --sb 1 --state MD --n 1
#python -u ./make_hists.py --party Rep --sb 1 --state MD --n 1

##### heat maps
#python -u ./make_heats.py --sb 1 --state TX --n 1
#python -u ./make_heats.py --sb 1 --state NC --n 1
#python -u ./make_heats.py --sb 1 --state WI --n 1
#python -u ./make_heats.py --sb 1 --state MD --n 1

##### scatter plots
#python -u ./make_scats.py --sb 1 --state TX --n 100
#python -u ./make_scats.py --sb 1 --state NC --n 100
#python -u ./make_scats.py --sb 1 --state WI --n 100
#python -u ./make_scats.py --sb 1 --state MD --n 100
