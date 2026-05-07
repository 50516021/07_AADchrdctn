"""Non-linear channel reduction helper for AAD pipelines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class ChannelReductionResult:
    """Result of channel reduction optimization."""

    selected_indices: list[int]
    retained_ratio: float


def optimize_aad_channels_nonlinear(
    scores: Sequence[float] | Iterable[float],
    *,
    retention_target: float = 0.95,
    gamma: float = 1.5,
    min_channels: int = 1,
) -> ChannelReductionResult:
    """Select the smallest high-value channel subset using non-linear scoring.

    A non-linear emphasis ``score ** gamma`` is used so high-value channels
    contribute proportionally more during selection.
    """

    values = [float(score) for score in scores]
    if not values:
        raise ValueError("scores must not be empty")
    if retention_target <= 0 or retention_target > 1:
        raise ValueError("retention_target must be in the range (0, 1]")
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    if min_channels < 1:
        raise ValueError("min_channels must be at least 1")
    if min_channels > len(values):
        raise ValueError("min_channels cannot exceed number of input scores")
    if any(score < 0 for score in values):
        raise ValueError("scores must be non-negative")

    weighted = [score**gamma for score in values]
    total = sum(weighted)
    if total == 0:
        return ChannelReductionResult(
            selected_indices=list(range(min_channels)),
            retained_ratio=1.0,
        )

    sorted_indices = sorted(range(len(weighted)), key=lambda index: weighted[index], reverse=True)
    selected: list[int] = []
    running = 0.0
    for index in sorted_indices:
        selected.append(index)
        running += weighted[index]
        if len(selected) >= min_channels and running / total >= retention_target:
            break

    selected.sort()
    return ChannelReductionResult(
        selected_indices=selected,
        retained_ratio=running / total,
    )
