import json
import random
import networkx as nx
import matplotlib.pyplot as plt

from basic_generator import BasicGrammar

class FSMGrammar(BasicGrammar):
    def __init__(self, num_states=4, alphabet=("a", "b"), num_accept_state=None, seed=None):
        self.rng = random.Random(seed)
        self.num_states = num_states
        self.alphabet = list(alphabet)
        self.start_state = 0
        self.accept_states = {self.rng.randint(0, num_accept_state if num_accept_state else num_states - 1)}

        self.transitions = {s: {} for s in range(num_states)}

    def build_random_graph(self):
        # transitions: state -> symbol -> next_state
        self.transitions = {
            s: {sym: self.rng.randint(0, self.num_states - 1) for sym in self.alphabet}
            for s in range(self.num_states)
        }

    def build_backbone(self):
        for s in range(self.num_states - 1):
            sym = self.rng.choice(self.alphabet)
            self.transitions[s][sym] = s + 1

    def add_random_transitions(self, prob=0.7):
        for s in range(self.num_states):
            for sym in self.alphabet:
                if sym not in self.transitions[s] and self.rng.random() < prob:
                    self.transitions[s][sym] = self.rng.randint(0, self.num_states - 1)

    def add_loops(self, num_loops=2, loop_length_range=(2, 3)):
        for _ in range(num_loops):
            length = self.rng.randint(*loop_length_range)
            states = [self.rng.randint(0, self.num_states - 1) for _ in range(length)]
            for i in range(length):
                sym = self.rng.choice(self.alphabet)
                self.transitions[states[i]][sym] = states[(i + 1) % length]

    def is_valid(self, string):
        state = self.start_state
        for sym in string:
            if sym not in self.transitions[state]:
                return False
            state = self.transitions[state][sym]
        return state in self.accept_states

    def generate_valid(self, max_len=8):
        for _ in range(100):
            state = self.start_state
            s = ""
            for _ in range(self.rng.randint(1, max_len)):
                if not self.transitions[state]:
                    break
                sym = self.rng.choice(list(self.transitions[state].keys()))
                s += sym
                state = self.transitions[state][sym]
            if state in self.accept_states:
                return s
        return None

    def generate_invalid_near(self, valid_string):
        i = self.rng.randint(0, len(valid_string) - 1)
        new_sym = self.rng.choice([s for s in self.alphabet if s != valid_string[i]])
        return valid_string[:i] + new_sym + valid_string[i+1:]
