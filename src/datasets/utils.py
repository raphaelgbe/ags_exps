import random

def edit_distance(a, b):
    dp = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + (a[i-1] != b[j-1])
            )
    return dp[-1][-1]

def enumerate_prefixes_k(grammar, k):
    prefixes = set()

    def dfs(state, current, depth):
        if depth == k:
            prefixes.add(current)
            return
        for sym, nxt in grammar.transitions[state].items():
            dfs(nxt, current + sym, depth + 1)

    dfs(grammar.start_state, "", 0)
    return prefixes

def prefix_coverage_k(grammar, dataset, k):
    all_p = enumerate_prefixes_k(grammar, k)
    
    data_p = set()
    for s in dataset:
        if len(s) >= k:
            data_p.add(s[:k])

    return len(data_p & all_p) / len(all_p) if all_p else 1.0

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

def prefix_validity(grammar, string):
    state = grammar.start_state
    valid_steps = 0

    for sym in string:
        if sym in grammar.transitions[state]:
            state = grammar.transitions[state][sym]
            valid_steps += 1
        else:
            break

    return valid_steps / len(string)

def credibility_score(grammar, string, valid_samples):
    prefix_score = prefix_validity(grammar, string)

    distances = [edit_distance(string, v) for v in valid_samples[:10]]
    dist_score = 1 / (1 + min(distances)) if distances else 0

    return 0.6 * prefix_score + 0.4 * dist_score

def generate_invalid_tagged(grammar, valid_samples):
    mode = random.choice(["random", "near_flip", "truncated", "extended"])

    if mode == "random":
        s = grammar.generate_invalid()
    elif mode == "near_flip":
        v = random.choice(valid_samples)
        s = grammar.generate_invalid_near(v)
    elif mode == "truncated":
        v = random.choice(valid_samples)
        s = v[:len(v)//2]
    elif mode == "extended":
        v = random.choice(valid_samples)
        s = v + random.choice(grammar.alphabet)
    else:
        s = grammar.generate_invalid()

    cred = credibility_score(grammar, s, valid_samples)

    return {
        "string": s,
        "label": "INVALID",
        "type": mode,
        "credibility": cred
    }

def analyze_errors(preds, dataset):
    results = {
        "false_positive": 0,
        "false_negative": 0,
        "by_type": {},
        "high_cred_errors": 0
    }

    for pred, item in zip(preds, dataset):
        true = item["label"]

        if pred != true:
            if true == "INVALID":
                results["false_positive"] += 1
                if item.get("credibility", 0) > 0.7:
                    results["high_cred_errors"] += 1

                t = item.get("type", "unknown")
                results["by_type"][t] = results["by_type"].get(t, 0) + 1

            else:
                results["false_negative"] += 1

    return results