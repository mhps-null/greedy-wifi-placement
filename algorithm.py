from __future__ import annotations

from itertools import combinations
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class GreedyStep:
    iteration: int
    selected_candidate: str
    newly_covered: tuple[str, ...]
    remaining_uncovered: tuple[str, ...]


@dataclass(frozen=True)
class GreedyResult:
    selected_candidates: tuple[str, ...]
    covered_users: tuple[str, ...]
    uncovered_users: tuple[str, ...]
    steps: tuple[GreedyStep, ...]

    @property
    def is_complete(self) -> bool:
        return not self.uncovered_users


def greedy_set_cover(
    all_users: set[str],
    coverage_map: Mapping[str, set[str]],
) -> GreedyResult:
    """
    Memilih kandidat access point menggunakan
    strategi Greedy Set Cover.

    Pada setiap iterasi, dipilih kandidat yang
    mencakup pengguna belum terlayani paling banyak.

    Jika terdapat nilai yang sama, kandidat dengan
    ID terkecil secara leksikografis dipilih.
    """
    uncovered = set(all_users)
    selected: list[str] = []
    steps: list[GreedyStep] = []

    available_candidates = set(coverage_map)

    iteration = 1

    while uncovered:
        scored_candidates: list[tuple[int, str, set[str]]] = []

        for candidate_id in available_candidates:
            newly_covered = coverage_map[candidate_id] & uncovered

            scored_candidates.append(
                (
                    len(newly_covered),
                    candidate_id,
                    newly_covered,
                )
            )

        if not scored_candidates:
            break

        best_gain = max(score[0] for score in scored_candidates)

        # Tidak ada kandidat yang memberikan
        # cakupan tambahan.
        if best_gain == 0:
            break

        best_candidate, newly_covered = min(
            (
                (candidate_id, covered)
                for gain, candidate_id, covered in scored_candidates
                if gain == best_gain
            ),
            key=lambda item: item[0],
        )

        selected.append(best_candidate)
        uncovered -= newly_covered

        available_candidates.remove(best_candidate)

        steps.append(
            GreedyStep(
                iteration=iteration,
                selected_candidate=best_candidate,
                newly_covered=tuple(sorted(newly_covered)),
                remaining_uncovered=tuple(sorted(uncovered)),
            )
        )

        iteration += 1

    covered = all_users - uncovered

    return GreedyResult(
        selected_candidates=tuple(selected),
        covered_users=tuple(sorted(covered)),
        uncovered_users=tuple(sorted(uncovered)),
        steps=tuple(steps),
    )

@dataclass(frozen=True)
class BruteForceResult:
    selected_candidates: tuple[str, ...]
    covered_users: tuple[str, ...]
    uncovered_users: tuple[str, ...]
    checked_combinations: int

    @property
    def is_complete(self) -> bool:
        return not self.uncovered_users


def brute_force_set_cover(
    all_users: set[str],
    coverage_map: Mapping[str, set[str]],
) -> BruteForceResult:
    """
    Mencari solusi optimal Set Cover dengan mencoba seluruh
    kombinasi kandidat dari ukuran terkecil.

    Metode ini menjamin solusi dengan jumlah kandidat minimum,
    tetapi kompleksitasnya eksponensial terhadap jumlah kandidat.
    """
    candidate_ids = sorted(coverage_map)
    checked = 0

    best_partial: tuple[str, ...] = ()
    best_covered: set[str] = set()

    for size in range(1, len(candidate_ids) + 1):
        for subset in combinations(candidate_ids, size):
            checked += 1

            covered: set[str] = set()
            for candidate_id in subset:
                covered |= coverage_map[candidate_id]

            if len(covered) > len(best_covered):
                best_partial = subset
                best_covered = covered

            if all_users <= covered:
                return BruteForceResult(
                    selected_candidates=tuple(subset),
                    covered_users=tuple(sorted(covered)),
                    uncovered_users=tuple(),
                    checked_combinations=checked,
                )

    uncovered = all_users - best_covered

    return BruteForceResult(
        selected_candidates=best_partial,
        covered_users=tuple(sorted(best_covered)),
        uncovered_users=tuple(sorted(uncovered)),
        checked_combinations=checked,
    )