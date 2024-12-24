from abc import abstractmethod
from collections import defaultdict
import random
from AoCUtils.utils import *


class AbstractNode:
    @abstractmethod
    def compute(self, wire_values):
        pass


class Node(AbstractNode):
    def __init__(self, wire1, wire2, op, out):
        self.wire1 = wire1
        self.wire2 = wire2
        self.op = op
        self.out = out

    def compute(self, wire_values):
        wire1_value = wire_values[self.wire1]
        wire2_value = wire_values[self.wire2]

        if self.op == "AND":
            return wire1_value & wire2_value
        if self.op == "OR":
            return wire1_value | wire2_value
        return wire1_value ^ wire2_value


class CompletedNode(AbstractNode):
    def __init__(self, wire, out):
        self.wire = wire
        self.out = out

    def compute(self, _):
        return self.out


def gen_id(wire_label_1, wire_label_2):
    return f"{wire_label_1}-{wire_label_2}"


def part_one():
    input = parse_input("input1.txt")

    vertices = {}
    outgoing_edges = defaultdict(set)
    incoming_degrees = defaultdict(int)
    zero_incoming_degrees = []
    num_bits = 0

    for line in input:
        if ":" in line:
            l = line.split(":")

            vertices[l[0]] = CompletedNode(l[0], int(l[1]))
            zero_incoming_degrees.append(l[0])

            if "z" in l[0]:
                num_bits += 1
        elif "->" in line:
            l = line.split()

            vertices[l[4]] = Node(l[0], l[2], l[1], l[4])
            outgoing_edges[l[0]].add(l[4])
            outgoing_edges[l[2]].add(l[4])
            incoming_degrees[l[4]] += 2

            if "z" in l[4]:
                num_bits += 1

    return top_sort(
        zero_incoming_degrees, vertices, outgoing_edges, incoming_degrees, num_bits
    )


def part_two():
    # 010101 = 21
    # 001101 = 13
    input = parse_input("input2.txt")

    vertices = {}
    outgoing_edges = defaultdict(set)
    incoming_degrees = defaultdict(int)
    zero_incoming_degrees = []
    num_bits = 0

    for line in input:
        if ":" in line:
            l = line.split(":")

            vertices[l[0]] = CompletedNode(l[0], int(l[1]))
            zero_incoming_degrees.append(l[0])

            if "z" in l[0]:
                num_bits += 1
        elif "->" in line:
            l = line.split()

            vertices[l[4]] = Node(l[0], l[2], l[1], l[4])
            outgoing_edges[l[0]].add(l[4])
            outgoing_edges[l[2]].add(l[4])
            incoming_degrees[l[4]] += 2

            if "z" in l[4]:
                num_bits += 1

    build_dependency_graph(vertices)
    # find_problematic_bits(
    #     zero_incoming_degrees,
    #     vertices,
    #     outgoing_edges,
    #     incoming_degrees,
    #     num_bits,
    #     max_bits=45,
    # )
    return


def find_problematic_bits(
    zero_incoming_degrees,
    vertices,
    outgoing_edges,
    incoming_degrees,
    num_bits,
    max_bits=45,
):
    freq = defaultdict(int)

    for i in range(10000):
        # print(i)
        random_bits_x = [int(digit) for digit in bin(random.getrandbits(max_bits))[2:]]
        random_bits_y = [int(digit) for digit in bin(random.getrandbits(max_bits))[2:]]

        while len(random_bits_x) < max_bits:
            random_bits_x.append(0)
        while len(random_bits_y) < max_bits:
            random_bits_y.append(0)
        # print(random_bits_x)
        # print(random_bits_y)

        modified_vertices = vertices.copy()
        for j in range(max_bits):
            modified_vertices[f"x0{j}" if j < 10 else f"x{j}"] = CompletedNode(
                f"x0{j}" if j < 10 else f"x{j}", int(random_bits_x[j])
            )
            modified_vertices[f"y0{j}" if j < 10 else f"y{j}"] = CompletedNode(
                f"y0{j}" if j < 10 else f"y{j}", int(random_bits_y[j])
            )

        incorrect_sum = bin(
            top_sort(
                zero_incoming_degrees.copy(),
                modified_vertices,
                outgoing_edges.copy(),
                incoming_degrees.copy(),
                num_bits,
            )
        )[2:]

        x_num = int("".join(list(map(str, reversed(random_bits_x)))), 2)
        y_num = int("".join(list(map(str, reversed(random_bits_y)))), 2)
        correct_sum = bin(x_num + y_num)[2:]

        if len(correct_sum) != len(incorrect_sum):
            # print("Incorrect Lengths!")
            continue
        c_incorrect_bits = set()
        for k in range(len(correct_sum)):
            if incorrect_sum[k] != correct_sum[k]:
                c_incorrect_bits.add(len(correct_sum) - 1 - k)
                freq[len(correct_sum) - 1 - k] += 1
        # print("Incorrect Bits: ", c_incorrect_bits)
    for k in sorted(freq.keys()):
        print(k, freq[k])

    return


def build_dependency_graph(vertices, max_bits=45):
    for i in range(max_bits):
        bit_str = f"z0{i}" if i < 10 else f"z{i}"
        eq = build_equation(vertices, bit_str)

        print(f"{bit_str} = {eq}\n")
        x_bit_str = f"x0{i}" if i < 10 else f"x{i}"
        y_bit_str = f"y0{i}" if i < 10 else f"y{i}"
        # if (
        #     f"{x_bit_str} XOR {y_bit_str}" not in eq
        #     and f"{y_bit_str} XOR {x_bit_str}" not in eq
        # ):
        #     print(f"Missing the addition at {bit_str}")

    return


def build_equation(vertices, c_vertex):
    if "x" in c_vertex or "y" in c_vertex:
        return c_vertex

    vertex_node: AbstractNode = vertices[c_vertex]
    return f"{build_equation(vertices, vertex_node.wire1)} {vertex_node.op} {build_equation(vertices, vertex_node.wire2)}"


def top_sort(
    zero_incoming_degrees, vertices, outgoing_edges, incoming_degrees, num_bits
):
    # Topological Sort
    wire_values = {}
    while len(zero_incoming_degrees) != 0:
        vertex = zero_incoming_degrees.pop()
        vertex_node: AbstractNode = vertices[vertex]

        computed_value = vertex_node.compute(wire_values)
        wire_values[vertex] = computed_value

        for outgoing_vertex in outgoing_edges[vertex]:
            incoming_degrees[outgoing_vertex] -= 1

            if incoming_degrees[outgoing_vertex] == 0:
                zero_incoming_degrees.append(outgoing_vertex)

    final_bits = ["0"] * num_bits
    for k, v in wire_values.items():
        if "z" in k:
            final_bits[int(k[1:])] = str(v)

    final_bit = "".join(final_bits[::-1])
    return int(final_bit, 2)


run_code(part_one, part_two)
