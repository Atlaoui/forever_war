import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT,
    MAX_MANA, MANA_COLOR, MANA_BG_COLOR, WHITE, BLACK, GRAY,
    DARK_GRAY, CARD_Y
)
from src.card import Deck


class UI:
    def __init__(self):
        self.deck = Deck(CARD_Y)
        self.font_large = None
        self.font_medium = None
        self.font_small = None

    def init_fonts(self):
        """Initialize fonts (must be called after pygame.init())."""
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def render_header(self, screen: pygame.Surface, enemy_mana: float):
        """Render the header with game title and enemy mana."""
        # Background
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, HEADER_HEIGHT)
        pygame.draw.rect(screen, DARK_GRAY, header_rect)

        # Title
        title = self.font_large.render("FOREVER WAR", True, WHITE)
        screen.blit(title, (20, 10))

        # Enemy mana indicator
        enemy_mana_text = self.font_small.render(f"Enemy Mana: {int(enemy_mana)}/{MAX_MANA}",
                                                  True, (200, 100, 100))
        screen.blit(enemy_mana_text, (SCREEN_WIDTH - 180, 15))

    def render_footer(self, screen: pygame.Surface, player_mana: float, selected_card):
        """Render the footer with mana bar and cards."""
        # Background
        footer_rect = pygame.Rect(0, SCREEN_HEIGHT - FOOTER_HEIGHT, SCREEN_WIDTH, FOOTER_HEIGHT)
        pygame.draw.rect(screen, DARK_GRAY, footer_rect)

        # Mana bar
        mana_bar_x = 20
        mana_bar_y = SCREEN_HEIGHT - FOOTER_HEIGHT + 15
        mana_bar_width = 300
        mana_bar_height = 25

        # Background
        pygame.draw.rect(screen, MANA_BG_COLOR,
                        (mana_bar_x, mana_bar_y, mana_bar_width, mana_bar_height),
                        border_radius=5)

        # Fill
        fill_width = (player_mana / MAX_MANA) * mana_bar_width
        pygame.draw.rect(screen, MANA_COLOR,
                        (mana_bar_x, mana_bar_y, fill_width, mana_bar_height),
                        border_radius=5)

        # Border
        pygame.draw.rect(screen, WHITE,
                        (mana_bar_x, mana_bar_y, mana_bar_width, mana_bar_height),
                        2, border_radius=5)

        # Mana text
        mana_text = self.font_medium.render(f"Mana: {int(player_mana)}/{MAX_MANA}", True, WHITE)
        screen.blit(mana_text, (mana_bar_x + mana_bar_width + 15, mana_bar_y))

        # Render deck
        self.deck.render(screen, self.font_small, player_mana)

        # Instructions
        if selected_card:
            instruction = f"Click a lane to deploy {selected_card.unit_data['name']}"
        else:
            instruction = "Click a card to select, then click a lane to deploy"
        instruction_text = self.font_small.render(instruction, True, GRAY)
        instruction_rect = instruction_text.get_rect(
            centerx=SCREEN_WIDTH // 2,
            bottom=SCREEN_HEIGHT - 10
        )
        screen.blit(instruction_text, instruction_rect)

    def render_game_over(self, screen: pygame.Surface, player_won: bool):
        """Render game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))

        # Result text
        if player_won:
            result_text = "VICTORY!"
            color = (0, 255, 0)
        else:
            result_text = "DEFEAT"
            color = (255, 0, 0)

        result_surface = self.font_large.render(result_text, True, color)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(result_surface, result_rect)

        # Restart instruction
        restart_text = self.font_medium.render("Press SPACE to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(restart_text, restart_rect)

    def handle_click(self, pos: tuple[int, int], player_mana: float):
        """Handle click on UI elements. Returns selected card or None."""
        # Check if click is in footer area (cards)
        if pos[1] >= SCREEN_HEIGHT - FOOTER_HEIGHT:
            return self.deck.handle_click(pos, player_mana)
        return None
