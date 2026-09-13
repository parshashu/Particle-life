from __future__ import annotations

import random
from typing import List

from .config import SimulationConfig
from .forces import apply_pair_forces
from .particle import Particle
from .spatial import SpatialGrid


class Simulation:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.particles: List[Particle] = [
            Particle(
                random.randint(0, config.width),
                random.randint(0, config.height),
                config.particle_radius,
                random.choice(config.particle_colors),
            )
            for _ in range(config.num_particles)
        ]

    def step(self) -> None:
        for particle in self.particles:
            particle.move(self.config)
        self._apply_forces()

    def _apply_forces(self) -> None:
        grid = SpatialGrid(self.particles, self.config)
        for cell, cell_particles in grid.grid.items():
            for i, particle in enumerate(cell_particles):
                for other in cell_particles[i + 1 :]:
                    apply_pair_forces(particle, other, self.config)
                for neighbor in grid.neighbors(cell):
                    if neighbor not in grid.grid:
                        continue
                    for other in grid.grid[neighbor]:
                        apply_pair_forces(particle, other, self.config)
