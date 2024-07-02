import numpy as np
import pickle
import os
import glob
import csv
from argparse import ArgumentParser

def test_hypothesis(w_vals, epsilon, alpha, verbose=True):
    m = w_vals.shape[0]
    k = w_vals.shape[1]
    if len(w_vals.shape) > 2:
        mn = w_vals.shape[2]
    else:
        mn = 1

    if verbose:
        print(m, 'trajectories,', k, 'steps')
        print('epsilon', epsilon, 'alpha', alpha)

    counts = np.sum(w_vals[:, 1:, :] < w_vals[:, 0, :].reshape(m, 1, mn), axis=1)
    rho_lower = np.sum(counts < epsilon*k, axis=0)
    rho_upper = np.sum(counts > (1-epsilon)*k, axis=0)

    # calculate p-value from Theorem 3.1
    r = rho_lower - m*np.sqrt(2*epsilon/alpha)
    p_lower = np.minimum(np.exp(-np.minimum((r**2)*np.sqrt(alpha/2/epsilon)/3/m, r/3)), 1) # clip at 1

    r = rho_upper - m*np.sqrt(2*epsilon/alpha)
    p_upper = np.minimum(np.exp(-np.minimum((r**2)*np.sqrt(alpha/2/epsilon)/3/m, r/3)), 1) # clip at 1

    if verbose:
        print('w0 in top e-fraction:', rho_upper, p_upper)
        print('w0 in bottom e-fraction:', rho_lower, p_lower)
        print()

    return (rho_upper, p_upper), (rho_lower, p_lower)

def main(args):
    eps = [float(x) for x in args.e.split(",")]
    alphas = [float(x) for x in args.a.split(",")]
    
    if os.path.isfile(args.fn):
        fns = [args.fn]
        csv_fn = args.fn[:-4]
    elif os.path.isdir(args.fn):
        fns = glob.glob(os.path.join(args.fn, "*.pkl"))
        csv_fn = args.fn + 'results'
    else:
        fns = glob.glob(args.fn)
        csv_fn = args.fn[:-4]

    print(fns)
    metric_names = ['efficiency gap', 'mean median', 'partisan bias', 'partisan gini', 'mean thirdian', 'safe seats']
    
    p_lower_count = {}
    p_upper_count = {}

    for ep in eps:
        for alpha in alphas:
            with open(f"{csv_fn}_{ep}_{alpha}.csv", 'w', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['map index']+  
                                ['rho upper'] + ['']*len(metric_names) + ['p-value upper'] + ['']*len(metric_names) + 
                                ['rho lower'] + ['']*len(metric_names) + ['p-value lower'] + ['']*(len(metric_names)-1)
                                )

                writer.writerow([''] + metric_names + [''] + metric_names + [''] + metric_names + [''] + metric_names)
                print(f"{csv_fn}_{ep}_{alpha}.csv")
                
                p_lower_count[(ep, alpha)] = 0
                p_upper_count[(ep, alpha)] = 0 

    for fn in fns:
        print()
        print(fn)
        with open(fn, 'rb') as f:
            (args_hp, map_idx, metric_names, all_metric_values, all_percents, res) = pickle.load(f)
            w_vals = np.array(all_metric_values)

        print(args_hp)
        print('index of map investigated', map_idx)
        print(w_vals.shape)
        print(metric_names)
        print(res['w0'])
#        print(np.array(res['counts']))
        
        
        for ep in eps:
            for alpha in alphas:
                (rho_upper, p_upper), (rho_lower, p_lower) = test_hypothesis(w_vals, ep, alpha)
                print(p_upper <= alpha, p_lower <= alpha)
                p_upper_count[(ep, alpha)] += p_upper <= alpha
                p_lower_count[(ep, alpha)] += p_lower <= alpha

                with open(f"{csv_fn}_{ep}_{alpha}.csv", 'a', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([map_idx] + list(rho_upper) + [''] + list(1*(p_upper <= alpha)) + ['']+ list(rho_lower) + [''] + list(1*(p_lower <= alpha)))
    
    for ep in eps:
        for alpha in alphas:
            with open(f"{csv_fn}_{ep}_{alpha}.csv", 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['total'] + ['']*(len(metric_names)+1) + list(p_upper_count[(ep, alpha)]) + ['']*(len(metric_names)+1) + ['']+ list(p_lower_count[(ep, alpha)])) 
    

if __name__ == "__main__":
    parser = ArgumentParser(description="run hypothesis test")
    parser.add_argument("--fn", type=str, default="hp/biased_chains/NC/shortburst_PRES16_Republican_mean_median*.pkl",
        help="filename")
    parser.add_argument("--a", type=str, default="0.009,0.05", help="alpha seperated by comma")
    parser.add_argument("--e", type=str, default="0.003,0.001", help="epsilon seperated by comma")
    args = parser.parse_args()

    print(args)
    main(args)
