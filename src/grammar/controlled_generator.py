import json
import random
import networkx as nx
import matplotlib.pyplot as plt

from src.grammar.basic_generator import BasicGrammar

class ControlledFSM(BasicGrammar):
    def __init__(self, num_states=5, alphabet=("a", "b"), seed=None):
        self.rng = random.Random(seed)
        self.num_states = num_states
        self.alphabet = list(alphabet)
        self.start_state = 0

        self.transitions = {s: {} for s in range(num_states)}
        self.accept_states = set()

    def build_connected_dag(self, max_out=2, max_nodes_to_expand=None):
        if max_nodes_to_expand is None:
            max_nodes_to_expand = self.num_states

        reachable = {self.start_state}

        # ensure all states are reachable
        for s in range(1, self.num_states):
            parent = self.rng.choice(list(reachable))
            sym = self.rng.choice(self.alphabet)
            self.transitions[parent][sym] = s
            reachable.add(s)

        # add extra forward edges (still acyclic)
        num_extra_edges = 0
        for s in self.rng.sample(range(self.num_states), max_nodes_to_expand):
            possible_targets = [t for t in range(s+1, self.num_states)]
            possible_letters = {l for l in self.alphabet if l not in self.transitions[s].keys()}
            num_edges = self.rng.randint(0, min(max_out, len(possible_targets), len(possible_letters)))

            for t in self.rng.sample(possible_targets, num_edges):
                if not possible_letters:
                    break
                num_extra_edges += 1
                sym = self.rng.choice(list(possible_letters))
                possible_letters.remove(sym)
                self.transitions[s][sym] = t
        self.num_extra_forward_edges = num_extra_edges

    def add_backward_edges(self, num_new_edges):
        self.num_backward_edges_created = 0
        for _ in range(num_new_edges):
            state = self.rng.randint(1, self.num_states)
            candidate = self.rng.randint(0, state - 1)
            if state not in self.transitions.keys():
                self.transitions[state] = {}
            possible_letters = {l for l in self.alphabet if l not in self.transitions[state].keys()}
            if (not possible_letters) or (candidate in self.transitions[state].values()):
                continue
            self.num_backward_edges_created += 1
            self.transitions[state][self.rng.choice(list(possible_letters))] = candidate

    def add_loops(self, num_loops=2, loop_length_range=(2, 4)):
        num_loops_created = 0
        for _ in range(num_loops):
            length = self.rng.randint(*loop_length_range)
            states = [self.rng.randint(0, self.num_states - 1) for _ in range(length)]

            loop_successfully_created = True  # won't be successful if we arrive at a state where no new connection can be created without breaking another
            for i in range(length):
                if states[(i + 1) % length] in self.transitions[states[i]].values():
                    # don't modify already existing edges:
                    continue
                else:
                    possible_letters = [l for l in self.alphabet if l not in self.transitions[states[i]].keys()]
                    if not possible_letters:
                        loop_successfully_created = False
                        break
                    sym = self.rng.choice(list(possible_letters))
                    self.transitions[states[i]][sym] = states[(i + 1) % length]
            num_loops_created += int(loop_successfully_created)
        self.num_loops_created = num_loops_created

    def _reverse_graph(self):
        reverse = {s: [] for s in self.transitions}
        for s in self.transitions:
            for sym, t in self.transitions[s].items():
                reverse[t].append(s)
        return reverse

    def set_accept_states(self, num_accept=1):
        num_accept_states = num_accept
        # pick random accept states
        self.accept_states = set(self.rng.sample(range(self.num_states), num_accept))

        # ensure all states can reach an accept state
        reverse = self._reverse_graph()

        good = set(self.accept_states)
        stack = list(good)

        while stack:
            s = stack.pop()
            for prev in reverse[s]:
                if prev not in good:
                    good.add(prev)
                    stack.append(prev)

        # prune bad states by redirecting them
        for s in range(self.num_states):
            if s not in good:
                possible_letters = {l for l in self.alphabet if l not in self.transitions[s].keys()}
                if not possible_letters:
                    self.accept_states.add(s)
                    num_accept_states += 1
                else:
                    # force a path to an accept state
                    target = self.rng.choice(list(self.accept_states))
                    sym = self.rng.choice(list(possible_letters))
                    self.transitions[s][sym] = target

    def validate(self):
        reachable = set()

        def dfs(s):
            if s in reachable:
                return
            reachable.add(s)
            for _, t in self.transitions[s].items():
                dfs(t)

        dfs(self.start_state)

        assert len(reachable) == self.num_states, "Unreachable states exist"
        assert len(self.accept_states) > 0, "No accept states"

    # def generate_report(self):
    #     G = nx.Graph()
    #     for s in self.transitions:
    #         for _, t in self.transitions[s].items():
    #             G.add_edge(s, t)
    #     cycles = list(nx.simple_cycles(G))
    #     num_cycles = len(cycles)
    #     num_edges = G.size()
    #     report = f"""
    #         Number of states: {self.num_states}
    #         Number of edges: {num_edges}
    #         Number of loops: {num_cycles}
    #     """
    #     return report

    def build(self, max_out=2, num_backward_edges=1, num_loops=2, loop_length_range=(2, 4), num_accept=1):
        self.build_connected_dag(max_out=max_out)
        print(f"Added {self.num_extra_forward_edges} forward edges in backbone DAG")
        self.add_backward_edges(num_backward_edges)
        print(f"Added {self.num_backward_edges_created} backward edges in DAG")
        self.add_loops(num_loops=num_loops, loop_length_range=loop_length_range)
        print(f"Added {self.num_loops_created} loops in DAG")
        self.set_accept_states(num_accept=num_accept)
        print(f"Number of accept states: {len(self.accept_states)}")
        self.validate()
        print("The graph is validated!")
        self.effective_alphabet = self._compute_effective_alphabet()
        # print(self.generate_report())