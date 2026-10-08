"""Boyer-Moore majority vote streaming counter."""

from typing import Iterable, Optional


class MajorityVoter:
    """Streaming counter for the Boyer-Moore majority vote algorithm.

    Identifies a *candidate* that, if a strict majority element exists in the
    stream (appearing more than half the total count), is guaranteed to be that
    element. Uses O(1) memory and processes each item exactly once.

    Note that the algorithm always returns a candidate even when no majority
    exists; the caller must verify by counting if the input is not known to
    contain a majority.
    """

    __slots__ = ("_candidate", "_count", "_n")

    def __init__(self) -> None:
        # Pairing trick: increment for a match, decrement for a mismatch.
        # The leader survives because a true majority element offsets every
        # decrement with a greater number of increments.
        self._candidate: object = None
        self._count: int = 0
        self._n: int = 0

    def feed(self, item: object) -> None:
        """Process a single stream element."""
        self._n += 1
        if self._count == 0:
            self._candidate = item
            self._count = 1
        elif item == self._candidate:
            self._count += 1
        else:
            self._count -= 1

    def feed_all(self, items: Iterable[object]) -> None:
        """Process a batch of elements."""
        for item in items:
            self.feed(item)

    @property
    def candidate(self) -> object:
        """The current majority candidate, or ``None`` if nothing has been fed."""
        return self._candidate

    @property
    def count(self) -> int:
        """Number of items fed so far."""
        return self._n

    def reset(self) -> None:
        """Clear all state so the instance can be reused."""
        self._candidate = None
        self._count = 0
        self._n = 0


def find_majority(items: Iterable[object]) -> Optional[object]:
    """Return the Boyer-Moore majority candidate of ``items``, or ``None``.

    Returns ``None`` when the iterable is empty. Otherwise returns the
    candidate produced by a single-pass pairing pass.

    The candidate is guaranteed to be the true majority element *only* when a
    majority (strictly more than half) exists. For arbitrary input where that
    is not known, the caller must verify the result against the full data.
    """
    voter = MajorityVoter()
    voter.feed_all(items)
    return voter.candidate
