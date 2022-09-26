
import pickle
from functools import partial
import pandas as pd

from gerrychain import (GeographicPartition, Graph, MarkovChain,
                        updaters, constraints, Election)
from gerrychain.proposals import recom

from biased_accept import get_biased_accept, get_elec_results
from settings import party_to_favor, election_name, bias_measure
import utils

graph = utils.read_PA_data("./data/PA/PA.shp")

# Population updater, for computing how close to equality the district
# populations are. "TOTPOP" is the population column from our shapefile.
my_updaters = {"population": updaters.Tally("TOTPOP", alias="population")}
# main difference here, name for the population column is different
my_updaters.update(utils.get_elections(party_to_favor, election_name))

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


num_steps = 100 

chain = MarkovChain(
    proposal=proposal,
    constraints=[
        pop_constraint,
        compactness_bound
    ],
    # accept=accept.always_accept,
    accept = get_biased_accept(bias_measure),
    initial_state=initial_partition,
    total_steps=num_steps
)

all_partitions = [] # keep track of the actual partitions
all_percents = [] # keep track of the democratic percentages
all_safe_seats = []
partisan_metric_values = [] # keep track of the partisan metrics
all_assignments = [] # something pickle-able
all_party_seats = []

#for partition in chain.with_progress_bar():
for idx, partition in enumerate(chain):

    all_partitions.append(partition)

    all_assignments.append(partition.assignment)

    elec_result = get_elec_results(partition)
    partisan_metric_values.append([
        elec_result.efficiency_gap(), 
        elec_result.mean_median(), 
        elec_result.partisan_bias(),
        elec_result.partisan_gini(),
        elec_result.mean_thirdian()
        ])

    safe_seats = len([x for x in partition[election_name].percents(party_to_favor) if x > 0.53])
    all_safe_seats.append(safe_seats)

    all_percents.append(sorted(partition[election_name].percents(party_to_favor)))

    all_party_seats.append(elec_result.seats(party_to_favor))

fname = 'chains/'+'_'.join([election_name, party_to_favor, bias_measure, str(num_steps)])

with open(fname +'.pkl', 'wb') as f:
    pickle.dump(all_assignments, f)

print('assignments saved to', fname)

data = pd.DataFrame(all_percents) #convert to a pd dataframe

utils.plot_bias_metrics(data, partisan_metric_values, all_safe_seats, all_party_seats, fname)

