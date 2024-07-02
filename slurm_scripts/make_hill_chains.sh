#!/bin/bash -l
#SBATCH --job-name=NC16
#SBATCH --time=48:0:0
#SBATCH --mem-per-cpu=40gb 
#SBATCH --account=svillar3

export GERRYCHAIN_RANDOM_SEED=$RANDOM
echo $GERRYCHAIN_RANDOM_SEED

module load python/3.11.6
source /home/ext-harlin/.venv/bin/activate

cd MRC_redistricting

##### NC #####
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias mean_median --n 10000 --sb 5 --state NC
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias efficiency_gap --n 10000 --sb 5 --state NC
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias partisan_bias --n 10000 --sb 5 --state NC
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias partisan_gini --n 10000 --sb 5 --state NC
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias safe_seats --n 10000 --sb 5 --state NC

#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias mean_median --n 10000 --sb 5 --state NC
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias efficiency_gap --n 10000 --sb 5 --state NC
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias partisan_bias --n 10000 --sb 5 --state NC
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias partisan_gini --n 10000 --sb 5 --state NC
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias safe_seats --n 10000 --sb 5 --state NC

python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias mean_median --n 50000 --state NC --diversity 1
python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias efficiency_gap --n 50000 --state NC --diversity 1
python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias partisan_bias --n 50000 --state NC --diversity 1
python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias partisan_gini --n 50000 --state NC --diversity 1
python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias safe_seats --n 50000 --state NC --diversity 1

#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias mean_median --n 50000 --state NC
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias efficiency_gap --n 50000 --state NC
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias partisan_bias --n 50000 --state NC
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias partisan_gini --n 50000 --state NC
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias safe_seats --n 50000 --state NC


##### TX #####

#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias mean_median --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias efficiency_gap --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias partisan_bias --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias partisan_gini --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias safe_seats --n 10000 --sb 5 --state TX

#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias mean_median --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias efficiency_gap --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias partisan_bias --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias partisan_gini --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias safe_seats --n 10000 --sb 5 --state TX

#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias mean_median --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias efficiency_gap --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias partisan_bias --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias partisan_gini --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias safe_seats --n 10000 --sb 5 --state TX

#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias mean_median --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias efficiency_gap --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias partisan_bias --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias partisan_gini --n 10000 --sb 5 --state TX
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias safe_seats --n 10000 --sb 5 --state TX

##### WI #####

#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias mean_median --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias efficiency_gap --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias partisan_bias --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias partisan_gini --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias safe_seats --n 10000 --sb 5 --state WI

#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias mean_median --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias efficiency_gap --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias partisan_bias --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias partisan_gini --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias safe_seats --n 10000 --sb 5 --state WI

#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias mean_median --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias efficiency_gap --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias partisan_bias --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias partisan_gini --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias safe_seats --n 10000 --sb 5 --state WI

#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias mean_median --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias efficiency_gap --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias partisan_bias --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias partisan_gini --n 10000 --sb 5 --state WI
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias safe_seats --n 10000 --sb 5 --state WI

##### MD #####

#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias mean_median --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias efficiency_gap --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias partisan_bias --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias partisan_gini --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Republican --election PRES12 --bias safe_seats --n 10000 --sb 5 --state MD

#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias mean_median --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias efficiency_gap --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias partisan_bias --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias partisan_gini --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Republican --election PRES16 --bias safe_seats --n 10000 --sb 5 --state MD

#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias mean_median --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias efficiency_gap --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias partisan_bias --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias partisan_gini --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES12 --bias safe_seats --n 10000 --sb 5 --state MD

#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias mean_median --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias efficiency_gap --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias partisan_bias --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias partisan_gini --n 10000 --sb 5 --state MD
#python -u ./make_hill_biased_chain.py --party Democratic --election PRES16 --bias safe_seats --n 10000 --sb 5 --state MD

