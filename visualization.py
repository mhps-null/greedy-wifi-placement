from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Rectangle


Point = tuple[float, float]
Wall = tuple[Point, Point]
Room = dict[str, object]


def _draw_room(
    ax,
    x: float,
    y: float,
    width: float,
    height: float,
    name: str,
    facecolor: str,
) -> None:
    rect = Rectangle(
        (x, y),
        width,
        height,
        facecolor=facecolor,
        edgecolor="#5f6b7a",
        linewidth=1.5,
        alpha=0.35,
        zorder=0,
    )
    ax.add_patch(rect)

    ax.text(
        x + width / 2,
        y + height - 0.18,
        name,
        ha="center",
        va="top",
        fontsize=9,
        fontweight="bold",
        color="#2d3640",
        zorder=6,
    )


def _draw_user_icon(
    ax,
    x: float,
    y: float,
    label: str,
    status: str = "neutral",
) -> None:
    """
    status:
    - neutral   : untuk gambar awal
    - covered   : pengguna tercakup
    - uncovered : pengguna belum tercakup
    """
    if status == "covered":
        color = "#1f7a1f"
        halo = "#b9e7b9"
    elif status == "uncovered":
        color = "#b22222"
        halo = "#f5b6b6"
    else:
        color = "#1f4e79"
        halo = "#d6e7f7"

    ax.add_patch(
        Circle(
            (x, y),
            0.24,
            facecolor=halo,
            edgecolor="none",
            alpha=0.95,
            zorder=3,
        )
    )

    ax.add_patch(
        Circle(
            (x, y + 0.08),
            0.07,
            facecolor=color,
            edgecolor="white",
            linewidth=0.8,
            zorder=4,
        )
    )

    ax.plot(
        [x, x],
        [y - 0.09, y + 0.01],
        color=color,
        linewidth=2.1,
        zorder=4,
    )

    ax.plot(
        [x - 0.08, x + 0.08],
        [y - 0.02, y - 0.02],
        color=color,
        linewidth=2.1,
        zorder=4,
    )

    ax.plot(
        [x, x - 0.07],
        [y - 0.09, y - 0.18],
        color=color,
        linewidth=2.1,
        zorder=4,
    )
    ax.plot(
        [x, x + 0.07],
        [y - 0.09, y - 0.18],
        color=color,
        linewidth=2.1,
        zorder=4,
    )

    ax.text(
        x + 0.13,
        y + 0.13,
        label,
        fontsize=8,
        fontweight="bold",
        color="#1f1f1f",
        zorder=6,
    )


def _draw_access_point_icon(
    ax,
    x: float,
    y: float,
    label: str,
    selected: bool = False,
) -> None:
    """
    Menggambar ikon access point yang lebih jelas:
    - badan perangkat/router
    - dua antena
    - gelombang Wi-Fi
    """
    if selected:
        device_face = "#ffd27a"
        device_edge = "#a86400"
        wave_color = "#8a4f00"
        halo_color = "#fff0c9"
        led_color = "#a86400"
    else:
        device_face = "#dbe7f5"
        device_edge = "#415a77"
        wave_color = "#2d4f73"
        halo_color = "#eef4fb"
        led_color = "#415a77"

    # Halo background
    ax.add_patch(
        Circle(
            (x, y),
            0.34,
            facecolor=halo_color,
            edgecolor="none",
            alpha=0.95,
            zorder=2,
        )
    )

    # Badan router/access point
    body_width = 0.34
    body_height = 0.12
    body_x = x - body_width / 2
    body_y = y - 0.12

    ax.add_patch(
        FancyBboxPatch(
            (body_x, body_y),
            body_width,
            body_height,
            boxstyle="round,pad=0.02,rounding_size=0.035",
            facecolor=device_face,
            edgecolor=device_edge,
            linewidth=1.5,
            zorder=5,
        )
    )

    # Antena kiri dan kanan
    ax.plot(
        [x - 0.11, x - 0.15],
        [y - 0.01, y + 0.16],
        color=device_edge,
        linewidth=2.0,
        zorder=5,
    )
    ax.plot(
        [x + 0.11, x + 0.15],
        [y - 0.01, y + 0.16],
        color=device_edge,
        linewidth=2.0,
        zorder=5,
    )

    # LED indikator
    ax.add_patch(
        Circle(
            (x, body_y + 0.05),
            0.014,
            facecolor=led_color,
            edgecolor=led_color,
            zorder=6,
        )
    )

    # Kaki kecil / garis bawah perangkat
    ax.plot(
        [x - 0.08, x + 0.08],
        [body_y - 0.01, body_y - 0.01],
        color=device_edge,
        linewidth=1.2,
        zorder=5,
    )

    # Gelombang Wi-Fi di atas perangkat
    for w in (0.20, 0.32, 0.45):
        ax.add_patch(
            Arc(
                (x, y + 0.02),
                w,
                w * 0.80,
                angle=0,
                theta1=35,
                theta2=145,
                linewidth=1.8,
                color=wave_color,
                zorder=6,
            )
        )

    # Titik sinyal
    ax.add_patch(
        Circle(
            (x, y + 0.01),
            0.015,
            facecolor=wave_color,
            edgecolor=wave_color,
            zorder=6,
        )
    )

    if selected:
        ax.text(
            x,
            y + 0.34,
            "Terpilih",
            fontsize=7,
            fontweight="bold",
            ha="center",
            va="center",
            color="#8a4f00",
            zorder=7,
        )

    ax.text(
        x + 0.13,
        y - 0.26,
        label,
        fontsize=8,
        fontweight="bold",
        color="#1f1f1f",
        zorder=7,
    )


def _draw_coverage_circle(
    ax,
    x: float,
    y: float,
    radius: float,
) -> None:
    ax.add_patch(
        Circle(
            (x, y),
            radius,
            facecolor="#7cc6fe",
            edgecolor="#2d89c6",
            linewidth=1.5,
            linestyle="--",
            alpha=0.16,
            zorder=1,
        )
    )


def draw_floor_plan(
    *,
    width: float,
    height: float,
    users: Mapping[str, Point],
    candidates: Mapping[str, Point],
    walls: Iterable[Wall] = (),
    rooms: Iterable[Room] = (),
    selected_candidates: Iterable[str] = (),
    radius: float | None = None,
    covered_users: Iterable[str] = (),
    output_file: str | Path | None = None,
    title: str = "Denah Ruangan",
    show: bool = False,
) -> None:
    selected_set = set(selected_candidates)
    covered_list = list(covered_users)
    covered_set = set(covered_list)
    coverage_mode = len(covered_list) > 0

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.set_title(
        title,
        fontsize=15,
        fontweight="bold",
        pad=14,
    )

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect("equal", adjustable="box")

    ax.set_xlabel("Koordinat X", fontsize=10, labelpad=10)
    ax.set_ylabel("Koordinat Y", fontsize=10, labelpad=10)

    ax.set_xticks(range(0, int(width) + 1))
    ax.set_yticks(range(0, int(height) + 1))

    ax.grid(True, linewidth=0.5, alpha=0.35, linestyle=":")
    ax.set_facecolor("#fafafa")

    ax.add_patch(
        Rectangle(
            (0, 0),
            width,
            height,
            fill=False,
            edgecolor="#1f1f1f",
            linewidth=2.2,
            zorder=2,
        )
    )

    room_palette = [
        "#cfe8ff",
        "#dff7df",
        "#ffe6cc",
        "#efe1ff",
        "#fff3bf",
        "#ffd6e7",
    ]

    # Ruangan
    for index, room in enumerate(rooms):
        x = float(room["x"])
        y = float(room["y"])
        room_width = float(room["width"])
        room_height = float(room["height"])
        name = str(room["name"])

        _draw_room(
            ax,
            x=x,
            y=y,
            width=room_width,
            height=room_height,
            name=name,
            facecolor=room_palette[index % len(room_palette)],
        )

    # Dinding
    for (x1, y1), (x2, y2) in walls:
        ax.plot(
            [x1, x2],
            [y1, y2],
            color="#333333",
            linewidth=3.0,
            solid_capstyle="round",
            zorder=3,
        )

    # Cakupan access point terpilih
    if radius is not None:
        for candidate_id in selected_set:
            if candidate_id in candidates:
                x, y = candidates[candidate_id]
                _draw_coverage_circle(ax, x, y, radius)

    # Kandidat access point
    for candidate_id, (x, y) in candidates.items():
        _draw_access_point_icon(
            ax,
            x=x,
            y=y,
            label=candidate_id,
            selected=(candidate_id in selected_set),
        )

    # Pengguna
    for user_id, (x, y) in users.items():
        if not coverage_mode:
            status = "neutral"
        elif user_id in covered_set:
            status = "covered"
        else:
            status = "uncovered"

        _draw_user_icon(
            ax,
            x=x,
            y=y,
            label=user_id,
            status=status,
        )

    total_users = len(users)
    total_candidates = len(candidates)
    total_selected = len(selected_set)
    total_covered = len(covered_set) if coverage_mode else 0
    coverage_percentage = (
        (total_covered / total_users) * 100
        if coverage_mode and total_users > 0
        else 0.0
    )

    if coverage_mode:
        summary_text = (
            f"Total Pengguna            : {total_users}\n"
            f"Kandidat Access Point     : {total_candidates}\n"
            f"Access Point Terpilih     : {total_selected}\n"
            f"Pengguna Tercakup         : {total_covered}/{total_users}\n"
            f"Persentase Cakupan        : {coverage_percentage:.2f}%"
        )
    else:
        summary_text = (
            f"Total Pengguna            : {total_users}\n"
            f"Kandidat Access Point     : {total_candidates}\n"
            f"Access Point Terpilih     : {total_selected}\n"
            f"Status                    : Denah awal"
        )

    ax.text(
        0.015,
        0.985,
        summary_text,
        transform=ax.transAxes,
        fontsize=9,
        va="top",
        ha="left",
        bbox=dict(
            boxstyle="round,pad=0.45",
            facecolor="white",
            edgecolor="#666666",
            alpha=0.35,
        ),
        zorder=10,
    )

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#1f4e79",
            markeredgecolor="#1f4e79",
            markersize=8,
            label="Pengguna",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor="#dbe7f5",
            markeredgecolor="#415a77",
            markersize=8,
            label="Kandidat Access Point",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor="#ffd27a",
            markeredgecolor="#a86400",
            markersize=8,
            label="Access Point Terpilih",
        ),
        Line2D(
            [0],
            [0],
            linestyle="--",
            color="#2d89c6",
            linewidth=1.5,
            label="Radius Cakupan Access Point",
        ),
    ]

    if coverage_mode:
        legend_elements.extend(
            [
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor="#1f7a1f",
                    markeredgecolor="#1f7a1f",
                    markersize=8,
                    label="Pengguna Tercakup",
                ),
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor="#b22222",
                    markeredgecolor="#b22222",
                    markersize=8,
                    label="Pengguna Belum Tercakup",
                ),
            ]
        )

    ax.legend(
        handles=legend_elements,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=3,
        frameon=True,
        fontsize=9,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.subplots_adjust(
        left=0.07,
        right=0.98,
        top=0.88,
        bottom=0.20,
    )

    if output_file is not None:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            output_path,
            dpi=220,
            bbox_inches="tight",
        )

    if show:
        plt.show()

    plt.close(fig)
