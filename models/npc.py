# models/npc.py

import random

class NPC:
    def __init__(self, name, hp, attack_power, loot_gold, xp_reward, is_boss=False):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.loot_gold = loot_gold
        self.xp_reward = xp_reward
        self.is_boss = is_boss
        self.status_effects = []  # Can have effects like "Poisoned", "Burning", "Stunned"

    def is_alive(self):
        return self.hp > 0

    def attack(self, player):
        """Regular attack."""
        return self.attack_power

    def special_attack(self, player):
        """Boss special attacks with random choice."""
        if not self.is_boss:
            return None  # Normal monsters have no specials

        battle_log = ""

        specials = []

        if self.name == "Ancient Dragon":
            specials = [
                ("\n🔥 The Ancient Dragon breathes FIRE!", 40, "Burning"),
                ("\n🌪️ The Ancient Dragon summons a cyclone!", 30, None)
            ]
        elif self.name == "Shadow Knight":
            specials = [
                ("\n🖤 The Shadow Knight strikes with DARK BLADE!", 30, "Poisoned"),
                ("\n🌫️ The Shadow Knight shrouds the battlefield in darkness!", 20, None)
            ]
        elif self.name == "Cave Wyrm":
            specials = [
                ("\n💨 The Cave Wyrm spits toxic gas!", 20, "Poisoned"),
                ("\n🪨 The Cave Wyrm shakes the ground!", 25, None)
            ]
        elif self.name == "Forest Guardian":
            specials = [
                ("\n🌿 The Forest Guardian summons thorny vines!", 25, "Stunned"),
                ("\n🌱 The Forest Guardian heals itself slightly!", -20, None)  # Heals itself
            ]
        else:
            specials = [
                (f"\n⚡ {self.name} strikes with overwhelming force!", 25, None)
            ]

        move = random.choice(specials)
        move_text, dmg, status = move

        battle_log += move_text

        if dmg > 0:
            player.hp -= dmg
        elif dmg < 0:
            self.hp = min(self.hp - dmg, 100)  # Heal self up to 100 max HP

        if status:
            player.add_status(status)

        return battle_log

    def describe(self):
        """Describe the enemy including any active statuses."""
        status = "Alive" if self.is_alive() else "Defeated"
        hp_display = f"{self.hp} HP" if self.is_alive() else "0 HP"
        boss_tag = " [Boss]" if self.is_boss else ""

        if self.status_effects:
            effects = ', '.join(self.status_effects)
            return f"{self.name}{boss_tag} - {hp_display} - {status} ({effects})"
        else:
            return f"{self.name}{boss_tag} - {hp_display} - {status}"

    def process_status_effects(self):
        """Apply ongoing damage for Burning or Poisoned status."""
        log = ""
        if "Burning" in self.status_effects:
            self.hp -= 5
            log += f"\n🔥 {self.name} suffers 5 damage from burning!"
        if "Poisoned" in self.status_effects:
            self.hp -= 5
            log += f"\n🧪 {self.name} suffers 5 damage from poison!"

        # Remove effects if NPC is dead
        if not self.is_alive():
            self.status_effects.clear()

        return log
