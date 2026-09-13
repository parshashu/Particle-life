from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

from .config import SimulationConfig
from .particle import Particle

Cell = Tuple[int, int]
Grid = Dict[Cell, List[Particle]]


class SpatialGrid:
    def __init__(self, particles: Iterable[Particle], config: SimulationConfig) -> None:
        self.cell_size = max(int(config.max_distance // 2), 1)
        self.grid_size_x = (config.width // self.cell_size) + 1
        self.grid_size_y = (config.height // self.cell_size) + 1
        self.grid: Grid = defaultdict(list)
        for particle in particles:
            cell = (int(particle.x // self.cell_size), int(particle.y // self.cell_size))
            self.grid[cell].append(particle)

    def neighbors(self, cell: Cell) -> List[Cell]:
        # Keep the original wrap using a single period so force pairing stays unchanged.
        period = max(self.grid_size_x, self.grid_size_y)
        x, y = cell
        return [
            ((x - 1) % period, (y - 1) % period),
            ((x - 1) % period, y % period),
            ((x - 1) % period, (y + 1) % period),
            (x % period, (y - 1) % period),
            (x % period, (y + 1) % period),
            ((x + 1) % period, (y - 1) % period),
            ((x + 1) % period, y % period),
            ((x + 1) % period, (y + 1) % period),
        ]
