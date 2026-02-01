import random
from src.player import Player
from src.unit import Unit
from src.constants import (
    AI_DECISION_INTERVAL, AI_DEFEND_THRESHOLD,
    AI_REINFORCE_THRESHOLD, AI_REINFORCE_CHANCE,
    UNIT_TYPES, PLAYER_BASE_Y, ENEMY_BASE_Y
)


class AI(Player):
    def __init__(self):
        super().__init__(is_human=False)
        self.decision_timer = 0.0
        self.unit_names = list(UNIT_TYPES.keys())

    def update(self, dt: float, enemy_units: list[Unit]):
        """Update AI state and make decisions."""
        # Call parent update
        super().update(dt, enemy_units)

        # Decision making
        self.decision_timer += dt
        if self.decision_timer >= AI_DECISION_INTERVAL:
            self.decision_timer = 0.0
            self.make_decision(enemy_units)

    def calculate_lane_threat(self, lane: int, enemy_units: list[Unit]) -> float:
        """
        Calculate threat level for a lane (0.0 to 1.0).
        Higher threat means enemy (player) is closer to our base (top).
        """
        lane_enemies = [u for u in enemy_units if u.lane == lane and u.is_alive]
        lane_allies = self.get_units_in_lane(lane)

        if not lane_enemies:
            return 0.0

        # Find the closest enemy to our base (top)
        # Player units move up (decreasing y), so smaller y = closer to AI base
        closest_enemy_y = min(e.y for e in lane_enemies)

        # Distance from AI base (top) - smaller distance = higher threat
        distance_to_base = closest_enemy_y - ENEMY_BASE_Y
        max_distance = PLAYER_BASE_Y - ENEMY_BASE_Y

        # Normalize: closer to our base = higher threat
        position_threat = 1.0 - (distance_to_base / max_distance)

        # Factor in enemy count vs ally count
        enemy_power = sum(e.hp for e in lane_enemies)
        ally_power = sum(a.hp for a in lane_allies) if lane_allies else 0

        if ally_power == 0:
            power_ratio = 1.0
        else:
            power_ratio = min(1.0, enemy_power / (ally_power + enemy_power))

        # Combined threat
        return (position_threat * 0.6 + power_ratio * 0.4)

    def calculate_lane_advantage(self, lane: int, enemy_units: list[Unit]) -> float:
        """
        Calculate our advantage in a lane (0.0 to 1.0).
        Higher value means we're winning that lane (pushing toward player base).
        """
        lane_enemies = [u for u in enemy_units if u.lane == lane and u.is_alive]
        lane_allies = self.get_units_in_lane(lane)

        if not lane_allies:
            return 0.0

        # Find our furthest unit toward player base (bottom)
        # AI units move down (increasing y), so larger y = closer to player base
        furthest_ally_y = max(a.y for a in lane_allies)

        # Calculate how far we've pushed
        max_distance = PLAYER_BASE_Y - ENEMY_BASE_Y
        distance_pushed = furthest_ally_y - ENEMY_BASE_Y
        position_advantage = distance_pushed / max_distance

        # Factor in power ratio
        ally_power = sum(a.hp for a in lane_allies)
        enemy_power = sum(e.hp for e in lane_enemies) if lane_enemies else 0

        if enemy_power == 0:
            power_ratio = 1.0
        else:
            power_ratio = min(1.0, ally_power / (ally_power + enemy_power))

        return (position_advantage * 0.4 + power_ratio * 0.6)

    def get_affordable_units(self) -> list[str]:
        """Get list of unit names we can afford."""
        return [name for name in self.unit_names if self.can_afford(name)]

    def make_decision(self, enemy_units: list[Unit]):
        """Make a strategic decision about what to spawn."""
        affordable = self.get_affordable_units()
        if not affordable:
            return

        # Analyze all lanes
        lane_threats = [self.calculate_lane_threat(i, enemy_units) for i in range(3)]
        lane_advantages = [self.calculate_lane_advantage(i, enemy_units) for i in range(3)]

        # Priority 1: Defend high threat lanes
        for lane, threat in enumerate(lane_threats):
            if threat > AI_DEFEND_THRESHOLD:
                # Spawn defensive unit
                defensive_units = [u for u in ["tank", "soldier", "knight"] if u in affordable]
                if defensive_units:
                    unit = random.choice(defensive_units)
                    self.spawn_unit(unit, lane)
                    return

        # Priority 2: Reinforce winning lanes
        for lane, advantage in enumerate(lane_advantages):
            if advantage > (1.0 - AI_REINFORCE_THRESHOLD):
                if random.random() < AI_REINFORCE_CHANCE:
                    # Spawn offensive unit to push
                    offensive_units = [u for u in ["soldier", "archer", "assassin", "knight"]
                                      if u in affordable]
                    if offensive_units:
                        unit = random.choice(offensive_units)
                        self.spawn_unit(unit, lane)
                        return

        # Priority 3: Random attack if we have enough mana
        if self.mana >= 5:
            lane = random.randint(0, 2)
            unit = random.choice(affordable)
            self.spawn_unit(unit, lane)
