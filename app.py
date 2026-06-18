from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter

from coverage import build_coverage_map
from greedy import GreedyResult, greedy_set_cover
from visualization import draw_floor_plan


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SCENARIO = BASE_DIR / "scenarios" / "denah.json"
DEFAULT_OUTPUT_DIR = BASE_DIR / "output"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Simulasi penempatan access point Wi-Fi menggunakan "
            "algoritma Greedy Set Cover."
        )
    )

    parser.add_argument(
        "--scenario",
        type=Path,
        default=DEFAULT_SCENARIO,
        help="Path ke berkas skenario JSON.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Direktori untuk menyimpan gambar hasil.",
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Tampilkan visualisasi selain menyimpannya sebagai PNG.",
    )

    return parser.parse_args()


def load_scenario(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Berkas skenario tidak ditemukan: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    required_keys = {
        "width",
        "height",
        "radius",
        "users",
        "candidates",
    }

    missing = required_keys - data.keys()

    if missing:
        raise ValueError(
            "Skenario tidak lengkap. Kunci yang hilang: " + ", ".join(sorted(missing))
        )

    return data


def to_point_map(
    raw_points: dict[str, list[float]],
) -> dict[str, tuple[float, float]]:
    return {
        point_id: (
            float(coordinates[0]),
            float(coordinates[1]),
        )
        for point_id, coordinates in raw_points.items()
    }


def print_result(
    result: GreedyResult,
    elapsed_ms: float,
    total_users: int,
) -> None:
    print("\n=== Log Iterasi Greedy Set Cover ===")

    if not result.steps:
        print("Tidak ada kandidat AP yang dapat mencakup pengguna.")

    for step in result.steps:
        newly_covered = ", ".join(step.newly_covered) or "-"
        remaining = ", ".join(step.remaining_uncovered) or "tidak ada"

        print(
            f"Iterasi {step.iteration}: "
            f"pilih {step.selected_candidate}; "
            f"pengguna baru tercakup = {newly_covered}; "
            f"tersisa = {remaining}."
        )

    coverage_percentage = (
        len(result.covered_users) / total_users * 100 if total_users else 100.0
    )

    print("\n=== Ringkasan ===")

    print(f"AP terpilih       : {', '.join(result.selected_candidates) or '-'}")
    print(f"Jumlah AP         : {len(result.selected_candidates)}")
    print(f"Pengguna tercakup : {len(result.covered_users)}/{total_users}")
    print(f"Persentase        : {coverage_percentage:.2f}%")
    print(f"Jumlah iterasi    : {len(result.steps)}")
    print(f"Waktu eksekusi    : {elapsed_ms:.4f} ms")

    if result.uncovered_users:
        print("Pengguna belum tercakup: " + ", ".join(result.uncovered_users))


def main() -> None:
    args = parse_args()

    scenario = load_scenario(args.scenario)
    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    users = to_point_map(scenario["users"])
    candidates = to_point_map(scenario["candidates"])

    walls = [
        (
            (
                float(wall[0][0]),
                float(wall[0][1]),
            ),
            (
                float(wall[1][0]),
                float(wall[1][1]),
            ),
        )
        for wall in scenario.get("walls", [])
    ]

    rooms = scenario.get("rooms", [])

    width = float(scenario["width"])
    height = float(scenario["height"])
    radius = float(scenario["radius"])

    initial_output = args.output_dir / "denah.png"
    result_output = args.output_dir / "hasil.png"

    # Membuat gambar kondisi awal.
    draw_floor_plan(
        width=width,
        height=height,
        users=users,
        candidates=candidates,
        walls=walls,
        rooms=rooms,
        output_file=initial_output,
        title="Denah Awal Kandidat Access Point",
        show=False,
    )

    # Menghitung pengguna yang dicakup setiap AP.
    coverage_map = build_coverage_map(
        users,
        candidates,
        radius,
    )

    # Menjalankan algoritma dan mengukur waktunya.
    start = perf_counter()

    result = greedy_set_cover(
        set(users),
        coverage_map,
    )

    elapsed_ms = (perf_counter() - start) * 1000

    # Membuat gambar hasil pemilihan AP.
    draw_floor_plan(
        width=width,
        height=height,
        users=users,
        candidates=candidates,
        walls=walls,
        rooms=rooms,
        selected_candidates=(result.selected_candidates),
        covered_users=result.covered_users,
        radius=radius,
        output_file=result_output,
        title="Hasil Greedy Set Cover",
        show=args.show,
    )

    print_result(
        result,
        elapsed_ms,
        len(users),
    )

    print(f"\nGambar awal  : {initial_output}")
    print(f"Gambar hasil : {result_output}")


if __name__ == "__main__":
    main()
