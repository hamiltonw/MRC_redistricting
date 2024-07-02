#!/bin/bash -l
#SBATCH --job-name=Rss
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=20gb
#SBATCH --account=svillar3

export GERRYCHAIN_RANDOM_SEED=$RANDOM
echo $GERRYCHAIN_RANDOM_SEED
echo $SLURM_ARRAY_TASK_ID

module load python/3.11.6
source /home/ext-harlin/.venv/bin/activate

cd MRC_redistricting

#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/unbiased_chains/NC/unbiased_PRES12*.pkl"
#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/unbiased_chains/NC/unbiased_PRES16*.pkl"

#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Republican_mean_median*.pkl" 
#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Republican_mean_median*.pkl" 

#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Democratic_mean_median*.pkl" 
#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Democratic_mean_median*.pkl"

#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Republican_efficiency_gap*.pkl" 
#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Republican_efficiency_gap*.pkl" 

#python -u read_hp_results.py --e 0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Democratic_efficiency_gap*.pkl" 
#python -u read_hp_results.py --e 0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Democratic_efficiency_gap*.pkl"

#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Republican_partisan_bias*.pkl" 
#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Republican_partisan_bias*.pkl" 

#python -u read_hp_results.py --e 0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Democratic_partisan_bias*.pkl" 
#python -u read_hp_results.py --e 0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Democratic_partisan_bias*.pkl"

#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Republican_partisan_gini*.pkl" 
#python -u read_hp_results.py --e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Republican_partisan_gini*.pkl" 

#python -u read_hp_results.py --e 0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Democratic_partisan_gini*.pkl" 
#python -u read_hp_results.py --e 0.005,0.003,0.001,0.0005 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Democratic_partisan_gini*.pkl"

python -u read_hp_results.py --e 0.005,0.003,0.001,0.0005,0.00005,0.000009 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES12_Republican_safe_seats*.pkl" 
python -u read_hp_results.py --e 0.005,0.003,0.001,0.0005,0.00005,0.000009 --a 0.05 --fn "hp/biased_chains/NC/shortburst_PRES16_Republican_safe_seats*.pkl" 

