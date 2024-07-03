import pickle
#from settings import party_to_favor, election_name, bias_measure
import utils
from argparse import ArgumentParser
import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_metrics_file(fname):
    with open(fname, 'rb') as f:
            partisan_metric_values, all_safe_seats, all_percents, all_party_seats, races = pickle.load(f)
    metric_values = np.array(partisan_metric_values)
    metric_values = np.hstack((metric_values, np.array(all_safe_seats).reshape(-1,1)))
    
    print(metric_values.shape)
    return metric_values

def run(args):

    elections = ['PRES16', 'PRES12']
    biased_metrics = ['efficiency_gap', 'mean_median', 'partisan_bias', 'partisan_gini',  'safe_seats']
    compared_metrics = ['efficiency_gap', 'mean_median', 'partisan_bias', 'partisan_gini',
        'mean_thirdian', 'safe_seats'] 
    n = args.n
    sb = args.sb
    state = args.state
    folder = f"biased_chains/{state}"
    ufolder = f"unbiased_chains/{state}"

    for election in elections:
        print(election)
        fig, ax = plt.subplots(len(compared_metrics), len(biased_metrics), figsize=(12, 8))

        for i, metric1 in enumerate(biased_metrics):
            if sb:
                Rep = glob.glob(os.path.join(folder, "shortburst_"+election+ "_Republican_"+metric1+"_10000*-metrics.pkl"))
                Dem = glob.glob(os.path.join(folder, "shortburst_"+election+ "_Democratic_"+metric1+"_10000*-Republican-metrics.pkl"))
                Neutral = glob.glob(os.path.join(ufolder, "unbiased_"+election+"_50000-metrics.pkl"))
                Rep = [r for r in Rep if len(r.split('-'))==2]
            else:
                Rep = glob.glob(os.path.join(folder, election+ "_Republican_"+metric1+"_50000*-metrics.pkl"))
                Dem = glob.glob(os.path.join(folder, election+ "_Democratic_"+metric1+"_50000*-Republican-metrics.pkl"))
                Neutral = glob.glob(os.path.join(ufolder, "unbiased_"+election+"_50000-metrics.pkl"))
                Rep = [r for r in Rep if len(r.split('-'))==2]

            assert len(Rep) == 1
            assert len(Dem) == 1
            assert len(Neutral) == 1
            print(Rep, Dem, Neutral)
        
            rep_values = load_metrics_file(Rep[0])
            dem_values = load_metrics_file(Dem[0])
            neu_values = load_metrics_file(Neutral[0])
        
            if metric1 != 'safe_seats':
                ri = rep_values[::n, i]
                di = dem_values[::n, i]
                ni = neu_values[::n, i]
            else:
                ri = rep_values[::n, -1]
                di = dem_values[::n, -1]
                ni = neu_values[::n, -1]

            for j, metric2 in enumerate(compared_metrics):
                rj = rep_values[::n, j]
                dj = dem_values[::n, j]
                nj = neu_values[::n, j]
            
                kwargs = {'alpha': 0.1}
            
                if metric1 != metric2:
                    ax[j, i].scatter(ni, nj, label='Unbiased (metrics calculated wrt Rep)', color='k', **kwargs)
                    ax[j, i].scatter(ri, rj, label='Republican', color='r', **kwargs)
                    ax[j, i].scatter(di, dj, label='Democratic (metrics calculated wrt Rep)', color='b', **kwargs)

                    ax[j, i].set_ylabel(metric2, fontsize=8)
                else:
                    ax[j, i].hist(ni, label='Unbiased (metrics calculated wrt Rep)', color='k', bins=50, **kwargs)
                    ax[j, i].hist(ri, label='Republican', color='r', bins=50,  **kwargs)
                    ax[j, i].hist(di, label='Democratic (metrics calculated wrt Rep)', color='b', bins=50, **kwargs)
            
                ax[j, i].set_xlabel(metric1, fontsize=8)
                ax[j, i].tick_params(axis='both', which='major', labelsize=6)
                ax[j, i].tick_params(axis='both', which='minor', labelsize=6)

        plt.suptitle(election+'. chains are biased for metric on the x-axis', fontsize=16)
        plt.tight_layout()

        hist_f = f"biased_chains/{state}/" + election + '/'
        os.makedirs(hist_f,  exist_ok=True)
           
        plot_f = hist_f + 'scatter.pdf'
        plt.savefig(plot_f, dpi=300)
        plt.close()
        print(plot_f)
    print('done!') 

if __name__ == "__main__":
    parser = ArgumentParser(description="make scatter plots of metrics")
    parser.add_argument("--n", type=int, default=100,
        help="plot every n numbers")
    parser.add_argument("--sb", type=int, default=0, help="shortburst")
    parser.add_argument("--state", type=str, default="PA", help="state")
    args = parser.parse_args()

    print(args)

    run(args)
