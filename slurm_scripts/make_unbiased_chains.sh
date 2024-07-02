#!/bin/bash -l
#SBATCH --job-name=ubPA
#SBATCH --time=24:0:0 
#SBATCH --mem-per-cpu=16gb 
#SBATCH --account=svillar3

module load python/3.11.6
source /home/ext-harlin/.venv/bin/activate

export GERRYCHAIN_RANDOM_SEED=$RANDOM
echo $GERRYCHAIN_RANDOM_SEED

cd MRC_redistricting

python -u ./make_unbiased_chain.py --election PRES16 --state PA
#python -u ./make_unbiased_chain.py --election PRES16 --state NC
#python -u ./make_unbiased_chain.py --election PRES16 --state WI
#python -u ./make_unbiased_chain.py --election PRES16 --state MD
#python -u ./make_unbiased_chain.py --election PRES16 --state TX

#python -u ./make_unbiased_chain.py --election PRES16 --state NC --n 100000
#python -u ./make_unbiased_chain.py --election PRES16 --state WI --n 100000
#python -u ./make_unbiased_chain.py --election PRES16 --state MD --n 100000
#python -u ./make_unbiased_chain.py --election PRES16 --state TX --n 100000

python -u ./make_unbiased_chain.py --election PRES12 --state PA
#python -u ./make_unbiased_chain.py --election PRES12 --state NC 
#python -u ./make_unbiased_chain.py --election PRES12 --state WI
#python -u ./make_unbiased_chain.py --election PRES12 --state MD
#python -u ./make_unbiased_chain.py --election PRES12 --state TX

#python -u ./make_unbiased_chain.py --election PRES12 --state NC --n 100000
#python -u ./make_unbiased_chain.py --election PRES12 --state WI --n 100000
#python -u ./make_unbiased_chain.py --election PRES12 --state MD --n 100000
#python -u ./make_unbiased_chain.py --election PRES12 --state TX --n 100000

