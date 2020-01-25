from typing import Tuple, Dict
import numpy as np
from bokeh.io import show
from bokeh.plotting import figure

from somvisualization.io.somlib import parse
from typing import Tuple, Dict

import numpy as np
from bokeh.io import show
from bokeh.plotting import figure

from somvisualization.io.somlib import parse


def visualize(map_info: Dict, winner_mapping: Dict):
    x_dim = int(map_info['XDIM'])
    y_dim = int(map_info['YDIM'])
    units = np.zeros((x_dim, y_dim), dtype=int)
    x = []
    y = []
    for winner in winner_mapping['MAPPING'].values():
        bmu = winner[0]
        sbmu = winner[1]
        bmu_pos = (bmu[0], bmu[1])
        sbmu_pos = (sbmu[0], sbmu[1])

        if dist(bmu_pos, sbmu_pos) > 1:
            x.append(bmu_pos[0])
            y.append(bmu_pos[1])
            units[bmu_pos[0], bmu_pos[1]] += 1

    H, xe, ye = np.histogram2d(x, y, bins=100)

    # produce an image of the 2d histogram
    p = figure(x_range=(0, x_dim), y_range=(0, y_dim), title='Image', match_aspect=True)
    p.image(image=[units], x=0, y=0, dw=x_dim, dh=y_dim, palette="Spectral11")

    show(p)


def dist(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0] + a[1] - b[1])


if __name__ == '__main__':
    map_info = parse('10Clusters-large.map')
    winner_mapping = parse('10Clusters-large.dwm')
    visualize(map_info=map_info, winner_mapping=winner_mapping)
