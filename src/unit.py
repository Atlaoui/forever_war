import pygame
from dataclasses import dataclass
from typing import Optional
from src.constants import (
    UNIT_TYPES, LANE_WIDTH,
    HEALTH_BAR_BG, HEALTH_BAR_PLAYER, HEALTH_BAR_ENEMY,
    PLAYER_BASE_Y, ENEMY_BASE_Y
)


@dataclass
class UnitType:
    name: str
    hp: int
    damage: int
    speed: int
    range: int
    cost: int
    attack_cooldown: float
    shape: str
    color: tuple
    size: int

    @classmethod
    def from_name(cls, unit_name: str) -> "UnitType":
        data = UNIT_TYPES[unit_name]
        return cls(
            name=data["name"],
            hp=data["hp"],
            damage=data["damage"],
            speed=data["speed"],
            range=data["range"],
            cost=data["cost"],
            attack_cooldown=data["attack_cooldown"],
            shape=data["shape"],
            color=data["color"],
            size=data["size"],
        )


class Unit:
    def __init__(self, unit_type: UnitType, lane: int, is_player: bool):
        self.unit_type = unit_type
        self.lane = lane
        self.is_player = is_player

        # Position (vertical orientation: x is lane-based, y moves)
        self.x = lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = PLAYER_BASE_Y if is_player else ENEMY_BASE_Y

        # Stats (copy from type so they can be modified)
        self.max_hp = unit_type.hp
        self.hp = unit_type.hp
        self.damage = unit_type.damage
        self.speed = unit_type.speed
        self.range = unit_type.range

        # Direction: -1 for player (moving up), +1 for enemy (moving down)
        self.direction = -1 if is_player else 1

        # Combat state
        self.target: Optional["Unit"] = None
        self.attack_cooldown = 0.0
        self.is_attacking = False

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def find_target(self, enemies: list["Unit"]) -> Optional["Unit"]:
        """Find the nearest enemy unit in range."""
        nearest_enemy = None
        nearest_distance = float('inf')

        for enemy in enemies:
            if not enemy.is_alive or enemy.lane != self.lane:
                continue

            distance = abs(self.y - enemy.y)
            if distance <= self.range and distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy

        return nearest_enemy

    def update(self, dt: float, enemies: list["Unit"]):
        """Update unit state each frame."""
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Find target
        self.target = self.find_target(enemies)

        if self.target:
            # Stop and attack
            self.is_attacking = True
            if self.attack_cooldown <= 0:
                self.attack(self.target)
        else:
            # Move forward (vertically)
            self.is_attacking = False
            self.y += self.direction * self.speed * dt

    def attack(self, target: "Unit"):
        """Attack the target unit."""
        target.take_damage(self.damage)
        self.attack_cooldown = self.unit_type.attack_cooldown

    def take_damage(self, amount: int):
        """Receive damage."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def has_reached_enemy_base(self) -> bool:
        """Check if unit has reached the enemy's base."""
        if self.is_player:
            return self.y <= ENEMY_BASE_Y
        else:
            return self.y >= PLAYER_BASE_Y

    def render(self, screen: pygame.Surface):
        """Render the unit on screen."""
        size = self.unit_type.size
        half_size = size // 2

        # Draw unit shape
        if self.unit_type.shape == "rect":
            rect = pygame.Rect(
                self.x - half_size,
                self.y - half_size,
                size,
                size
            )
            pygame.draw.rect(screen, self.unit_type.color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        else:  # circle
            pygame.draw.circle(screen, self.unit_type.color, (int(self.x), int(self.y)), half_size)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), half_size, 2)

        # Draw health bar
        health_bar_width = size + 10
        health_bar_height = 6
        health_bar_x = self.x - health_bar_width // 2
        health_bar_y = self.y - half_size - 12

        # Background
        pygame.draw.rect(screen, HEALTH_BAR_BG,
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Health fill
        health_ratio = self.hp / self.max_hp
        health_color = HEALTH_BAR_PLAYER if self.is_player else HEALTH_BAR_ENEMY
        pygame.draw.rect(screen, health_color,
                        (health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height))

        # Border
        pygame.draw.rect(screen, (200, 200, 200),
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 1)
