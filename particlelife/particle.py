from __future__ import annotations

from typing import Tuple

from .config import Color, SimulationConfig


class Particle:
    def __init__(self, x: float, y: float, radius: int, color: Color) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = 0.0
        self.vy = 0.0

    def move(self, config: SimulationConfig) -> None:
        self.vx *= config.friction
        self.vy *= config.friction
        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.x += config.width
        elif self.x > config.width:
            self.x -= config.width
        if self.y < 0:
            self.y += config.height
        elif self.y > config.height:
            self.y -= config.height

    def apply_force(self, fx: float, fy: float) -> None:
        self.vx += fx
        self.vy += fy

    def wrapped_offset(self, other: "Particle", config: SimulationConfig) -> Tuple[float, float]:
        dx = other.x - self.x
        dy = other.y - self.y
        half_w = config.width / 2
        half_h = config.height / 2
        if abs(dx) > half_w:
            dx = -1.0 if dx > 0 else 1.0
            dx *= config.width - abs(other.x - self.x)
        if abs(dy) > half_h:
            dy = -1.0 if dy > 0 else 1.0
            dy *= config.height - abs(other.y - self.y)
        return dx, dy
