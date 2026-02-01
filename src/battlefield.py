import pygame
from src.constants import (
    SCREEN_WIDTH, HEADER_HEIGHT, LANE_WIDTH,
    LANE_COLORS, LANE_DIVIDER_COLOR,
    PLAYER_BASE_Y, ENEMY_BASE_Y, BATTLEFIELD_HEIGHT
)
from src.unit import Unit


class Battlefield:
    def __init__(self):
        self.num_lanes = 3
        self.lane_rects: list[pygame.Rect] = []

        # Create vertical lane rectangles
        for i in range(self.num_lanes):
            lane_rect = pygame.Rect(
                i * LANE_WIDTH,
                HEADER_HEIGHT,
                LANE_WIDTH,
                BATTLEFIELD_HEIGHT
            )
            self.lane_rects.append(lane_rect)

    def get_lane_from_x(self, x: int) -> int | None:
        """Get lane index from x coordinate, or None if outside battlefield."""
        for i, rect in enumerate(self.lane_rects):
            if rect.collidepoint(x, HEADER_HEIGHT + BATTLEFIELD_HEIGHT // 2):
                return i
        return None

    def is_in_battlefield(self, pos: tuple[int, int]) -> bool:
        """Check if position is within the battlefield area."""
        x, y = pos
        return (HEADER_HEIGHT <= y < HEADER_HEIGHT + BATTLEFIELD_HEIGHT)

    def render(self, screen: pygame.Surface):
        """Render the battlefield."""
        # Draw lanes
        for i, rect in enumerate(self.lane_rects):
            pygame.draw.rect(screen, LANE_COLORS[i], rect)

            # Draw lane dividers (vertical lines)
            if i < self.num_lanes - 1:
                divider_x = rect.right
                pygame.draw.line(
                    screen,
                    LANE_DIVIDER_COLOR,
                    (divider_x, HEADER_HEIGHT),
                    (divider_x, HEADER_HEIGHT + BATTLEFIELD_HEIGHT),
                    2
                )

        # Draw base zones
        # Enemy base (top)
        enemy_base_rect = pygame.Rect(
            0, HEADER_HEIGHT,
            SCREEN_WIDTH, ENEMY_BASE_Y - HEADER_HEIGHT + 20
        )
        pygame.draw.rect(screen, (50, 30, 30), enemy_base_rect)
        pygame.draw.line(
            screen,
            (150, 0, 0),
            (0, ENEMY_BASE_Y + 20),
            (SCREEN_WIDTH, ENEMY_BASE_Y + 20),
            3
        )

        # Player base (bottom)
        player_base_rect = pygame.Rect(
            0, PLAYER_BASE_Y - 20,
            SCREEN_WIDTH, HEADER_HEIGHT + BATTLEFIELD_HEIGHT - PLAYER_BASE_Y + 20
        )
        pygame.draw.rect(screen, (30, 50, 30), player_base_rect)
        pygame.draw.line(
            screen,
            (0, 150, 0),
            (0, PLAYER_BASE_Y - 20),
            (SCREEN_WIDTH, PLAYER_BASE_Y - 20),
            3
        )

    def render_units(self, screen: pygame.Surface, player_units: list[Unit], enemy_units: list[Unit]):
        """Render all units on the battlefield."""
        for unit in player_units:
            if unit.is_alive:
                unit.render(screen)

        for unit in enemy_units:
            if unit.is_alive:
                unit.render(screen)
