import pickle
#from settings import party_to_favor, election_name, bias_measure
from argparse import ArgumentParser
import utils
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
    elections =  ['PRES16', 'PRES12']
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
        cor_r = np.zeros((len(biased_metrics), len(compared_metrics)))
        cor_d = np.zeros_like(cor_r)
        cor_n = np.zeros_like(cor_d)

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
            
                print(np.corrcoef(ri, rj))
                cor_r[i, j] = np.corrcoef(ri, rj)[0,1]
                cor_d[i, j] = np.corrcoef(di, dj)[0,1]
                cor_n[i, j] = np.corrcoef(ni, nj)[0,1]

        for label, cor in zip(['Republican', 'Democratic', 'Unbiased'], [cor_r, cor_d, cor_n]):
    
            fig, ax = plt.subplots()
            im = ax.imshow(cor)

            ax.set_xticks(np.arange(len(compared_metrics)), labels=compared_metrics)
            ax.set_yticks(np.arange(len(biased_metrics)), labels=biased_metrics)

            plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

            for i in range(len(biased_metrics)):
                for j in range(len(compared_metrics)):
                    text = ax.text(j, i, np.around(cor[i, j], 2),
                       ha="center", va="center", color="w")

            ax.set_title(election + ', ' +label, fontsize=16)
            ax.set_xlabel('compared')
            ax.set_ylabel('biased')

            hist_f = f"biased_chains/{state}/" + election + '/'
            os.makedirs(hist_f,  exist_ok=True)
           
            plot_f = hist_f + label+ '-correlation.pdf'
            plt.savefig(plot_f, dpi=300)
            plt.close()
            print(plot_f)
    print('done!')  

if __name__ == "__main__":
    parser = ArgumentParser(description="make heatmaps of metrics")
    parser.add_argument("--n", type=int, default=100,
        help="plot every n numbers")
    parser.add_argument("--sb", type=int, default=0, help="shortburst")
    parser.add_argument("--state", type=str, default="PA", help="state")
    args = parser.parse_args()

    print(args)

    run(args)

