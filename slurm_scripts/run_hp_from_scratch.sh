#!/bin/bash -l
#SBATCH --job-name=hpDss
#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=16gb
#SBATCH --account=svillar3
#SBATCH --array=1-50

export GERRYCHAIN_RANDOM_SEED=$RANDOM
echo $GERRYCHAIN_RANDOM_SEED
echo $SLURM_ARRAY_TASK_ID

module load python/3.11.6
source /home/ext-harlin/.venv/bin/activate

cd MRC_redistricting

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn unbiased_chains/NC/unbiased_PRES16_50000.pkl --proposal random
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn unbiased_chains/NC/unbiased_PRES12_50000.pkl --proposal random

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Republican_mean_median_10000_1719428053.pkl --proposal random
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Republican_mean_median_10000_1719427359.pkl --proposal random

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Republican_efficiency_gap_10000_1719433844.pkl --proposal random
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Republican_efficiency_gap_10000_1719432986.pkl --proposal random

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Democratic_efficiency_gap_10000_1719433105.pkl --proposal random
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Democratic_efficiency_gap_10000_1719433873.pkl --proposal random

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Democratic_mean_median_10000_1719428562.pkl --proposal random
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Democratic_mean_median_10000_1719427835.pkl --proposal random

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Republican_partisan_bias_10000_1719436407.pkl --proposal random
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Republican_partisan_bias_10000_1719436777.pkl --proposal random

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Democratic_partisan_bias_10000_1719436496.pkl --proposal random
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Democratic_partisan_bias_10000_1719435728.pkl --proposal random

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Republican_partisan_gini_10000_1719440298.pkl --proposal random
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Republican_partisan_gini_10000_1719440281.pkl --proposal random

#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Republican_safe_seats_10000_1719443078.pkl --proposal random --e 0.003 --a 0.05
#python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Republican_safe_seats_10000_1719443107.pkl --proposal random --e 0.003 --a 0.05

python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES12_Democratic_safe_seats_10000_1719443196.pkl --proposal random --e 0.003 --a 0.05
python -u ./run_hp_from_scratch.py --k 200000 --m 32 --map random --fn biased_chains/NC/shortburst_PRES16_Democratic_safe_seats_10000_1719444352.pkl --proposal random --e 0.003 --a 0.05

