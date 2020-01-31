from typing import Tuple, Dict

import numpy as np
import plotly.express as px

from somvisualization.io.somlib import parse


def dist(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0] + a[1] - b[1])


def visualize(map_info: Dict, winner_mapping: Dict,
                color_palette: str = 'Viridis', title: str = 'Topographic Error'):
    x_dim = int(map_info['XDIM'])
    y_dim = int(map_info['YDIM'])
    units = np.zeros((x_dim, y_dim), dtype=int)

    # Iterate over each input vector and count the instances where the SBMU is not adjacent to the BMU
    for winner in winner_mapping['MAPPING'].values():
        bmu = winner[0]
        sbmu = winner[1]
        bmu_pos = (bmu[0], bmu[1])
        sbmu_pos = (sbmu[0], sbmu[1])

        if dist(bmu_pos, sbmu_pos) > 1:
            units[bmu_pos[0], bmu_pos[1]] += 1

    fig = px.imshow(units.T, title=title, color_continuous_scale=color_palette,origin='lower')
    fig.update_layout(coloraxis_colorbar=dict(
        thickness=50,
        dtick=max(np.amax(units) / 5, 1)
    ))

    fig.show()


if __name__ == '__main__':
    map_info = parse('soms/10Clusters-large.map')
    winner_mapping = parse('soms/10Clusters-large.dwm')
    visualize(map_info=map_info, winner_mapping=winner_mapping)
