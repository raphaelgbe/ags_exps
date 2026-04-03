import random
#===================
def generate_benchmark_instance(
    seed=42,
    num_states=4,
    alphabet=("a", "b"),
    num_loops=2,
    loop_length_range=(2, 3),
    n_train=30,
    n_test=30
):
    rng = random.Random(seed)

    # 1. Build grammar
    grammar = FSMGrammar(num_states=num_states, alphabet=alphabet, seed=seed)
    grammar.build_backbone()
    grammar.add_loops(num_loops=num_loops, loop_length_range=loop_length_range)
    grammar.add_random_transitions()

    # 2. Complexity
    comp = grammar_complexity(grammar)

    # 3. Dataset
    train, test_id, test_ood = generate_dataset(grammar, n_train, n_test)

    # 4. Stats
    train_stats = dataset_stats(grammar, train)
    test_id_stats = dataset_stats(grammar, test_id)
    test_ood_stats = dataset_stats(grammar, test_ood)

    # 5. Exportable grammar
    grammar_dict = {
        "num_states": grammar.num_states,
        "alphabet": grammar.alphabet,
        "start_state": grammar.start_state,
        "accept_states": list(grammar.accept_states),
        "transitions": grammar.transitions
    }

    return {
        "grammar": grammar_dict,
        "complexity": comp,
        "dataset_stats": {
            "train": train_stats,
            "test_id": test_id_stats,
            "test_ood": test_ood_stats
        },
        "train": train,
        "test_id": test_id,
        "test_ood": test_ood
    }


instance = generate_benchmark_instance()

print(instance["complexity"])
print(instance["dataset_stats"]["train"])
#===================