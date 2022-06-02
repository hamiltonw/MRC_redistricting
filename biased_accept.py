import numpy as np

election_name = "PRES16"

partytofavor = "Republican"
bias_for_second_party = True

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

