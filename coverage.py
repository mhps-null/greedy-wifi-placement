from __future__ import annotations

from math import hypot
from typing import Mapping


Point = tuple[float, float]


def euclidean_distance(
    first: Point,
    second: Point,
) -> float:
    """
    Menghitung jarak Euclidean antara dua titik.
    """
    return hypot(
        first[0] - second[0],
        first[1] - second[1],
    )


def build_coverage_map(
    users: Mapping[str, Point],
    candidates: Mapping[str, Point],
    radius: float,
) -> dict[str, set[str]]:
    """
    Membentuk himpunan pengguna yang dapat dicakup
    oleh setiap kandidat access point.

    Pengguna dianggap tercakup ketika jarak
    Euclidean antara pengguna dan kandidat AP
    lebih kecil atau sama dengan radius.
    """
    if radius <= 0:
        raise ValueError("Radius harus lebih besar dari 0.")

    coverage_map: dict[str, set[str]] = {}

    for (
        candidate_id,
        candidate_position,
    ) in candidates.items():
        covered_users = {
            user_id
            for user_id, user_position in users.items()
            if euclidean_distance(
                candidate_position,
                user_position,
            )
            <= radius
        }

        coverage_map[candidate_id] = covered_users

    return coverage_map
