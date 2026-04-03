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