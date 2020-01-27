from dataclasses import dataclass
from typing import Dict, IO, Optional, List


def parse_map(file: IO) -> Dict:
    properties = filter(lambda l: l.startswith('$'), file.readlines())
    properties = map(lambda l: l.replace('\n', ''), properties)
    properties = map(lambda l: (l[1:].split(' ')[0], l.split(' ')[1]), properties)
    return dict(properties)


def parse_winner_mapping(file: IO) -> Dict:
    lines = file.readlines()
    lines = list(map(lambda l: l.replace('\n', ''), lines))
    header = filter(lambda l: l.startswith('$'), lines)
    header = dict(map(lambda l: (l[1:].split(' ')[0], l.split(' ')[1]), header))
    mapping = {}

    mappings = list(filter(lambda l: not l.startswith('$'), lines))
    mappings = [(mappings[i], mappings[i + 1]) for i in range(0, len(mappings) - 1, 2)]
    for vec, winners in mappings:
        matchings = []
        winner_info = winners.split(' ')
        for i in range(0, len(winner_info) - 1, 3):
            x = int(winner_info[i])
            y = int(winner_info[i + 1])
            distance = float(winner_info[i + 2])
            matchings.append((x, y, distance))
        mapping[vec] = matchings
    header['MAPPING'] = mapping
    return header


def parse_input_vectors(file: IO) -> Dict:
    lines = file.readlines()
    lines = list(map(lambda l: l.replace('\n', ''), lines))
    header = filter(lambda l: l.startswith('$'), lines)
    header = dict(map(lambda l: (l[1:].split(' ')[0], l.split(' ')[1]), header))
    header['VEC_DIM'] = int(header['VEC_DIM'])
    header['XDIM'] = int(header['XDIM'])
    header['YDIM'] = int(header['YDIM'])
    vec_dim = header['VEC_DIM']
    vectors = filter(lambda l: not l.startswith('$'), lines)
    vectors = map(lambda l: l.split(' '), vectors)
    vectors = map(lambda l: l[:vec_dim], vectors)
    vectors = map(lambda l: list(map(lambda v: float(v), l)), vectors)
    header['VECTORS'] = list(vectors)
    return header


@dataclass
class WeightedVector:
    weights: List[float]
    x: int
    y: int
    z: int


def parse_vector(split: List[str], vec_dim: int) -> WeightedVector:
    weights = [float(x) for x in split[:vec_dim]]
    coords = split[vec_dim].split('_')
    coords = coords[len(coords) - 1].lstrip('(').rstrip(')').split('/')
    x = int(coords[0])
    y = int(coords[1])
    z = int(coords[2])
    return WeightedVector(weights, x, y, z)


def parse_weighted_vectors(file: IO):
    lines = file.readlines()
    lines = list(map(lambda l: l.replace('\n', ''), lines))
    header = filter(lambda l: l.startswith('$'), lines)
    header = dict(map(lambda l: (l[1:].split(' ')[0], l.split(' ')[1]), header))
    header['VEC_DIM'] = int(header['VEC_DIM'])
    header['XDIM'] = int(header['XDIM'])
    header['YDIM'] = int(header['YDIM'])
    header['ZDIM'] = int(header['ZDIM'])
    vec_dim = header['VEC_DIM']
    vectors = filter(lambda l: not l.startswith('$'), lines)
    vectors = map(lambda l: l.split(' '), vectors)
    vectors = map(lambda l: parse_vector(l, vec_dim), vectors)
    vectors = dict(map(lambda l: ((l.x, l.y), l), vectors))
    header['VECTORS'] = vectors
    return header


def parse(path: str) -> Optional[Dict]:
    with open(path) as f:
        if path.endswith('.map'):
            return parse_map(f)
        if path.endswith('.dwm'):
            return parse_winner_mapping(f)
        if path.endswith('.vec'):
            return parse_input_vectors(f)
        if path.endswith('.wgt'):
            return parse_weighted_vectors(f)
    return None


if __name__ == '__main__':
    parse('10Clusters-small.dwm')
