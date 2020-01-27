import math
from typing import List


def distance(vec1: List[float], vec2: List[float]) -> float:
    if len(vec1) != len(vec2):
        raise AttributeError('Vectors must have same dimensions for distance.')
    dist = 0.0
    for i in range(len(vec1)):
        dist += (vec1[i] - vec2[i]) * (vec1[i] - vec2[i])
    a =  math.sqrt(dist)
    return a
