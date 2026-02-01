import pygame
from src.constants import (
    UNIT_TYPES, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, SCREEN_WIDTH,
    CARD_BG_COLOR, CARD_SELECTED_COLOR, CARD_DISABLED_COLOR,
    WHITE, MANA_COLOR
)


class Card:
    def __init__(self, unit_name: str, x: int, y: int):
        self.unit_name = unit_name
        self.unit_data = UNIT_TYPES[unit_name]
        self.x = x
        self.y = y
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.selected = False

    @property
    def cost(self) -> int:
        return self.unit_data["cost"]

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        """Check if the card was clicked."""
        return self.rect.collidepoint(pos)

    def render(self, screen: pygame.Surface, font: pygame.font.Font,
               current_mana: float, is_selected: bool):
        """Render the card."""
        can_afford = current_mana >= self.cost

        # Determine background color
        if is_selected:
            bg_color = CARD_SELECTED_COLOR
        elif not can_afford:
            bg_color = CARD_DISABLED_COLOR
        else:
            bg_color = CARD_BG_COLOR

        # Draw card background
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)

        # Draw border
        border_color = WHITE if is_selected else (100, 100, 100)
        border_width = 3 if is_selected else 1
        pygame.draw.rect(screen, border_color, self.rect, border_width, border_radius=8)

        # Draw unit icon (small preview)
        icon_size = 20
        icon_x = self.x + self.width // 2
        icon_y = self.y + 25

        unit_color = self.unit_data["color"] if can_afford else (80, 80, 80)

        if self.unit_data["shape"] == "rect":
            icon_rect = pygame.Rect(
                icon_x - icon_size // 2,
                icon_y - icon_size // 2,
                icon_size,
                icon_size
            )
            pygame.draw.rect(screen, unit_color, icon_rect)
        else:
            pygame.draw.circle(screen, unit_color, (icon_x, icon_y), icon_size // 2)

        # Draw unit name
        name_color = WHITE if can_afford else (100, 100, 100)
        name_surface = font.render(self.unit_data["name"], True, name_color)
        name_rect = name_surface.get_rect(centerx=self.x + self.width // 2,
                                          top=self.y + 45)
        screen.blit(name_surface, name_rect)

        # Draw mana cost
        cost_color = MANA_COLOR if can_afford else (60, 60, 100)
        cost_surface = font.render(f"{self.cost}", True, cost_color)
        cost_rect = cost_surface.get_rect(centerx=self.x + self.width // 2,
                                          top=self.y + 62)
        screen.blit(cost_surface, cost_rect)


class Deck:
    def __init__(self, card_y: int):
        self.cards: list[Card] = []
        self.selected_card: Card | None = None

        # Create cards for all unit types
        unit_names = ["soldier", "tank", "archer", "knight", "assassin", "giant"]
        total_width = len(unit_names) * CARD_WIDTH + (len(unit_names) - 1) * CARD_SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2  # Center cards

        for i, unit_name in enumerate(unit_names):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            card = Card(unit_name, x, card_y)
            self.cards.append(card)

    def handle_click(self, pos: tuple[int, int], current_mana: float) -> Card | None:
        """Handle click on deck, return selected card or None."""
        for card in self.cards:
            if card.is_clicked(pos) and current_mana >= card.cost:
                if self.selected_card == card:
                    # Deselect if clicking same card
                    self.selected_card = None
                else:
                    self.selected_card = card
                return self.selected_card
        return None

    def deselect(self):
        """Deselect any selected card."""
        self.selected_card = None

    def render(self, screen: pygame.Surface, font: pygame.font.Font, current_mana: float):
        """Render all cards in the deck."""
        for card in self.cards:
            is_selected = card == self.selected_card
            card.render(screen, font, current_mana, is_selected)
