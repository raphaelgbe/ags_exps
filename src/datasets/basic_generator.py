import random
import numpy as np
from collections import Counter

from src.grammar.utils import state_coverage, transition_coverage

def generate_dataset(grammar, n_train=30, n_test=30, invalid_mode="mixed"):
    train = []
    test_id = []
    test_ood = []

    def sample_invalid():
        if invalid_mode == "random":
            return grammar.generate_invalid()
        elif invalid_mode == "near":
            v = grammar.generate_valid()
            return grammar.generate_invalid_near(v)
        else:  # mixed
            if random.random() < 0.5:
                return grammar.generate_invalid()
            else:
                v = grammar.generate_valid()
                return grammar.generate_invalid_near(v)

    # TRAIN
    for _ in range(n_train // 2):
        train.append({"string": grammar.generate_valid(), "label": "VALID"})
        train.append({"string": sample_invalid(), "label": "INVALID"})

    # TEST (ID)
    for _ in range(n_test // 2):
        test_id.append({"string": grammar.generate_valid(), "label": "VALID"})
        test_id.append({"string": sample_invalid(), "label": "INVALID"})

    # TEST (OOD - longer)
    for _ in range(n_test // 2):
        test_ood.append({"string": grammar.generate_valid(max_len=12), "label": "VALID"})
        test_ood.append({"string": sample_invalid(), "label": "INVALID"})

    return train, test_id, test_ood


def dataset_stats(grammar, dataset):
    strings = [x["string"] for x in dataset]
    labels = [x["label"] for x in dataset]

    # redundancy
    counts = Counter(strings)
    unique_ratio = len(counts) / len(strings)

    # balance
    valid_ratio = sum(1 for l in labels if l == "VALID") / len(labels)

    # coverage
    state_cov = state_coverage(grammar, strings)
    trans_cov = transition_coverage(grammar, strings)

    return {
        "size": len(dataset),
        "unique_ratio": unique_ratio,
        "valid_ratio": valid_ratio,
        "state_coverage": state_cov,
        "transition_coverage": trans_cov
    }