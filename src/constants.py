# Screen dimensions (vertical orientation)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (65, 105, 225)
YELLOW = (255, 215, 0)
PURPLE = (148, 0, 211)
ORANGE = (255, 140, 0)
CYAN = (0, 255, 255)
BROWN = (139, 69, 19)

# UI Colors
MANA_COLOR = (0, 150, 255)
MANA_BG_COLOR = (30, 30, 60)
CARD_BG_COLOR = (50, 50, 70)
CARD_SELECTED_COLOR = (100, 100, 140)
CARD_DISABLED_COLOR = (30, 30, 40)
HEALTH_BAR_BG = (60, 60, 60)
HEALTH_BAR_PLAYER = (0, 200, 0)
HEALTH_BAR_ENEMY = (200, 0, 0)

# Lane colors (3 vertical lanes)
LANE_COLORS = [
    (40, 45, 50),
    (35, 40, 45),
    (40, 45, 50),
]
LANE_DIVIDER_COLOR = (60, 65, 70)

# Layout
HEADER_HEIGHT = 50
FOOTER_HEIGHT = 150
BATTLEFIELD_HEIGHT = SCREEN_HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT
LANE_WIDTH = SCREEN_WIDTH // 3

# Base positions (vertical: player at bottom, enemy at top)
PLAYER_BASE_Y = SCREEN_HEIGHT - FOOTER_HEIGHT - 40
ENEMY_BASE_Y = HEADER_HEIGHT + 40

# Card dimensions
CARD_WIDTH = 90
CARD_HEIGHT = 80
CARD_SPACING = 8
CARD_Y = SCREEN_HEIGHT - FOOTER_HEIGHT + 50

# Mana settings
MAX_MANA = 10
STARTING_MANA = 5
MANA_REGEN_RATE = 1.0  # per second

# Game settings
FPS = 60

# Unit type definitions
UNIT_TYPES = {
    "soldier": {
        "name": "Soldier",
        "hp": 100,
        "damage": 15,
        "speed": 80,
        "range": 40,
        "cost": 2,
        "attack_cooldown": 1.0,
        "shape": "rect",
        "color": BLUE,
        "size": 25,
    },
    "tank": {
        "name": "Tank",
        "hp": 250,
        "damage": 10,
        "speed": 40,
        "range": 35,
        "attack_cooldown": 1.5,
        "cost": 4,
        "shape": "rect",
        "color": GRAY,
        "size": 35,
    },
    "archer": {
        "name": "Archer",
        "hp": 60,
        "damage": 20,
        "speed": 60,
        "range": 150,
        "attack_cooldown": 1.2,
        "cost": 3,
        "shape": "circle",
        "color": GREEN,
        "size": 20,
    },
    "knight": {
        "name": "Knight",
        "hp": 150,
        "damage": 25,
        "speed": 70,
        "range": 45,
        "attack_cooldown": 0.9,
        "cost": 5,
        "shape": "rect",
        "color": YELLOW,
        "size": 30,
    },
    "assassin": {
        "name": "Assassin",
        "hp": 80,
        "damage": 40,
        "speed": 120,
        "range": 30,
        "attack_cooldown": 0.7,
        "cost": 4,
        "shape": "circle",
        "color": PURPLE,
        "size": 22,
    },
    "giant": {
        "name": "Giant",
        "hp": 400,
        "damage": 35,
        "speed": 30,
        "range": 50,
        "attack_cooldown": 2.0,
        "cost": 7,
        "shape": "rect",
        "color": ORANGE,
        "size": 40,
    },
}

# AI settings
AI_DECISION_INTERVAL = 1.5  # seconds
AI_DEFEND_THRESHOLD = 0.7
AI_REINFORCE_THRESHOLD = 0.3
AI_REINFORCE_CHANCE = 0.6
