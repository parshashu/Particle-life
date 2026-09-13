from __future__ import annotations

import math

from .config import SimulationConfig
from .particle import Particle


def pairwise_force(distance: float, max_force: float, config: SimulationConfig) -> float:
    if distance < config.min_distance:
        return -config.repulsive_force * (1 - distance / config.min_distance)

    mid = (config.max_distance + config.min_distance) / 2
    span = config.max_distance - config.min_distance
    if distance < mid:
        return -2 * max_force * (distance - config.min_distance) / span
    if distance < config.max_distance:
        return 2 * max_force * (distance - config.max_distance) / span
    return 0.0


def apply_pair_forces(particle: Particle, other: Particle, config: SimulationConfig) -> None:
    dx, dy = particle.wrapped_offset(other, config)
    distance = math.hypot(dx, dy)
    if distance == 0:
        return

    force1 = pairwise_force(distance, config.force_matrix[particle.color][other.color], config)
    force2 = pairwise_force(distance, config.force_matrix[other.color][particle.color], config)

    if force1:
        particle.apply_force(force1 * dx / distance, force1 * dy / distance)
    if force2:
        other.apply_force(-force2 * dx / distance, -force2 * dy / distance)
