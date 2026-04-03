INVALID_TYPES = [
    "random",        # totally random
    "near_flip",     # one char flipped
    "truncated",     # valid prefix but cut early
    "extended",      # valid + extra junk
    "dead_end",      # leads to non-accepting state
]