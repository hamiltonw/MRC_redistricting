import matplotlib.pyplot as plt
from settings import party_to_favor
from gerrychain import (GeographicPartition, Graph, MarkovChain,
                        updaters, constraints, Election)
from gerrychain.proposals import recom
import geopandas as gpd

def read_PA_data(path):

    # read in the shapefile as a dataframe
    pa_vtds = gpd.read_file(path)

    # convert the dataframe to a gerrychain-viable object
    graph = Graph.from_geodataframe(pa_vtds)
    return graph

def get_elections(party_to_favor, election_name):
    if party_to_favor == "Democratic":
        elections_dict = {
            "SEN10" : {"Democratic": "SEN10D", "Republican": "SEN10R"},
            "SEN12" : {"Democratic": "USS12D", "Republican": "USS12R"},
            "SEN16" : {"Democratic": "T16SEND", "Republican": "T16SENR"},
            "PRES12" : {"Democratic": "PRES12D", "Republican": "PRES12R"},
            "PRES16" : {"Democratic": "T16PRESD", "Republican": "T16PRESR"}
        }
    elif party_to_favor == "Republican":
        elections_dict = {
            "SEN10" : {"Republican": "SEN10R", "Democratic": "SEN10D"},
            "SEN12" : {"Republican": "USS12R", "Democratic": "USS12D"},
            "SEN16" : {"Republican": "T16SENR", "Democratic": "T16SEND"},
            "PRES12" : {"Republican": "PRES12R", "Democratic": "PRES12D"},
            "PRES16" : {"Republican": "T16PRESR", "Democratic": "T16PRESD"}
        } 
    else:
        raise Exception

    elections = [Election(election_name, elections_dict[election_name])]
    print([(e.name, e.parties) for e in elections])

    # Election updaters, for computing election results using the vote totals
    # from our shapefile.

    election_updaters = {election.name: election for election in elections}

    return election_updaters
    
def plot_bias_metrics(data, partisan_metric_values, all_safe_seats, all_party_seats, fname):

    fig = plt.figure(figsize=(15, 5))

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
    ax.plot(all_party_seats)
    ax.legend(['safe seats', 'seats won'])
    ax.set_xlabel('Steps on MCMC chain')
    ax.set_title('# of seats for ' + party_to_favor)

    plt.tight_layout()
    plt.savefig(fname+'.pdf', dpi=300, format='pdf')
    plt.show()