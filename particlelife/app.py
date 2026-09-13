from __future__ import annotations

import pygame

from .config import SimulationConfig
from .render import draw_force_matrix, draw_particles
from .simulation import Simulation


def run(config: SimulationConfig | None = None) -> None:
    config = config or SimulationConfig()
    pygame.init()
    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption("Particle Life Simulation")
    font = pygame.font.Font(None, 14)
    clock = pygame.time.Clock()
    simulation = Simulation(config)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        simulation.step()
        screen.fill(config.background_color)
        draw_force_matrix(screen, font, config)
        draw_particles(screen, simulation.particles)
        pygame.display.flip()
        clock.tick(config.fps)

    pygame.quit()
