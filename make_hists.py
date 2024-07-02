from argparse import ArgumentParser
import pickle
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

def main(args):
    elections = ['PRES16', 'PRES12']
    biased_metrics = ['efficiency_gap', 'mean_median', 'partisan_bias', 'partisan_gini',  'safe_seats']
    compared_metrics = ['efficiency_gap', 'mean_median', 'partisan_bias', 'partisan_gini',
            'mean_thirdian', 'safe_seats'] 

    n = args.n
    party = args.party
    state = args.state
    folder = f"biased_chains/{state}"
    ufolder = f"unbiased_chains/{state}"
    sb = args.sb

    for election in elections:
        print(election)

        for i, metric1 in enumerate(biased_metrics):
            if sb:
                if party == 'Rep':
                    Rep = glob.glob(os.path.join(folder, "shortburst_"+election+ "_Republican_"+metric1+"_10000*-metrics.pkl"))
                    Dem = glob.glob(os.path.join(folder, "shortburst_"+election+ "_Democratic_"+metric1+"_10000*-Republican-metrics.pkl"))
                    Neutral = glob.glob(os.path.join(ufolder, "unbiased_"+election+"_50000-metrics.pkl"))
                    Rep = [r for r in Rep if len(r.split('-'))==2]
                else:
                    Rep = glob.glob(os.path.join(folder, "shortburst_"+election+ "_Republican_"+metric1+"_10000*-Democratic-metrics.pkl"))
                    Dem = glob.glob(os.path.join(folder, "shortburst_"+election+ "_Democratic_"+metric1+"_10000*-metrics.pkl"))
                    Neutral = glob.glob(os.path.join(ufolder, "unbiased_"+election+"_50000-Democratic-metrics.pkl"))
                    Dem = [d for d in Dem if len(d.split('-'))==2]
            else:
                if party == 'Rep':
                    Rep = glob.glob(os.path.join(folder, election+ "_Republican_"+metric1+"_50000*-metrics.pkl"))
                    Dem = glob.glob(os.path.join(folder, election+ "_Democratic_"+metric1+"_50000*-Republican-metrics.pkl"))
                    Neutral = glob.glob(os.path.join(ufolder, "unbiased_"+election+"_50000-metrics.pkl"))
                    Rep = [r for r in Rep if len(r.split('-'))==2]
                else:
                    Rep = glob.glob(os.path.join(folder, election+ "_Republican_"+metric1+"_50000*-Democratic-metrics.pkl"))
                    Dem = glob.glob(os.path.join(folder, election+ "_Democratic_"+metric1+"_50000*-metrics.pkl"))
                    Neutral = glob.glob(os.path.join(ufolder, "unbiased_"+election+"_50000-Democratic-metrics.pkl"))
                    Dem = [d for d in Dem if len(d.split('-'))==2]

            assert len(Rep) == 1
            assert len(Dem) == 1
            assert len(Neutral) == 1
            print(Rep, Dem, Neutral)

            rep_values = load_metrics_file(Rep[0])
            dem_values = load_metrics_file(Dem[0])
            neu_values = load_metrics_file(Neutral[0])

            for j, metric2 in enumerate(compared_metrics):
                fig, ax = plt.subplots(1, figsize=(10, 8))
                kwargs = {'alpha': 0.3}
                r = rep_values[::n, j]
                d = dem_values[::n, j]
                ne = neu_values[::n, j]
                min_v = min(r.min(), d.min(), ne.min())
                max_v = max(r.max(), d.max(), ne.max())
                print(min_v, max_v)

                if metric2 in ['efficiency_gap', 'mean_median', 'mean_thirdian', 'partisan_gini']:
                    kwargs.update({'bins': 200, 'range':(min_v, max_v)})
                elif metric2 in ['partisan_bias', 'safe_seats']:
                    kwargs.update({'range': (min_v, max_v), 'bins':20})

                ax.hist(rep_values[::n, j], label='Republican', color='r', **kwargs)
                ax.hist(dem_values[::n, j], label='Democratic (metrics calculated wrt '+party+')', color='b', **kwargs)
                ax.hist(neu_values[::n, j], label='Unbiased (metrics calculated wrt '+party+')', color='k', **kwargs)

                ax.axvline(rep_values[-1, j], color='r', alpha=0.5, ls='-.')
                ax.axvline(dem_values[-1, j], color='b', alpha=0.5, ls='-.')
                ax.axvline(neu_values[-1, j], color='k', alpha=0.5, ls='-.')

                if metric1==metric2:
                    print(np.argmax(rep_values[:, j]), np.max(rep_values[:, j]))
                    print(np.argmax(dem_values[:, j]), np.max(dem_values[:, j]))
                    print(np.argmax(neu_values[:, j]), np.max(neu_values[:, j]))

                ax.axvline(neu_values[0, j], label=f'{state} CD', color='k', alpha=1)
                plt.title(election +', biased for ' + metric1 +'. comparing '+ metric2, fontsize=16)
                plt.legend()
                plt.tight_layout()

                hist_f = os.path.join(folder, election, metric1)
                os.makedirs(hist_f,  exist_ok=True)
                
                if sb:
                    if party == 'Dem':
                        plot_f = os.path.join(hist_f, 'shortburst-'+ metric2+'-Dem.pdf')
                    else:
                        plot_f = os.path.join(hist_f, 'shortburst-'+ metric2+'.pdf')
                else:
                    if party == 'Dem':
                        plot_f = os.path.join(hist_f, metric2+'-Dem.pdf')
                    else:
                        plot_f = os.path.join(hist_f, metric2+'.pdf')
                
                plt.savefig(plot_f, dpi=300)
                plt.close()
                print(plot_f)
    print('done!')    



if __name__ == "__main__":
    parser = ArgumentParser(description="make histograms of metrics")
    parser.add_argument("--party", type=str, default="Dem", 
        help="party")
    parser.add_argument("--n", type=int, default=1, 
        help="plot every n numbers")
    parser.add_argument("--sb", type=int, default=0, help="shortburst")
    parser.add_argument("--state", type=str, default="PA", help="state")
    args = parser.parse_args()
    
    print(args)
    
    main(args)
