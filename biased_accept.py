import numpy as np
from settings import partytofavor, election_name, bias_for_second_party

# this is from the Duchin, Needham, Weighill paper
def increase_safe_seats(partition):
    parent = partition.parent
    DEMseats = len(
        [x for x in partition[election_name].percents(partytofavor) if x > 0.53]
    )
    DEMseatsparent = len(
        [x for x in parent[election_name].percents(partytofavor) if x > 0.53]
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
    
    if bias_for_second_party:
        delta = -delta
        
    # accept immediately if "bias" is not decreasing
    # else: accept with some probability, Metropolis style
    return np.random.random() < np.exp(beta*delta)

def increase_mean_median(partition):
    parent = partition.parent

    curr = get_elec_results(partition)
    prev = get_elec_results(parent)

    delta = curr.mean_median() - prev.mean_median()
    beta = 2 # this should change with the bias metric
    
    if bias_for_second_party:
        delta = -delta
        
    # accept immediately if "bias" is not decreasing
    # else: accept with some probability, Metropolis style
    return np.random.random() < np.exp(beta*delta)

def increase_partisan_bias(partition):
    parent = partition.parent

    curr = get_elec_results(partition)
    prev = get_elec_results(parent)

    delta = curr.partisan_bias() - prev.partisan_bias()
    beta = 2 # this should change with the bias metric
        
    # accept immediately if "bias" is not decreasing
    # else: accept with some probability, Metropolis style
    return np.random.random() < np.exp(beta*delta)


def increase_partisan_gini(partition):
    parent = partition.parent

    curr = get_elec_results(partition)
    prev = get_elec_results(parent)

    delta = curr.partisan_gini() - prev.partisan_gini()
    beta = 2 # this should change with the bias metric
        
    # accept immediately if "bias" is not decreasing
    # else: accept with some probability, Metropolis style
    return np.random.random() < np.exp(beta*delta)
