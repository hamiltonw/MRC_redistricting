import pickle
from functools import partial
import geopandas as gpd
import matplotlib.pyplot as plt 
from gerrychain import (GeographicPartition, Graph, MarkovChain,
                        updaters, constraints, Election, accept)
from gerrychain.proposals import recom, propose_random_flip
import hypothesis_test as hp
from settings import party_to_favor, election_name, bias_measure
import utils


pa_vtds = gpd.read_file("./data/PA/PA.shp")
graph = Graph.from_geodataframe(pa_vtds)
del pa_vtds
my_updaters = {"population": updaters.Tally("TOTPOP", alias="population")}
my_updaters.update(utils.get_elections(party_to_favor, election_name))
initial_partition = GeographicPartition(graph, assignment="CD_2011", updaters=my_updaters)
ideal_population = sum(initial_partition["population"].values()) / len(initial_partition)
pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, 0.02)
compactness_bound = constraints.UpperBound(
    lambda p: len(p["cut_edges"]),
    2*len(initial_partition["cut_edges"])
)

# load biased chain
num_steps = 3000
fname = 'chains/'+'_'.join([election_name, party_to_favor, bias_measure, str(num_steps)])
with open(fname+'.pkl', 'rb') as f:
    all_assignments = pickle.load(f)

#identify a chain of interest
idx = len(all_assignments)-1
# import random
# idx = random.randrange(len(all_assignments))
test_partition = GeographicPartition(graph, all_assignments[idx], updaters=my_updaters)

plt.figure(figsize=(10,10))
ax = plt.subplot(2,1,1)
plt.axis('off')
initial_partition.plot(cmap="tab20", ax=ax)
plt.title('actual plan')

ax = plt.subplot(2,1,2)
test_partition.plot(cmap="tab20", ax=ax)
plt.axis('off')
plt.title('plan to be tested: '+str(idx)+'th in biased chain' )
plt.xlabel(fname)
#plt.show()



# run the hypothesis test

k = 10000
epsilon = 0.1

#set up the new chain
hypo_chain = MarkovChain(
    proposal=propose_random_flip,
    constraints = [pop_constraint, compactness_bound],
    accept = accept.always_accept,
    initial_state=test_partition,
    total_steps=k+1
)

#run the hypothesis test v1
res = hp.test_hypothesis(
    hypo_chain,
    test_partition,
    epsilon,
    k,
    hp.partisan_bias,
    election_name
    )

print(f"tested map using label function partisan bias is epsilon-outlier: {res[0]}")
print(res[1])
# print(res[-1])

# random parameters
m = 100
alpha = 0.1
r = 0.1

#run the hypothesis test v2
res = hp.test_hypothesis_v2(
    hypo_chain,
    test_partition,
    epsilon,
    m,
    alpha,
    r,
    k,
    hp.partisan_bias,
    election_name
    )


