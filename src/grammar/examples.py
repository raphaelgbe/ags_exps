# lowercase alphabets:
ALL_LOWERCASE_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

SIMPLE_LOOP_GRAMMAR = """{
  "num_states": 1,
  "alphabet": ["a"],
  "start_state": 0,
  "accept_states": [0],
  "transitions": {
    "0": {"a": 0}
  }
}"""  # ESTIMATED DIFFICULTY 1

ALTERNATING_AB_LOOP_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["a", "b"],
  "start_state": 0,
  "accept_states": [2],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 2},
    "2": {"a": 1},
  }
}"""  # ESTIMATED DIFFICULTY 1.5

ALTERNATING_ABEXPONENT_LOOP_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["a", "b"],
  "start_state": 0,
  "accept_states": [2],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 2},
    "2": {"a": 1, "b": 2},
  }
}"""  # ESTIMATED DIFFICULTY 2

ALTERNATING_CONSONANT_VOWEL_LOOP_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["a", "b"],
  "symbol_map": {"a": "bcdfghjklmnpqrstvwxyz", "b": "aeiou"},
  "start_state": 0,
  "accept_states": [2],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 2},
    "2": {"a": 1},
  }
}"""  # ESTIMATED DIFFICULTY 2 : simple structure, larger alphabet

ALTERNATING_CONSONANT_VOWELEXPONENT_LOOP_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["a", "b"],
  "symbol_map": {"a": "bcdfghjklmnpqrstvwxyz", "b": "aeiou"},
  "start_state": 0,
  "accept_states": [2],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 2},
    "2": {"a": 1, "b": 2},
  }
}"""  # ESTIMATED DIFFICULTY 3

ALTERNATING_GIBBEGIBBERISH_LOOP_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["a", "b"],
  "symbol_map": {"a": "qdnblvtcxjeys", "b": "afghikmopruwz"},
  "start_state": 0,
  "accept_states": [2],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 2},
    "2": {"a": 1},
  }
}"""  # ESTIMATED DIFFICULTY 3: no structure in alphabet distribution

ALTERNATING_GIBBEGIBBERISHEXPONENT_LOOP_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["a", "b"],
  "symbol_map": {"a": "qdnblvtcxjeys", "b": "afghikmopruwz"},
  "start_state": 0,
  "accept_states": [2],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 2},
    "2": {"a": 1, "b": 2},
  }
}"""  # ESTIMATED DIFFICULTY 4: no structure in alphabet distribution

# derived from https://www.sciencedirect.com/science/article/pii/S0028393217303160:
LADDER_GRAMMAR = """{
  "num_states": 12,
  "alphabet": ["a", "b", "c", "d", "e"],
  "start_state": 0,
  "accept_states": [11]],
  "transitions": {
    "0": {"c": 1, "a": 3},
    "1": {"d": 2},
    "2": {"c": 1, "a": 3},
    "3": {"a": 4, "b": 8},
    "4": {"a": 5, "b": 7},
    "5": {"a": 4, "b": 6},
    "6": {"b": 7},
    "7": {"b": 8},
    "8": {"c": 9, "e": 11},
    "9": {"d": 10},
    "10": {"c": 9, "e": 11}
  }
}""" # ESTIMATED DIFFICULTY 4: simple alphabet, elaborate structure, ending char can be a red herring


# from https://en.wikipedia.org/wiki/Artificial_grammar_learning:
WAYBACK_GRAMMAR = """{
  "num_states": 6,
  "alphabet": ["p", "s", "t", "v", "x"],
  "start_state": 0,
  "accept_states": [5],
  "transitions": {
    "0": {"t": 1, "v": 2},
    "1": {"p": 1, "t": 3},
    "2": {"x": 2, "v": 4},
    "3": {"x": 2, "s": 5},
    "4": {"p": 3, "s": 5}
  }
}"""

# word alphabets

ALTERNATING_MUSTSTOP_LOOP_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["must ", "stop "],
  "start_state": 0,
  "accept_states": [2],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 2},
    "2": {"a": 1},
  }
}"""  # ESTIMATED DIFFICULTY 2: poisoning with meaning

ALTERNATING_MUSTSTOPEXPONENT_LOOP_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["must ", "stop "],
  "start_state": 0,
  "accept_states": [2],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 2},
    "2": {"a": 1, "b": 2},
  }
}"""  # ESTIMATED DIFFICULTY 2+: poisoning with meaning

# GPT-generated simple grammars

LINEAR_GRAMMAR = """{
  "num_states": 4,
  "alphabet": ["a"],
  "start_state": 0,
  "accept_states": [3],
  "transitions": {
    "0": {"a": 1},
    "1": {"a": 2},
    "2": {"a": 3},
    "3": {}
  }
}"""

BRANCHING_GRAMMAR = """{
  "num_states": 5,
  "alphabet": ["a", "b"],
  "start_state": 0,
  "accept_states": [3, 4],
  "transitions": {
    "0": {"a": 1, "b": 2},
    "1": {"a": 3, "b": 4},
    "2": {"a": 3, "b": 4},
    "3": {},
    "4": {}
  }
}"""

LOOP_GRAMMAR = """{
  "num_states": 2,
  "alphabet": ["a", "b"],
  "start_state": 0,
  "accept_states": [0],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 0}
  }
}"""

DELAYED_CONSTRAINT_GRAMMAR = """{
  "num_states": 5,
  "alphabet": ["a", "b", "x", "y"],
  "start_state": 0,
  "accept_states": [3, 4],
  "transitions": {
    "0": {"a": 1, "b": 2},
    "1": {"a": 1, "x": 3},
    "2": {"b": 2, "y": 4},
    "3": {},
    "4": {}
  }
}"""

TIGHT_BOUNDARY_GRAMMAR = """{
  "num_states": 3,
  "alphabet": ["a", "b"],
  "start_state": 0,
  "accept_states": [0],
  "transitions": {
    "0": {"a": 1},
    "1": {"b": 0}
  }
}"""

SPARSE_GRAMMAR = """{
  "num_states": 5,
  "alphabet": ["a", "b"],
  "start_state": 0,
  "accept_states": [4],
  "transitions": {
    "0": {"a": 1, "b": 2},
    "1": {"a": 3},
    "2": {"b": 3},
    "3": {"a": 4},
    "4": {}
  }
}"""