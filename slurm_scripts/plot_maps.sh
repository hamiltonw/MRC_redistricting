#!/bin/bash -l
#SBATCH --job-name=map
#SBATCH --time=0:30:0
#SBATCH --mem-per-cpu=12gb 
#SBATCH --account=svillar3

export GERRYCHAIN_RANDOM_SEED=$RANDOM
echo $GERRYCHAIN_RANDOM_SEED

module load python/3.11.6
source /home/ext-harlin/.venv/bin/activate

cd MRC_redistricting

# Need to change these for descartes 1.1.0 and shapely 2.0.1 
# https://stackoverflow.com/questions/75287534/indexerror-descartes-polygonpatch-wtih-shapely
# https://stackoverflow.com/questions/38930192/how-to-extract-polygons-from-multipolygons-in-shapely

# plot random map
python -u plot_maps.py --fn 'biased_chains/NC/shortburst_PRES16_Republican_mean_median_10000_1719427359.pkl' 

# plot one specific map
python -u plot_maps.py --fn 'biased_chains/NC/shortburst_PRES16_Republican_mean_median_10000_1719427359.pkl' --i 0

# plot multiple specific maps
python -u plot_maps.py --fn 'biased_chains/NC/shortburst_PRES16_Republican_mean_median_10000_1719427359.pkl' --i 1,10000,40000
