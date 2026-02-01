from src.constants import MAX_MANA, STARTING_MANA, MANA_REGEN_RATE
from src.unit import Unit, UnitType


class Player:
    def __init__(self, is_human: bool = True):
        self.is_human = is_human
        self.mana = STARTING_MANA
        self.units: list[Unit] = []

    def update(self, dt: float, enemy_units: list[Unit]):
        """Update player state and all units."""
        # Regenerate mana
        self.mana = min(MAX_MANA, self.mana + MANA_REGEN_RATE * dt)

        # Update all units
        for unit in self.units:
            unit.update(dt, enemy_units)

        # Remove dead units
        self.units = [u for u in self.units if u.is_alive]

    def can_afford(self, unit_name: str) -> bool:
        """Check if player can afford to spawn a unit."""
        from src.constants import UNIT_TYPES
        cost = UNIT_TYPES[unit_name]["cost"]
        return self.mana >= cost

    def spawn_unit(self, unit_name: str, lane: int) -> Unit | None:
        """Spawn a unit in the specified lane if affordable."""
        from src.constants import UNIT_TYPES
        cost = UNIT_TYPES[unit_name]["cost"]

        if self.mana < cost:
            return None

        self.mana -= cost
        unit_type = UnitType.from_name(unit_name)
        unit = Unit(unit_type, lane, is_player=self.is_human)
        self.units.append(unit)
        return unit

    def get_units_in_lane(self, lane: int) -> list[Unit]:
        """Get all units in a specific lane."""
        return [u for u in self.units if u.lane == lane and u.is_alive]

    def check_win_condition(self) -> bool:
        """Check if any unit has reached the enemy base."""
        for unit in self.units:
            if unit.has_reached_enemy_base():
                return True
        return False
