from collections import Counter, defaultdict
import math
import networkx as nx
import numpy as np

from src.datasets.utils import edit_distance

def count_duplicates_in_string_list(strings):
    counts = Counter(strings)
    unique_ratio = len(counts) / len(strings)
    return {
        "unique_ratio": unique_ratio,
        "duplicates": sum(v-1 for v in counts.values())
    }

def state_coverage(grammar, dataset):
    visited = set()
    
    for s in dataset:
        state = grammar.start_state
        visited.add(state)
        for sym in s:
            if sym in grammar.transitions[state]:
                state = grammar.transitions[state][sym]
                visited.add(state)
    
    return len(visited) / grammar.num_states

def transition_coverage(grammar, dataset):
    visited = set()
    total = 0
    
    for s in grammar.transitions:
        for sym in grammar.transitions[s]:
            total += 1
    
    for string in dataset:
        state = grammar.start_state
        for sym in string:
            if sym in grammar.transitions[state]:
                visited.add((state, sym))
                state = grammar.transitions[state][sym]
    
    return len(visited) / total

def grammar_complexity(grammar):
    G = nx.DiGraph()
    
    for s in grammar.transitions:
        for sym, t in grammar.transitions[s].items():
            G.add_edge(s, t)

    num_states = grammar.num_states
    num_edges = G.size()
    avg_branching = np.mean([len(grammar.transitions[s]) for s in grammar.transitions])

    cycles = list(nx.simple_cycles(G))
    num_cycles = len(cycles)
    avg_cycle_length = np.mean([len(c) for c in cycles]) if cycles else 0

    # estimate sparsity
    samples = [grammar.generate_valid() for _ in range(50)]
    sparsity = len(samples) / 50  # crude proxy

    return {
        "num_states": num_states,
        "num_edges": num_edges,
        "avg_branching": avg_branching,
        "num_cycles": num_cycles,
        "avg_cycle_length": avg_cycle_length,
        "sparsity": sparsity,
        "score": (
            1.0 * num_states +
            1.0 * avg_branching +
            1.5 * num_cycles +
            1.0 * avg_cycle_length +
            2.0 * (1 - sparsity)
        )
    }

def enumerate_prefixes(grammar, max_len=5):
    prefixes = set()

    def dfs(state, current, depth):
        if depth > max_len:
            return
        prefixes.add(current)

        for sym, nxt in grammar.transitions[state].items():
            dfs(nxt, current + sym, depth + 1)

    dfs(grammar.start_state, "", 0)
    return prefixes

def prefix_coverage(grammar, dataset, max_len=5):
    all_prefixes = enumerate_prefixes(grammar, max_len)
    
    dataset_prefixes = set()
    for s in dataset:
        for i in range(1, min(len(s), max_len) + 1):
            dataset_prefixes.add(s[:i])

    return len(dataset_prefixes) / len(all_prefixes) if all_prefixes else 1.0


def prefix_redundancy(strings, max_prefix_len=5):
    prefixes = []

    for s in strings:
        for i in range(1, min(len(s), max_prefix_len) + 1):
            prefixes.append(s[:i])

    unique = len(set(prefixes))
    total = len(prefixes)

    return {
        "prefix_unique_ratio": unique / total if total > 0 else 1.0,
        "total_prefixes": total
    }

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def build_trie(strings):
    root = TrieNode()
    
    for s in strings:
        node = root
        for c in s:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True
    
    return root

# diversity evaluation:
def enumerate_valid_strings_k(grammar, k, up_to=True):
    results = set()

    def dfs(state, current, depth):
        if depth <= k:
            if state in grammar.accept_states:
                results.add(current)
            return
        
        for sym, nxt in grammar.transitions[state].items():
            dfs(nxt, current + sym, depth + 1)

    dfs(grammar.start_state, "", 0)
    return results

def estimate_diversity(grammar, k=5):
    strings = enumerate_valid_strings_k(grammar, k)
    return len(strings)

def normalized_diversity(grammar, k=5):
    strings = enumerate_valid_strings_k(grammar, k, up_to=False)
    max_possible = len(grammar.alphabet) ** k
    return len(strings) / max_possible

 # entropy
def transition_entropy(grammar):

    H_total = 0
    count = 0

    for s in grammar.transitions:
        outgoing = grammar.transitions[s]
        n = len(outgoing)
        
        if n > 0:
            p = 1 / n  # assume uniform choice
            H = -n * p * math.log(p)
            H_total += H
            count += 1

    return H_total / max(count, 1)

from collections import defaultdict
import math

def estimate_entropy(grammar, samples=200):
    transitions = defaultdict(lambda: defaultdict(int))

    for _ in range(samples):
        s = grammar.generate_valid()
        for i in range(len(s)-1):
            prefix = s[:i]
            next_char = s[i]
            transitions[prefix][next_char] += 1

    H_total = 0
    count = 0

    for prefix in transitions:
        total = sum(transitions[prefix].values())
        for c in transitions[prefix]:
            p = transitions[prefix][c] / total
            H_total -= p * math.log(p + 1e-9)
        count += 1

    return H_total / max(count, 1)

def boundary_complexity(valid_samples, invalid_samples, num_valid_samples=20):
    distances = []
    for inv in invalid_samples:
        compare_samples = valid_samples if not num_valid_samples else sorted(valid_samples, key=lambda v: abs(len(v) - len(inv)))[:num_valid_samples]
        d = min(edit_distance(inv, v) for v in compare_samples)
        distances.append(d)
    return sum(distances) / len(distances)

def grammar_similarity(g1, g2, k=5):
    s1 = enumerate_valid_strings_k(g1, k, up_to=True)
    s2 = enumerate_valid_strings_k(g2, k, up_to=True)

    inter = len(s1 & s2)
    union = len(s1 | s2)

    return inter / union if union > 0 else 1.0