import unittest

from aad_channel_reduction import optimize_aad_channels_nonlinear


class OptimizeAADChannelsNonlinearTests(unittest.TestCase):
    def test_selects_smallest_subset_for_target(self) -> None:
        result = optimize_aad_channels_nonlinear(
            [0.9, 0.7, 0.3, 0.1],
            retention_target=0.9,
            gamma=2.0,
        )
        self.assertEqual(result.selected_indices, [0, 1])
        self.assertGreaterEqual(result.retained_ratio, 0.9)

    def test_respects_min_channels_even_if_target_met(self) -> None:
        result = optimize_aad_channels_nonlinear(
            [1.0, 0.05, 0.04],
            retention_target=0.8,
            gamma=1.5,
            min_channels=2,
        )
        self.assertEqual(len(result.selected_indices), 2)

    def test_zero_scores_returns_min_channels(self) -> None:
        result = optimize_aad_channels_nonlinear(
            [0.0, 0.0, 0.0],
            min_channels=2,
        )
        self.assertEqual(result.selected_indices, [0, 1])
        self.assertEqual(result.retained_ratio, 1.0)

    def test_rejects_negative_scores(self) -> None:
        with self.assertRaises(ValueError):
            optimize_aad_channels_nonlinear([0.3, -0.1, 0.9])


if __name__ == "__main__":
    unittest.main()
