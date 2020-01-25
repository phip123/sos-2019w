from typing import Dict, IO, Optional


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


def parse(path: str) -> Optional[Dict]:
    with open(path) as f:
        if path.endswith('.map'):
            return parse_map(f)
        if path.endswith('.dwm'):
            return parse_winner_mapping(f)
    return None


if __name__ == '__main__':
    parse('10Clusters-small.dwm')
