import json
import random
import networkx as nx
import matplotlib.pyplot as plt

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
        for _, sym in self.transitions.items():
            effective_alphabet.add(sym)
        return effective_alphabet

    def is_valid(self, string):
        state = self.start_state
        for sym in string:
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
    def from_json(path):
        with open(path) as f:
            data = json.load(f)
        g = BasicGrammar(data["num_states"], data["alphabet"])
        g.start_state = data["start_state"]
        g.effective_alphabet = set(data["effective_alphabet"])
        g.accept_states = set(data["accept_states"])
        if "symbol_map" in data.keys():
            g.transitions = {}
            for k, v in data["transitions"].items():
                g.transitions[int(k)] = {}
                for kk, vv in v.items():
                    if kk in data["symbol_maps"].keys():
                        for newkk in data["symbol_maps"][kk]:
                            g.transitions[int(k)][newkk] = int(vv)
                    else:
                        g.transitions[int(k)][kk] = int(vv)
        else:
            g.transitions = {int(k): {kk: int(vv) for kk, vv in v.items()} for k, v in data["transitions"].items()}
        return g

    def visualize(self):
        G = nx.DiGraph()
        for s in self.transitions:
            for sym, t in self.transitions[s].items():
                G.add_edge(s, t, label=sym)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="lightblue")

        edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.show()