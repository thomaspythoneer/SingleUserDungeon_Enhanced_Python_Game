class Player:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100  # Scales with level
        
        # Base stats
        self.max_hp = 100
        self.hp = 100
        self.base_attack = 10
        self.base_defense = 5
        self.gold = 0
        
        # Apply class modifiers
        self._apply_class_modifiers()
        
        # Equipment
        self.equipped_weapon = None
        self.equipped_armor = None
        self.inventory = []
        self.inventory_capacity = 10
        
        # Status effects (temporary buffs/debuffs)
        self.status_effects = []  # [{effect: str, value: int, duration: int}]
        
        # Quest tracking
        self.quests = {}
        self.visited_rooms = set()
    
    def _apply_class_modifiers(self):
        """Apply stat modifiers based on character class"""
        if self.character_class == "warrior":
            self.max_hp *= 1.2
            self.hp = self.max_hp
            self.base_defense *= 1.2
        elif self.character_class == "mage":
            self.max_hp *= 0.8
            self.hp = self.max_hp
            self.base_attack *= 1.3
        elif self.character_class == "rogue":
            self.base_attack *= 1.2
            self.base_defense *= 0.9
    
    @property
    def attack(self):
        """Calculate total attack power including equipment and effects"""
        total = self.base_attack
        if self.equipped_weapon:
            total += self.equipped_weapon.damage
        
        # Add status effect bonuses
        for effect in self.status_effects:
            if effect["effect"] == "attack_boost":
                total += effect["value"]
        
        return total
    
    @property
    def defense(self):
        """Calculate total defense including equipment and effects"""
        total = self.base_defense
        if self.equipped_armor:
            total += self.equipped_armor.defense
        
        # Add status effect bonuses
        for effect in self.status_effects:
            if effect["effect"] == "defense_boost":
                total += effect["value"]
        
        return total
    
    def update_status_effects(self):
        """Update duration of status effects and remove expired ones"""
        active_effects = []
        for effect in self.status_effects:
            effect["duration"] -= 1
            if effect["duration"] > 0:
                active_effects.append(effect)
        self.status_effects = active_effects
    
    def add_status_effect(self, effect, value, duration):
        """Add a temporary status effect"""
        self.status_effects.append({
            "effect": effect,
            "value": value,
            "duration": duration
        })
    
    def take_damage(self, damage):
        """Take damage considering defense and return actual damage taken"""
        mitigated_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - mitigated_damage)
        return mitigated_damage
    
    def heal(self, amount):
        """Heal the player and return amount actually healed"""
        if self.hp >= self.max_hp:
            return 0
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def add_xp(self, amount):
        """Add XP and handle leveling up"""
        self.xp += amount
        level_ups = 0
        
        while self.xp >= self.xp_to_next_level:
            self.level_up()
            level_ups += 1
        
        return level_ups
    
    def level_up(self):
        """Handle level up mechanics"""
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        
        # Increase stats
        old_max_hp = self.max_hp
        self.max_hp = int(self.max_hp * 1.1)
        self.hp += (self.max_hp - old_max_hp)
        self.base_attack = int(self.base_attack * 1.1)
        self.base_defense = int(self.base_defense * 1.1)
    
    def add_to_inventory(self, item):
        """Add item to inventory if there's space"""
        if len(self.inventory) >= self.inventory_capacity:
            return False
        self.inventory.append(item)
        return True
    
    def remove_from_inventory(self, item):
        """Remove item from inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def equip_weapon(self, weapon):
        """Equip a weapon, moving the old one to inventory"""
        if weapon not in self.inventory:
            return False
        
        if self.equipped_weapon:
            self.inventory.append(self.equipped_weapon)
        
        self.inventory.remove(weapon)
        self.equipped_weapon = weapon
        return True
    
    def equip_armor(self, armor):
        """Equip armor, moving the old one to inventory"""
        if armor not in self.inventory:
            return False
        
        if self.equipped_armor:
            self.inventory.append(self.equipped_armor)
        
        self.inventory.remove(armor)
        self.equipped_armor = armor
        return True
    
    def use_item(self, item):
        """Use an item from inventory"""
        if item not in self.inventory:
            return "Item not in inventory"
        
        if not item.can_use:
            return "This item cannot be used"
        
        result = item.use(self)
        if result:
            self.remove_from_inventory(item)
        return result
    
    def get_status(self):
        """Get a formatted string of player's current status"""
        status = [
            f"Name: {self.name} ({self.character_class})",
            f"Level: {self.level} (XP: {self.xp}/{self.xp_to_next_level})",
            f"HP: {self.hp}/{self.max_hp}",
            f"Attack: {self.attack} (Base: {self.base_attack})",
            f"Defense: {self.defense} (Base: {self.base_defense})",
            f"Gold: {self.gold}",
        ]
        
        if self.equipped_weapon:
            status.append(f"Weapon: {self.equipped_weapon.name}")
        if self.equipped_armor:
            status.append(f"Armor: {self.equipped_armor.name}")
        
        if self.status_effects:
            status.append("\nActive Effects:")
            for effect in self.status_effects:
                status.append(f"- {effect['effect']}: +{effect['value']} ({effect['duration']} turns)")
        
        return "\n".join(status)

    def move(self, direction):
        if direction in self.current_room.exits:
            self.current_room = self.current_room.exits[direction]
            return f"You move {direction} to {self.current_room.name}."
        return "You can't go that way."

    def look(self):
        return self.current_room.look()

    def add_status(self, status):
        if status not in self.status_effects:
            self.status_effects.append(status)

    def apply_status_damage(self):
        damage_log = ""
        if "Burning" in self.status_effects:
            self.hp -= 5
            damage_log += "\n🔥 You are burning! Lose 5 HP."
        if "Poisoned" in self.status_effects:
            self.hp -= 3
            damage_log += "\n🧪 You are poisoned! Lose 3 HP."
        if self.hp < 0:
            self.hp = 0
        return damage_log

    def clear_status(self, status):
        if status in self.status_effects:
            self.status_effects.remove(status)

    def list_statuses(self):
        if not self.status_effects:
            return "Normal"
        return ", ".join(effect['effect'] for effect in self.status_effects)

    def pick_item(self, item_name):
        for item in self.current_room.items:
            if item.name.lower() == item_name.lower():
                self.inventory.append(item)
                self.current_room.items.remove(item)
                return f"You picked up {item.name}."
        return "There's no such item here."

    def drop_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                self.current_room.items.append(item)
                return f"🗑️ You dropped {item.name}."
        return "You don't have that item."

    def equip_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if item.item_type == "weapon":
                    self.equipped_weapon = item
                    return f"🗡️ You equipped {item.name}!"
                elif item.item_type == "armor":
                    self.equipped_armor = item
                    return f"🛡️ You equipped {item.name}!"
                else:
                    return "You can't equip that item."
        return "You don't have that item."

    def show_inventory(self):
        if not self.inventory:
            return "🎒 Your inventory is empty."

        inv = "\n".join(f"- {item.describe()}" for item in self.inventory)
        equipped = f"\n🗡️ Equipped Weapon: {self.equipped_weapon.name if self.equipped_weapon else 'None'}"
        equipped += f"\n🛡️ Equipped Armor: {self.equipped_armor.name if self.equipped_armor else 'None'}"

        return f"🎒 Inventory:\n{inv}{equipped}"

    def health_bar(self):
        total_blocks = 20
        health_ratio = max(self.hp / self.max_hp, 0)
        filled_blocks = int(total_blocks * health_ratio)
        empty_blocks = total_blocks - filled_blocks
        return "[" + "█" * filled_blocks + "-" * empty_blocks + f"] {self.hp}/{self.max_hp} HP"

    def xp_bar(self):
        total_blocks = 20
        xp_ratio = self.xp / (100 * self.level)
        filled_blocks = int(total_blocks * xp_ratio)
        empty_blocks = total_blocks - filled_blocks
        return "[" + "█" * filled_blocks + "-" * empty_blocks + f"] {self.xp}/{100 * self.level} XP"

    def learn_spell(self, spell_name: str):
        self.spells.add(spell_name.lower())
        return f"🔮 You have learned the '{spell_name}' spell!"

    def cast_spell(self, spell_name: str, world):
        s = spell_name.lower()
        if s not in self.spells:
            return "❌ You don't know that spell."
        room = self.current_room
        if s == "reveal":
            if room.name == "Whispering Caverns" and "up" not in room.exits:
                room.add_exit('up', world.rooms["Hidden Chamber"])
                return "✨ You whisper the secret words… a hidden passage opens upward!"
            else:
                return "🔒 The spell fizzles—there's nothing to reveal here."
        if s == "exit":
            if room.name == "Hidden Chamber" and "up" not in room.exits:
                room.add_exit('up', world.rooms["Whispering Caverns"])
                return "✨ A swirling portal appears, leading back up!"
            else:
                return "🔒 The spell fizzles—there's no exit to conjure here."
        return f"❓ Casting '{spell_name}' has no effect."
