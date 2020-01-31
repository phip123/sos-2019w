from typing import Dict, Tuple, Callable

import networkx as nx
import numpy as np
import plotly.express as px

import somvisualization.distances.L2 as L2
from somvisualization.io.somlib import parse, WeightedVector


def calculate_qe(input_vectors, units, winner_mapping, xdim, ydim):
    qes = np.zeros((xdim, ydim), dtype=float)
    for i in range(xdim):
        for j in range(ydim):
            qe = 0
            for idx in winner_mapping['MAPPING']:
                winner = winner_mapping['MAPPING'][idx]
                idx = int(idx) - 1  # MAPPING starts with 1 but input_vectors with 0
                bmu = winner[0]
                if bmu[0] == i and bmu[1] == j:
                    input_vec = input_vectors['VECTORS'][idx]
                    for k in range(len(input_vec)):
                        dist = abs(input_vec[k] - units[(i, j)].weights[k])
                        qe += dist
            qes[i, j] = qe
    return qes


def calculate_shortest_distances(graph, units, winner_mapping, xdim, ydim):
    shortest_distances = np.zeros((xdim, ydim), dtype=float)

    for winner in winner_mapping['MAPPING'].values():
        bmu = winner[0]
        sbmu = winner[1]
        length = nx.dijkstra_path_length(graph, (bmu[0], bmu[1]), (sbmu[0], sbmu[1]), weight='weight')
        shortest_distances[bmu[0], bmu[1]] += length

    return shortest_distances


def build_graph(xdim: int, ydim: int, weighted_vectors: Dict[Tuple[int, int], WeightedVector],
                dist: Callable) -> nx.Graph:
    G = nx.Graph()
    for i in range(xdim):
        for j in range(ydim):
            vec = weighted_vectors[(i, j)]
            up_pos = (i, j - 1)
            left_pos = (i - 1, j)
            right_pos = (i + 1, j)
            down_pos = (i, j - 1)
            positions = [up_pos, left_pos, right_pos, down_pos]
            for pos in positions:
                if not (pos[0] < 0 or pos[0] >= xdim or pos[1] < 0 or pos[1] >= ydim):
                    G.add_edge((i, j), pos, weight=dist(vec.weights, weighted_vectors[pos].weights))
    return G


def visualize(map_info: Dict, winner_mapping: Dict, input_vectors: Dict,
              weighted_vectors: Dict[Tuple[int, int], WeightedVector],
              dist: Callable = L2.distance, color_palette: str = 'Viridis',
              title: str = 'Intrinsic Distance'):
    xdim = weighted_vectors['XDIM']
    ydim = weighted_vectors['YDIM']
    units = weighted_vectors['VECTORS']
    # Build the graph
    graph = build_graph(xdim, ydim, units, dist)

    # Create matrix (xdim,ydim) where each cell contains the shortest distance to the SBMU
    shortest_distances = calculate_shortest_distances(graph, units, winner_mapping, xdim, ydim)

    # Create matrix (xdim, ydim) where cell contains the qe of the corresponding unit
    qes = calculate_qe(input_vectors, units, winner_mapping, xdim, ydim)

    # Calculate intrinsic distance for each unit
    intrinsic_distances = shortest_distances + qes

    fig = px.imshow(intrinsic_distances.T, color_continuous_scale=color_palette, title=title, origin='lower')
    fig.update_layout(coloraxis_colorbar=dict(
        thickness=50,
        dtick=max(np.amax(intrinsic_distances) / 5, 1)
    ))
    fig.show()


def main():
    map_info = parse('soms/10Clusters-small.map')
    winner_mapping = parse('soms/10Clusters-small.dwm')
    input_vectors = parse('soms/10clusters.vec')
    weighted_vectors = parse('soms/10Clusters-small.wgt')
    visualize(
        map_info=map_info,
        winner_mapping=winner_mapping,
        input_vectors=input_vectors,
        weighted_vectors=weighted_vectors
    )


if __name__ == '__main__':
    main()
