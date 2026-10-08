import unittest

from boyer_moore_majority_vote import MajorityVoter, find_majority


class TestMajorityVoter(unittest.TestCase):
    def test_empty_feeds_yield_none_candidate(self):
        voter = MajorityVoter()
        self.assertIsNone(voter.candidate)
        self.assertEqual(voter.count, 0)

    def test_single_element_becomes_candidate(self):
        voter = MajorityVoter()
        voter.feed("x")
        self.assertEqual(voter.candidate, "x")
        self.assertEqual(voter.count, 1)

    def test_majority_element_is_found(self):
        voter = MajorityVoter()
        voter.feed_all([1, 1, 2, 1, 3, 1, 1])
        self.assertEqual(voter.candidate, 1)
        self.assertEqual(voter.count, 7)

    def test_majority_with_equal_distribution_of_minorities(self):
        voter = MajorityVoter()
        voter.feed_all(["a", "b", "a", "c", "a", "d", "a"])
        self.assertEqual(voter.candidate, "a")

    def test_no_majority_returns_some_candidate(self):
        # No strict majority exists; algorithm still yields a candidate.
        voter = MajorityVoter()
        voter.feed_all([1, 2, 3, 4])
        self.assertIn(voter.candidate, (1, 2, 3, 4))

    def test_no_majority_pairs_cancel(self):
        # Classic cancelling pattern: candidate depends on order, but count
        # of the returned candidate need not exceed half.
        voter = MajorityVoter()
        voter.feed_all([1, 2, 1, 2])
        # First element re-emerges due to pairing order; documented behaviour.
        self.assertEqual(voter.candidate, 1)

    def test_two_to_one_majority(self):
        voter = MajorityVoter()
        voter.feed_all([5, 5, 5, 9])
        self.assertEqual(voter.candidate, 5)

    def test_majority_at_tail(self):
        voter = MajorityVoter()
        voter.feed_all([1, 2, 1, 2, 1, 2, 1])
        self.assertEqual(voter.candidate, 1)

    def test_reset_clears_state(self):
        voter = MajorityVoter()
        voter.feed_all([7, 7, 7])
        self.assertEqual(voter.candidate, 7)
        voter.reset()
        self.assertIsNone(voter.candidate)
        self.assertEqual(voter.count, 0)

    def test_reset_allows_reuse(self):
        voter = MajorityVoter()
        voter.feed_all([1, 1, 2])
        self.assertEqual(voter.candidate, 1)
        voter.reset()
        voter.feed_all([9, 9, 9, 3])
        self.assertEqual(voter.candidate, 9)

    def test_streaming_incremental_matches_batch(self):
        voter = MajorityVoter()
        voter.feed(1)
        voter.feed(1)
        self.assertEqual(voter.candidate, 1)
        voter.feed(2)
        voter.feed(2)
        # After two 1s and two 2s, candidate reverts due to pairing.
        self.assertEqual(voter.candidate, 1)
        voter.feed(1)
        self.assertEqual(voter.candidate, 1)

    def test_handles_none_as_element(self):
        # None is a legitimate element value, distinct from "no data fed".
        voter = MajorityVoter()
        voter.feed_all([None, None, None, 5])
        self.assertEqual(voter.candidate, None)
        self.assertEqual(voter.count, 4)

    def test_candidate_none_after_reset_means_no_data(self):
        voter = MajorityVoter()
        self.assertIsNone(voter.candidate)
        voter.reset()
        self.assertIsNone(voter.candidate)

    def test_count_tracks_total_not_leader_balance(self):
        voter = MajorityVoter()
        voter.feed_all([1, 2, 3])
        # Total items is 3, even though internal leader count is 1.
        self.assertEqual(voter.count, 3)


class TestFindMajority(unittest.TestCase):
    def test_empty_iterable_returns_none(self):
        self.assertIsNone(find_majority([]))

    def test_single_item_iterable(self):
        self.assertEqual(find_majority([42]), 42)

    def test_clear_majority(self):
        self.assertEqual(find_majority([0, 0, 0, 1, 2, 0, 0]), 0)

    def test_exactly_half_plus_one(self):
        # Smallest strict majority: 3 of 5.
        self.assertEqual(find_majority([1, 2, 1, 2, 1]), 1)

    def test_no_majority_iterable_returns_some_candidate(self):
        result = find_majority([1, 2, 3, 4, 5])
        self.assertIn(result, (1, 2, 3, 4, 5))

    def test_accepts_generator(self):
        def gen():
            for i in [2, 2, 3, 2, 4, 2, 2]:
                yield i
        self.assertEqual(find_majority(gen()), 2)

    def test_single_element_repeated(self):
        self.assertEqual(find_majority([7] * 6), 7)

    def test_two_elements_no_majority(self):
        # Equal counts: no strict majority; result is the first element by
        # the documented pairing order.
        self.assertEqual(find_majority([1, 1, 2, 2]), 1)


if __name__ == "__main__":
    unittest.main()
