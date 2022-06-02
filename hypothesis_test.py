# for gerrychain

import matplotlib.pyplot as plt
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from functools import partial
import pandas as pd
import geopandas as gpd

from tqdm import tqdm

# for fancy map plotting
import folium
import mapclassify

"""
wrappers for some of the Gerrychain functions
"""

def partisan_bias(p_election):
    """
    p should be the results of an election, say like
    p = partition["PRES16"], etc.
    """
    return p_election.partisan_bias()


def partisan_gini(p_election):
    """
    p should be the results of an election, say like
    p = partition["PRES16"], etc.
    """
    return p_election.partisan_gini()


def mean_thirdian(p_election):
    """
    p should be the results of an election, say like
    p = partition["PRES16"], etc.
    """
    return p_election.mean_thirdian()


def efficiency_gap(p_election):
    """
    p should be the results of an election, say like
    p = partition["PRES16"], etc.
    """
    return p_election.efficiency_gap()

def mean_median(p_election):
    """
    p should be the results of an election, say like
    p = partition["PRES16"], etc.
    """
    return p_election.mean_median()


"""
main function to run the hypothesis test from "Assessing significance in a Markov chain without mixing"
"""
def test_hypothesis(markov_chain,p,epsilon,k,w,election_name):
    """
    :param p: partition of interest
    :param epsilon: significance parameter
    :param k: number of steps
    :param w: function to evaluate plans in the trajectory on and evaluate outlierness
    :param markov_chain: the markov chain to use
    :param election_name: name of the election to use in computing w(plans)
    """

    #(1) Beginning from the districting being evaluated,

    markov_chain.initial_state = p
    markov_chain.total_steps = k + 1

    #(2) Make a sequence of random changes to the districting, while preserving some set of constraints imposed on the districtings.

    all_results = [None for i in range(k+1)] #set some space for each plan

    for idx, partition in enumerate(markov_chain): #run the chain 
        all_results[idx] = partition

    #(3) Evaluate the partisan properties of each districting encountered (e.g., by simulating elections using past voting data).

    w_vals = [w(p[election_name]) for p in all_results]

    #(4) Call the original districting “carefully crafted” or “gerrymandered” if the overwhelming majority of districtings produced by making small random changes are less partisan than the original districting.

    counts = sum(w_vals[1:]> w_vals[0])

    if counts <= epsilon*(k+1):
        return True 
    else:
        return False
