#!/usr/bin/env python3
"""
Forever War - A simplified Clash Royale-like 2D game

Controls:
- Click a card at the bottom to select it
- Click a lane on the battlefield to deploy the selected unit
- ESC to quit
- SPACE to restart after game over
"""

from src.game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
