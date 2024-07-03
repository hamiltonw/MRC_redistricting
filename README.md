# MRC Redistricting project

## Structure
  1. Making unbiased and biased chains
     - `make_unbiased_chains.sh` runs `make_unbiased_chain.py`
     - `make_hill_chains.sh` runs `make_hill_chains.py`
     - `make_shorburst_chains.sh` runs `make_shortburst_chain.py`
  3. For a given state, calcualte metrics and generate figures for all chains
     - `calculate_metrics.sh` runs `calculate_metrics.py`, `make_hists.py`, `make_heats.py`, `make_scats.py`
  5. Run multiple trajectories for hypothesis test
     - `run_hp_from_scratch.sh` runs `run_hp_from_scratch.py`
  7. Read results from multiple trajectories and perform hypothesis test
     - `read_hp_results.sh` runs `read_hp_results.py`

## Common parameters
| Parameter             | Explanation | Examples |
| :---------------- | :------ | :---- |
| `state`        |   State name | NC, PA, etc [^1]  |
| `election`          |   Election name   | PRES16, PRES12, SEN10, etc [^1] |
| `n` | Number of steps in MCMC chain | 50000, 10000|
| `bias`    |  Bias metric   | mean_median, efficiency_gap, partisan_bias, partisan_gini, safe_seats |
| `party` | Party to favor | Republican or Democratic |
| `diversity` | Collect diversity statistics [^2]  | 0 or 1 |

#### Notes on `sb` and `n`:
There was a slight abuse of notation with `sb` and `n`.
- `sb` in `make_shortburst_chain.py` refers to the number of steps in the inner loop (default: 5). `sb` in `calculate_metrics.sh` just asks whether we're plotting shortburst chains or not for filename purposes. That code can probably be updated to remove the parameter and just run on all chains.
- When `n` is asked for in `calculate_metrics.sh`, it means only one in every `n` numbers will be used to generate the plots for readability.  
 
### Hypothesis test parameters
Shows up in `run_hp_from_scratch.py` and `read_hp_results.py`. 

| Parameter             | Explanation | Examples |
| :---------------- | :------ | :---- |
| `e` | Epsilon for hypothesis test | 0.0005 |
| `a` | Alpha for hypothesis test | 0.05 |
| `m` | Number of trajectories | 32 |
| `k` | Number of steps in MCMC chain | 100000 |
| `proposal` | MCMC chain generation method | recom (reversible), random (flipnode), chunk (chunk flip) [^3]|
| `map` | Which maps to investigate | random (randomly select from chain), max (map with max value), min |
| `fn` | File name | See below |

#### Notes on `run_hp_from_scratch.py`:
  - Where do we control parameter 100, i.e. how many maps to sample from a given chain? In the header of `run_hp_from_scratch.sh`, there's a slurm parameter `#SBATCH --array=1-100\%50`. This means run 100 of the same script in parallel but no more than 50 at a time[^4].
- `fn` should be the path to where the (un)biased chain is. For example, `biased_chains/NC/shortburst_PRES16_Republican_partisan_gini_10000_1719440281.pkl` or `unbiased_chains/NC/unbiased_PRES16_50000.pkl`.
  
#### Notes on `read_hp_results.py`:
  - Note that `e` and `a` can take in multiple values separated by comma. For example, `--e 0.015,0.01,0.005,0.003,0.001,0.0005 --a 0.05`.
  - `fn` should be the filename for trajectories from `run_hp_from_scratch.py`. It can be a single pkl file, regex that matches multiple files, or a folder name. For example, `*` in `hp/biased_chains/NC/shortburst_PRES12_Republican_mean_median*.pkl` is a wildcard and can take any value. This should match 100 filenames.
  
[^1]: See `get_elections` function in `utils.py` for options.
[^2]: https://gerrychain.readthedocs.io/en/latest/api/#gerrychain.meta.diversity.collect_diversity_stats
[^3]: https://gerrychain.readthedocs.io/en/latest/api/#module-gerrychain.proposals
[^4]: https://slurm.schedmd.com/job_array.html


<!--Goals:
1. Given a biased plan, find nearest non-biased plan.
2. Quantify what we mean by biased.
3. Explore the topography of the space of partitions (?).
4. Identify ``contentious'' precincts in a biased plan.

To run the notebooks:
1. Download the data from https://github.com/mggg-states/PA-shapefiles (PA.zip)
2. Download the empty notebook, or the zipped notebook
3. Run the notebook!-->


