from collections import defaultdict
from AoCUtils.utils import *


def part_one():
    inputs = parse_input("input1.txt")
    adjacency_list = defaultdict(set)

    for connection in inputs:
        connection = connection.split("-")
        adjacency_list[connection[0]].add(connection[1])
        adjacency_list[connection[1]].add(connection[0])

    interconnected = set()
    for first_c in adjacency_list.keys():
        for second_c in adjacency_list[first_c]:
            intersect = adjacency_list[first_c] & adjacency_list[second_c]
            for third_c in intersect:
                interconnected.add(tuple(sorted([first_c, second_c, third_c])))

    num_t_connections = 0
    for first_c, second_c, third_c in interconnected:
        if (
            first_c.startswith("t")
            or second_c.startswith("t")
            or third_c.startswith("t")
        ):
            num_t_connections += 1
    return num_t_connections


def part_two():
    inputs = parse_input("input2.txt")
    adjacency_list = defaultdict(set)
    vertices = set()

    for connection in inputs:
        connection = connection.split("-")
        adjacency_list[connection[0]].add(connection[1])
        adjacency_list[connection[1]].add(connection[0])
        vertices.add(connection[0])
        vertices.add(connection[1])

    # Learned Bron-Kerbosch Algorithm for finding all maximal cliques
    maximal_cliques = bron_kerbosch(adjacency_list, set(), vertices, set())

    largest_set = set()
    for clique in maximal_cliques:
        if len(clique) > len(largest_set):
            largest_set = clique

    return ",".join(sorted(largest_set))


def bron_kerbosch(adjacency_list, reported, potential, excluded):
    if not potential and not excluded:
        return [reported]

    maximal_cliques = []
    cp_potential = potential.copy()

    for v in cp_potential:
        maximal_cliques += bron_kerbosch(
            adjacency_list,
            reported | {v},
            potential & adjacency_list[v],
            excluded & adjacency_list[v],
        )
        potential.discard(v)
        excluded.add(v)

    return maximal_cliques


run_code(part_one, part_two)
