import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
)
from src.player import Player
from src.ai import AI
from src.battlefield import Battlefield
from src.ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Forever War")
        self.clock = pygame.time.Clock()

        self.battlefield = Battlefield()
        self.ui = UI()
        self.ui.init_fonts()

        self.reset_game()

    def reset_game(self):
        """Reset the game state."""
        self.player = Player(is_human=True)
        self.enemy = AI()
        self.game_over = False
        self.player_won = False
        self.running = True

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos)

    def handle_click(self, pos: tuple[int, int]):
        """Handle mouse click."""
        if self.game_over:
            return

        # First check if clicking on cards
        card = self.ui.handle_click(pos, self.player.mana)
        if card is not None:
            return

        # Check if clicking on battlefield with a selected card
        selected = self.ui.deck.selected_card
        if selected and self.battlefield.is_in_battlefield(pos):
            lane = self.battlefield.get_lane_from_x(pos[0])
            if lane is not None:
                # Try to spawn unit
                if self.player.can_afford(selected.unit_name):
                    self.player.spawn_unit(selected.unit_name, lane)
                    self.ui.deck.deselect()
        else:
            # Clicking on battlefield without selected card - deselect
            if self.battlefield.is_in_battlefield(pos):
                self.ui.deck.deselect()

    def update(self, dt: float):
        """Update game state."""
        if self.game_over:
            return

        # Update player and enemy
        self.player.update(dt, self.enemy.units)
        self.enemy.update(dt, self.player.units)

        # Check win conditions
        if self.player.check_win_condition():
            self.game_over = True
            self.player_won = True
        elif self.enemy.check_win_condition():
            self.game_over = True
            self.player_won = False

    def render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(BLACK)

        # Render battlefield
        self.battlefield.render(self.screen)
        self.battlefield.render_units(self.screen, self.player.units, self.enemy.units)

        # Render UI
        self.ui.render_header(self.screen, self.enemy.mana)
        self.ui.render_footer(self.screen, self.player.mana, self.ui.deck.selected_card)

        # Render game over screen if needed
        if self.game_over:
            self.ui.render_game_over(self.screen, self.player_won)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()
