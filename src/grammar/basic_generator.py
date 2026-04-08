import json
import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque

class BasicGrammar:
    def __init__(self, num_states=4, alphabet=("a", "b"), seed=None):
        self.rng = random.Random(seed)
        self.num_states = num_states
        self.alphabet = list(alphabet)
        self.start_state = 0
        self.accept_states = {}

        self.transitions = {s: {} for s in range(num_states)}

    def _compute_effective_alphabet(self):
        effective_alphabet = set()
        for _, dct in self.transitions.items():
            for sym, _ in dct.items():
                effective_alphabet.add(sym)
        return effective_alphabet

    def is_valid(self, string):
        state = self.start_state
        for sym in string:
            if state not in self.transitions.keys():
                return False
            if sym not in self.transitions[state]:
                return False
            state = self.transitions[state][sym]
        return state in self.accept_states

    def generate_valid(self, max_len=8, num_tries=100, generate_candidates=True):
        candidates = []
        weights = []
        for _ in range(num_tries):
            state = self.start_state
            s = ""
            for _ in range(self.rng.randint(1, max_len)):
                if not self.transitions[state]:
                    break
                if (state in self.accept_states) and generate_candidates:
                    candidates.append(s)
                    weights.append(len(s))
                sym = self.rng.choice(list(self.transitions[state].keys()))
                s += sym
                state = self.transitions[state][sym]
            if state in self.accept_states:
                return s
        if generate_candidates and candidates:
            return random.choices(candidates, weights=weights)[0]
        return None
    
    def generate_plausible_invalid(self, expected_len, num_disruptions_range=(1,1), num_tries=100):
        num_disruptions = random.randint(*num_disruptions_range)
        num_disruptions_made = 0
        if (1 > num_disruptions) or (num_disruptions > expected_len):
            raise ValueError("num_disruptions_range should be between 1 and expected_len")
        disruption_points = set(random.sample(range(expected_len), num_disruptions))
        for _ in range(num_tries):
            state = self.start_state
            s = ""
            for i in range(expected_len):
                if not self.transitions[state]:
                    break
                sym = self.rng.choice(list(self.transitions[state].keys()))
                sym_to_add = sym
                if i in disruption_points:
                    possible_letters = {l for l in self.alphabet if l not in self.transitions[state].keys()}
                    if possible_letters:
                        sym_to_add = self.rng.choice(list(possible_letters))
                        num_disruptions_made += 1
                    else:
                        disruption_points.add(i+1)
                s += sym_to_add
                state = self.transitions[state][sym]
            if (i == expected_len-1) and (not self.is_valid(s)):
                return s, num_disruptions_made

    def generate_invalid(self, max_len=6, attempts=100):
        for _ in range(attempts):
            s = "".join(self.rng.choice(self.alphabet) for _ in range(self.rng.randint(1, max_len)))
            if not self.is_valid(s):
                return s
        return None

    def generate_invalid_near(self, valid_string):
        i = self.rng.randint(0, len(valid_string) - 1)
        new_sym = self.rng.choice([s for s in self.alphabet if s != valid_string[i]])
        new_string = valid_string[:i] + new_sym + valid_string[i+1:]
        return new_string if not self.is_valid(new_string) else None

    def enumerate_valid_samples(self, max_len=5, early_stop_function=None):
        outs = []
        to_visit = deque()
        to_visit.append((self.start_state, "", 0))
        while True:
            if not to_visit:
                break
            if early_stop_function and (early_stop_function(outs)):
                break
            s, curr, depth = to_visit.popleft()
            if s not in self.transitions.keys():  # could happen e.g. for an accept state
                continue
            for sym, nxt in self.transitions[s].items():
                outs.append(curr + sym)
                if depth < max_len:
                    to_visit.append((nxt, curr + sym, depth + 1))
        return outs

    def to_jsondumps(self):
        data = {
            "num_states": self.num_states,
            "alphabet": self.alphabet,
            "effective_alphabet": list(self._compute_effective_alphabet()),
            "start_state": self.start_state,
            "accept_states": list(self.accept_states),
            "transitions": self.transitions
        }
        return json.dumps(data)

    def to_json(self, path):
        data = {
            "num_states": self.num_states,
            "alphabet": self.alphabet,
            "effective_alphabet": list(self._compute_effective_alphabet()),
            "start_state": self.start_state,
            "accept_states": list(self.accept_states),
            "transitions": self.transitions
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def _get_effective_alphabet_from_data(data):
        if "effective_alphabet" in data.keys():
            return data["effective_alphabet"]
        effective_alphabet = data["alphabet"]
        if "symbol_map" in data.keys():
            for source, targets in data["symbol_map"].items():
                effective_alphabet.remove(source)
                effective_alphabet.extend([t for t in targets])
        return set(effective_alphabet)

    @staticmethod
    def from_json(input_text, is_path=True):
        if is_path:
            path = input_text
            with open(path) as f:
                data = json.load(f)
        else:
            data = json.loads(input_text)
        g = BasicGrammar(data["num_states"], data["alphabet"])
        g.start_state = data["start_state"]
        g.effective_alphabet = BasicGrammar._get_effective_alphabet_from_data(data)
        g.accept_states = set(data["accept_states"])
        if "symbol_map" in data.keys():
            g.transitions = {}
            for k, v in data["transitions"].items():
                g.transitions[int(k)] = {}
                for kk, vv in v.items():
                    if kk in data["symbol_map"].keys():
                        for newkk in data["symbol_map"][kk]:
                            g.transitions[int(k)][newkk] = int(vv)
                    else:
                        g.transitions[int(k)][kk] = int(vv)
        else:
            g.transitions = {int(k): {kk: int(vv) for kk, vv in v.items()} for k, v in data["transitions"].items()}
        return g

    def visualize_with_pygraphviz(self, filename="fsm.png"):
        from networkx.drawing.nx_agraph import to_agraph
        G = nx.MultiDiGraph()

        for s in self.transitions:
            for sym, t in self.transitions[s].items():
                G.add_edge(s, t, label=sym)

        A = to_agraph(G)

        # Optional styling (nice for FSMs)
        A.graph_attr.update(rankdir="LR")  # left-to-right layout
        A.node_attr.update(shape="circle")

        # Draw using Graphviz
        A.layout("dot")
        A.draw(filename)

    def visualize(self):
        print(f"Accept states:", self.accept_states)
        G = nx.DiGraph()
        edge_map = defaultdict(list)

        for s in self.transitions:
            for sym, t in self.transitions[s].items():
                if s <= t:
                    edge_map[(s,t)].append(sym + "→")
                else:
                    edge_map[(t,s)].append(sym + "←")

        for (s, t), syms in edge_map.items():
            G.add_edge(s, t, label=",".join(syms))

        pos = nx.spring_layout(G)

        nx.draw_networkx(G, pos, with_labels=True, node_color="lightblue", connectionstyle="arc3, rad=0.2")

        edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.show()