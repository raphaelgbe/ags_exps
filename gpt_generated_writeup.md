## 📝 Title

**“Probing In-Context Learning via Controlled Artificial Grammars”**

---

## 🧩 Motivation

Current LLM benchmarks primarily evaluate **stored knowledge** rather than the ability to **acquire new rules from limited experience**.

This benchmark isolates **learning as a process** by introducing:

- entirely synthetic grammars  
- unseen symbolic systems  
- controlled exposure regimes  

---

## 🎯 What this benchmark measures

We evaluate:

### 1. Concept acquisition
Can the model infer rules from examples?

### 2. Generalization
Can it apply rules to unseen cases?

### 3. Robustness
Can it distinguish valid from near-valid inputs?

---

## 🧠 Cognitive framing

Each grammar family targets a distinct faculty:

| Family | Cognitive Skill |
|------|----------------|
| Linear | sequence learning |
| Branching | uncertainty handling |
| Loop | abstraction / recursion |
| Delayed | working memory |
| Tight boundary | precision |
| Sparse | calibration |

---

## 🔬 What’s new

Unlike standard benchmarks:

- no memorized knowledge applies  
- rules must be inferred in-context  
- difficulty is *parametrically controlled*  
- failure modes are **diagnosable**

---

## 📊 Outputs

For each model:

- accuracy (ID / OOD)  
- learning curves  
- error breakdown by type  
- sensitivity to grammar complexity  

---

## 💡 Key insight

> Two models with similar accuracy may rely on fundamentally different strategies:
> - pattern matching  
> - true rule induction  

This benchmark distinguishes between them.