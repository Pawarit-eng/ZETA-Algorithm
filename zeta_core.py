# zeta_core.py
# ZETA Algorithm - Core Version (Greedy Only)
# Created by Pawarit Chantaraket

import math
import random
from time import time

# Generate random cities
def generate_cities(n, seed=42):
    random.seed(seed)
    return {i: (random.randint(0, 1000), random.randint(0, 1000)) for i in range(n)}

# Euclidean distance
def dist(a, b, cities):
    ax, ay = cities[a]
    bx, by = cities[b]
    return math.hypot(ax - bx, ay - by)

# Greedy TSP inside a list of cities
def tsp_greedy(city_list, cities):
    start = city_list[0]
    unvisited = set(city_list)
    path = [start]
    unvisited.remove(start)
    while unvisited:
        last = path[-1]
        next_city = min(unvisited, key=lambda x: dist(last, x, cities))
        path.append(next_city)
        unvisited.remove(next_city)
    cost = sum(dist(path[i], path[i+1], cities) for i in range(len(path)-1)) + dist(path[-1], path[0], cities)
    return path, cost

# Core ZETA algorithm (greedy by zone)
def zlh_tsp(cities, zone_size=5):
    city_ids = list(cities.keys())
    zones = [city_ids[i:i+zone_size] for i in range(0, len(city_ids), zone_size)]

    zone_paths = {}
    zone_costs = {}

    for zid, zcities in enumerate(zones):
        path, cost = tsp_greedy(zcities, cities)
        zone_paths[zid] = path
        zone_costs[zid] = cost

    zone_order = list(zone_paths.keys())
    total_cost = 0
    full_path = []

    for i, zid in enumerate(zone_order):
        full_path += zone_paths[zid]
        total_cost += zone_costs[zid]
        if i < len(zone_order) - 1:
            end_city = zone_paths[zid][-1]
            next_city = zone_paths[zone_order[i+1]][0]
            total_cost += dist(end_city, next_city, cities)

    if full_path:
        total_cost += dist(full_path[-1], full_path[0], cities)
    return full_path, total_cost

# Example usage
if __name__ == "__main__":
    n = 1000000
    cities = generate_cities(n)
    start = time()
    path, cost = zlh_tsp(cities)
    elapsed = time() - start

    print(f"ZETA Core Version")
    print(f"# Cities: {n}")
    print(f"Total Cost: {round(cost, 2)}")
    print(f"Runtime: {round(elapsed, 4)} seconds")
    print(f"Path Valid: {len(set(path)) == len(cities)}")
