import numpy as np
from settings import election_name, party_to_favor

def get_biased_accept(bias_measure):
    accept_dict = {
        'safe_seats' : increase_safe_seats,
        'efficiency_gap' : increase_efficiency_gap,
        'mean_median' : increase_mean_median,
        'partisan_bias' : increase_partisan_bias,
        'partisan_gini' : increase_partisan_gini
    }

    return accept_dict[bias_measure]

# this is from the Duchin, Needham, Weighill paper
def increase_safe_seats(partition):
    parent = partition.parent
    DEMseats = len(
        [x for x in partition[election_name].percents(party_to_favor) if x > 0.53]
    )
    DEMseatsparent = len(
        [x for x in parent[election_name].percents(party_to_favor) if x > 0.53]
    )
    alpha = np.exp(2*(DEMseats-DEMseatsparent))
    doaccept = (np.random.random() < alpha)
    return doaccept

def get_elec_results(x):
    # get ElectionResults for a map
    return x.updaters[election_name](x)

def increase_efficiency_gap(partition):
    parent = partition.parent

    curr = get_elec_results(partition)
    prev = get_elec_results(parent)

    ## change here if we are interested in different "bias" metric
    # https://gerrychain.readthedocs.io/en/latest/api.html#module-gerrychain.metrics
    delta = curr.efficiency_gap() - prev.efficiency_gap()
    beta = 300
        
    # accept immediately if "bias" is not decreasing
    # else: accept with some probability, Metropolis style
    return np.random.random() < np.exp(beta*delta)

def increase_mean_median(partition):
    parent = partition.parent

    curr = get_elec_results(partition)
    prev = get_elec_results(parent)

    delta = curr.mean_median() - prev.mean_median()
    beta = 300 # this should change with the bias metric
    
    # accept immediately if "bias" is not decreasing
    # else: accept with some probability, Metropolis style
    return np.random.random() < np.exp(beta*delta)

def increase_partisan_bias(partition):
    parent = partition.parent

    curr = get_elec_results(partition)
    prev = get_elec_results(parent)

    delta = curr.partisan_bias() - prev.partisan_bias()
    beta = 50 # this should change with the bias metric
        
    # accept immediately if "bias" is not decreasing
    # else: accept with some probability, Metropolis style
    return np.random.random() < np.exp(beta*delta)


def increase_partisan_gini(partition):
    parent = partition.parent

    curr = get_elec_results(partition)
    prev = get_elec_results(parent)

    delta = curr.partisan_gini() - prev.partisan_gini()
    beta = 300 # this should change with the bias metric
        
    # accept immediately if "bias" is not decreasing
    # else: accept with some probability, Metropolis style
    return np.random.random() < np.exp(beta*delta)
