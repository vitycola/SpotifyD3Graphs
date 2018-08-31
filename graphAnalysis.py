import networkx as nx
import json
from networkx.readwrite import json_graph
import community
import operator

def get_centralities(g):

    centralities_data = {'degree': [], 'closeness':[], 'betweeness':[], 'eigenvector':[], 'pagerank':[]}

    for comp in nx.connected_component_subgraphs(g):
        if len(comp) > 1:
            centralities_data['degree'].append(nx.degree_centrality(comp))
            centralities_data['closeness'].append(nx.closeness_centrality(comp))
            centralities_data['betweeness'].append(nx.betweenness_centrality(comp))
            centralities_data['eigenvector'].append(nx.eigenvector_centrality(comp))
            centralities_data['pagerank'].append(nx.pagerank(comp))

    return centralities_data


def centralities_integration_nodes(g, centralities_data):

    centralities_types = centralities_data.keys()
    for CT in centralities_types:
        for comp in centralities_data[CT]:
            for node_name in comp.keys():
                g.node[node_name][CT] = comp[node_name]
    return g


def centralities_measurements_comparison(centralities_data):
    centralities_types = centralities_data.keys()
    max_measurements1 = {'degree': [], 'closeness':[], 'betweeness':[], 'eigenvector':[], 'pagerank':[]}
    max_measurements2 = {'degree': [], 'closeness':[], 'betweeness':[], 'eigenvector':[], 'pagerank':[]}

    for CT in centralities_types:

        print('\t Maximum centrality ', str(CT),  'measurements of each vertex')

        for comp in centralities_data[CT]:
            max_measurements1[CT].append(max(comp.items(), key=operator.itemgetter(1)))
            max_measurements2[CT].append(max(comp.items(), key=operator.itemgetter(1))[0])

        print('\t', max_measurements1[CT])

    return



if __name__ == "__main__":


    path = "data/data.json"

    with open(path, 'r') as f:
        json_data = json.load(f)
        g = json_graph.node_link_graph(json_data, directed=False, multigraph = False)

        layout = nx.spring_layout(g)
        nx.draw_networkx_nodes(g, layout, node_size=100, node_color='blue', alpha=0.3)
        nx.draw_networkx_edges(g, layout)
        nx.draw_networkx_labels(g, layout, font_size=8, font_family='sans-serif')


        # Graph analysis with centralities measurements

        centralities_data = get_centralities(g)
        centralities_measurements_comparison(centralities_data)
        g = centralities_integration_nodes(g, centralities_data)

        # Clustering Coefficient
        print("\nCOEFICIENTE DE CLUSTERING")
        print('Clustering:', nx.average_clustering(g))


        # Community detection
        communities = community.best_partition(g)


        # Export graph to json

        g_json = json_graph.node_link_data(g)

        filename = 'data/graph_analyzed.json'
        with open(filename, 'w') as f:
            json.dump(g_json, f, indent=1)

