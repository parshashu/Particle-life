from __future__ import annotations

import pygame

from .config import SimulationConfig
from .particle import Particle


def draw_particles(screen: pygame.Surface, particles: list[Particle]) -> None:
    for particle in particles:
        pygame.draw.circle(
            screen,
            particle.color,
            (int(particle.x), int(particle.y)),
            particle.radius,
        )


def draw_force_matrix(
    screen: pygame.Surface,
    font: pygame.font.Font,
    config: SimulationConfig,
    matrix_width: int = 150,
    matrix_height: int = 150,
    x_offset: int = 10,
    y_offset: int = 10,
) -> None:
    colors = config.particle_colors
    matrix_size = len(colors)
    cell_width = matrix_width // (matrix_size + 1)
    cell_height = matrix_height // (matrix_size + 1)
    circle_radius = 10

    title = font.render("Force Matrix", True, (255, 255, 255))
    screen.blit(title, (x_offset, y_offset))

    for i, color in enumerate(colors, start=1):
        col_center = (x_offset + i * cell_width + cell_width // 2, y_offset + 20 + cell_height // 2)
        row_center = (x_offset + cell_width // 2, y_offset + 20 + i * cell_height + cell_height // 2)
        pygame.draw.circle(screen, color, col_center, circle_radius)
        pygame.draw.circle(screen, (255, 255, 255), col_center, circle_radius, 1)
        pygame.draw.circle(screen, color, row_center, circle_radius)
        pygame.draw.circle(screen, (255, 255, 255), row_center, circle_radius, 1)

    for i, color1 in enumerate(colors):
        for j, color2 in enumerate(colors):
            force = config.force_matrix[color1][color2]
            cell = pygame.Rect(
                x_offset + (j + 1) * cell_width,
                y_offset + 20 + (i + 1) * cell_height,
                cell_width,
                cell_height,
            )
            pygame.draw.rect(screen, (255, 255, 255), cell, 1)
            text = font.render(f"{force:.2f}", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=cell.center))
