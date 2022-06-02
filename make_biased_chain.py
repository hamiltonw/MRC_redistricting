
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

all_partitions = [] # keep track of the actual partitions
all_percents = [] # keep track of the democratic percentages
all_safe_seats = []
partisan_metric_values = [] # keep track of the partisan metrics
all_assignments = [] # something pickle-able
all_party_seats = []

#for partition in chain.with_progress_bar():
for idx, partition in enumerate(chain):
    if idx % 50 == 0:
        print('.', end='')
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

    safe_seats = len([x for x in partition[election_name].percents(partytofavor) if x > 0.53])
    all_safe_seats.append(safe_seats)

    all_percents.append(sorted(partition[election_name].percents(partytofavor)))

    all_party_seats.append(elec_result.seats(partytofavor))

fname = 'chains/'+partytofavor+'efficiency_gap_'+str(num_steps)
#fname = 'chains/'+partytofavor+'safe_seats_'+str(num_steps)

with open(fname +'.pkl', 'wb') as f:
    pickle.dump(all_assignments, f)

print('assignments saved to', fname)

data = pd.DataFrame(all_percents) #convert to a pd dataframe

fig = plt.figure(figsize=(5, 5))
plt.hist(all_party_seats, bins=range(0, 18))
plt.tight_layout()
plt.savefig(fname+'_hist'+'.pdf', dpi=300, format='pdf')
plt.show()

fig = plt.figure(figsize=(12, 4))

ax = fig.add_subplot(1,3,1)
# Draw 50% line
ax.axhline(0.5, color="#cccccc")
# Draw boxplot
data.boxplot(ax=ax, positions=range(len(data.columns)))
# Draw initial plan's Democratic vote %s (.iloc[0] gives the first row)
plt.plot(data.iloc[0], "ro")
# Annotate
ax.set_title("Comparing the plan to an ensemble")
ax.set_ylabel("Democratic vote %")
ax.set_xlabel("Sorted districts")
ax.set_ylim(0, 1)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])

ax = fig.add_subplot(1,3,2)
ax.plot(partisan_metric_values)
ax.set_title('Partisan metric values')
ax.set_xlabel('Steps on MCMC chain')
ax.legend(['efficiency gap', 'mean median', 'partisan bias', 'partisan gini', 'mean thirdian'])

ax = fig.add_subplot(1,3,3)
ax.plot(all_safe_seats)
ax.set_xlabel('Steps on MCMC chain')
ax.set_title('Safe seats for' + partytofavor)

plt.tight_layout()
plt.savefig(fname+'.pdf', dpi=300, format='pdf')
plt.show()