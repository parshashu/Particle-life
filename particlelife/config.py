from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

Color = Tuple[int, int, int]
ForceMatrix = Dict[Color, Dict[Color, float]]

YELLOW: Color = (255, 255, 0)
CYAN: Color = (0, 255, 255)
MAGENTA: Color = (255, 0, 255)
GREEN: Color = (0, 255, 0)
DEFAULT_COLORS: List[Color] = [YELLOW, CYAN, MAGENTA, GREEN]

# Hand-tuned matrix used for the cell-like clusters in media/cells.png
DEFAULT_FORCE_MATRIX: ForceMatrix = {
    YELLOW: {YELLOW: -0.1, CYAN: -0.05, MAGENTA: 0.0, GREEN: 0.0},
    CYAN: {YELLOW: 0.04, CYAN: -0.1, MAGENTA: -0.06, GREEN: 0.0},
    MAGENTA: {YELLOW: 0.0, CYAN: 0.05, MAGENTA: -0.1, GREEN: -0.07},
    GREEN: {YELLOW: 0.0, CYAN: 0.0, MAGENTA: 0.06, GREEN: -0.1},
}


def _copy_matrix(matrix: ForceMatrix) -> ForceMatrix:
    return {src: dict(targets) for src, targets in matrix.items()}


def random_force_matrix(
    colors: List[Color],
    max_random: float = 0.3,
    seed: Optional[int] = None,
) -> ForceMatrix:
    rng = random.Random(seed)
    return {
        src: {dst: rng.uniform(-max_random, max_random) for dst in colors}
        for src in colors
    }


@dataclass
class SimulationConfig:
    width: int = 1550
    height: int = 900
    background_color: Color = (11, 10, 34)
    particle_colors: List[Color] = field(default_factory=lambda: list(DEFAULT_COLORS))
    num_particles: int = 700
    particle_radius: int = 3
    min_distance: float = 15
    max_distance: float = 100
    friction: float = 0.8
    repulsive_force: float = 3.0
    fps: int = 60
    seed: Optional[int] = 4
    force_matrix: ForceMatrix = field(default_factory=lambda: _copy_matrix(DEFAULT_FORCE_MATRIX))

    def __post_init__(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)

    @classmethod
    def with_random_forces(
        cls,
        max_random: float = 0.3,
        seed: int = 4,
        **kwargs,
    ) -> "SimulationConfig":
        colors = kwargs.get("particle_colors", list(DEFAULT_COLORS))
        kwargs.setdefault("force_matrix", random_force_matrix(colors, max_random, seed))
        kwargs.setdefault("seed", seed)
        return cls(**kwargs)
