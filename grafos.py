import networkx as nx
import json
from networkx.readwrite import json_graph
#import community

import matplotlib.pyplot as plt



def get_centralities(g):

    centralities_data = {'degree': [], 'closeness':[], 'betweeness':[], 'pagerank':[]}

    for comp in nx.connected_component_subgraphs(g):
        if len(comp) > 1:
            centralities_data['degree'].append(nx.degree_centrality(comp))
            centralities_data['closeness'].append(nx.closeness_centrality(comp))
            centralities_data['betweeness'].append(nx.betweenness_centrality(comp))
            centralities_data['pagerank'].append(nx.pagerank(comp))

    return centralities_data


def add_centralities_tonodes(g, centralities_data):

    centralities_types = centralities_data.keys()
    for cent_type in centralities_types:
        for conex_comp in centralities_data[cent_type]:
            for node_name in conex_comp.keys():
                g.node[node_name][cent_type] = conex_comp[node_name]
    return g


def add_community_tonodes(g, communities):

    for node_name in communities.keys():
        g.node[node_name]['community'] = communities[node_name]
    return g



if __name__ == "__main__":


    path = "data/data.json"

    with open(path, 'r') as f:
        json_data = json.load(f)
        g = json_graph.node_link_graph(json_data, directed=False, multigraph = False)

        layout = nx.spring_layout(g)
        nx.draw_networkx_nodes(g, layout, node_size=100, node_color='blue', alpha=0.3)
        nx.draw_networkx_edges(g, layout)
        nx.draw_networkx_labels(g, layout, font_size=8, font_family='sans-serif')
        plt.show()

        # 2 Muestra todos los artistas
        print("ARTISTAS")
        for node, atts in g.nodes(data=True):
            if 'type' in atts and atts['type'] == 'artist':
                print(node)
                print(atts["name"])

        # # Numero de canciones por disco
        # print("\nCANCIONES POR DISCO")
        # for node, atts in g.nodes(data=True):
        #     if 'type' in atts and atts['type'] == 'album':
        #         print(node, ':', g.degree(node)-1)

        # Coeficiente de clustering
        print("\nCOEFICIENTE DE CLUSTERING")
        print('Clustering:', nx.average_clustering(g))



        centralities_data = get_centralities(g)
        g = add_centralities_tonodes(g, centralities_data)


        # # Community detection
        # communities = community.best_partition(g)
        # artist_subgraph = add_community_tonodes(g, communities)


        # Export graph to json

        g_json = json_graph.node_link_data(g)

        filename = 'data/graph_analyzed.json'
        with open(filename, 'w') as f:
            json.dump(g_json, f, indent=1)

