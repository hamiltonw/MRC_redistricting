
import pickle
import matplotlib.pyplot as plt
from functools import partial
import pandas as pd

from gerrychain import (GeographicPartition, Graph, MarkovChain,
                        updaters, constraints, Election)
from gerrychain.proposals import recom
import geopandas as gpd

from biased_accept import increase_safe_seats, increase_efficiency_gap, get_elec_results
from settings import partytofavor, election_name

# read in the shapefile as a dataframe
pa_vtds = gpd.read_file("./data/PA/PA.shp")

# convert the dataframe to a gerrychain-viable object
graph = Graph.from_geodataframe(pa_vtds)

# this is more-or-less following the tutorial here: https://gerrychain.readthedocs.io/en/latest/user/recom.html
elections = [
    Election("SEN10", {"Democratic": "SEN10D", "Republican": "SEN10R"}),
    Election("SEN12", {"Democratic": "USS12D", "Republican": "USS12R"}),
    Election("SEN16", {"Democratic": "T16SEND", "Republican": "T16SENR"}),
    Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
    Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"})
]

# Population updater, for computing how close to equality the district
# populations are. "TOTPOP" is the population column from our shapefile.
my_updaters = {"population": updaters.Tally("TOTPOP", alias="population")}
# main difference here, name for the population column is different

# Election updaters, for computing election results using the vote totals
# from our shapefile.
election_updaters = {election.name: election for election in elections}
my_updaters.update(election_updaters)

initial_partition = GeographicPartition(graph, assignment="CD_2011", updaters=my_updaters)

# The ReCom proposal needs to know the ideal population for the districts so that
# we can improve speed by bailing early on unbalanced partitions.

ideal_population = sum(initial_partition["population"].values()) / len(initial_partition)

# We use functools.partial to bind the extra parameters (pop_col, pop_target, epsilon, node_repeats)
# of the recom proposal.
proposal = partial(recom,
                   pop_col="TOTPOP",
                   pop_target=ideal_population,
                   epsilon=0.02,
                   node_repeats=2
                  )

compactness_bound = constraints.UpperBound(
    lambda p: len(p["cut_edges"]),
    2*len(initial_partition["cut_edges"])
)

pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, 0.02)
# see also https://gerrychain.readthedocs.io/en/latest/api.html#module-gerrychain.constraints


num_steps = 3000

chain = MarkovChain(
    proposal=proposal,
    constraints=[
        pop_constraint,
        compactness_bound
    ],
    # accept=accept.always_accept,
    #accept = increase_safe_seats,
    accept = increase_efficiency_gap,
    initial_state=initial_partition,
    total_steps=num_steps
)

fname = './chains/'+partytofavor+'efficiency_gap_'+str(num_steps)+'.pkl'

with open(fname, 'rb') as f:
    x = pickle.load(f)

#read out the plans
all_partitions = [[xx[i] for i in range(len(graph))] for xx in x]
