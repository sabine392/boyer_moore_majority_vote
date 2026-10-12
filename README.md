# Boyer Moore Majority Vote

A small, dependency-free Python library implementing the Boyer-Moore majority vote algorithm as a streaming counter. It identifies a majority candidate element in a single pass using constant memory.

## Usage

```python
from boyer_moore_majority_vote import MajorityVoter, find_majority

# Streaming interface
voter = MajorityVoter()
voter.feed_all([1, 1, 2, 1, 3, 1, 1])
print(voter.candidate)  # 1

# Convenience function
print(find_majority(["a", "b", "a", "c", "a", "d", "a"]))  # a
```

## Why this exists

The Boyer-Moore algorithm solves a specific problem: given a stream too large to buffer, detect whether a single element accounts for more than half of all observations. The trade-off is memory versus certainty — the counter uses O(1) space, but it always produces a candidate even when no strict majority exists. A second verification pass is required to confirm the candidate when input guarantees are not known.

This library provides only the detection pass. It keeps a single leader and a balance counter: matches increment, mismatches decrement, and a depleted leader is replaced by the current element. The total item count is tracked separately so the public `count` reflects input volume rather than internal leader balance.

## Edge cases

The candidate after an empty stream is `None`. Feeding `None` as a real element value is supported and is distinct from having fed nothing. When no strict majority exists, the returned candidate is arbitrary with respect to majority semantics — it is one of the observed elements, selected by stream order, but it is not guaranteed to be the most frequent element.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

