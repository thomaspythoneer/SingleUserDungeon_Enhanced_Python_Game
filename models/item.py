class Item:
    def __init__(self, name, description, item_type="misc", value=0, combat_usable=False, effects=None, rarity="common"):
        self.name = name
        self.description = description
        self.item_type = item_type  # "weapon", "armor", "consumable", "key", etc.
        self.value = value
        self.combat_usable = combat_usable
        self.effects = effects if effects else {}
        self.rarity = rarity
    
    def use(self, player, enemy=None):
        """Use the item and apply its effects"""
        if self.item_type == "consumable":
            # Apply healing or other effects
            if "heal" in self.effects:
                heal_amount = self.effects["heal"]
                player.hp = min(player.max_hp, player.hp + heal_amount)
                return f"You used {self.name} and healed for {heal_amount} HP!"
            
            if "temp_attack" in self.effects:
                player.add_status_effect("attack_boost", self.effects["temp_attack"], 3)
                return f"You used {self.name} and gained +{self.effects['temp_attack']} attack for 3 turns!"
            
            if "temp_defense" in self.effects:
                player.add_status_effect("defense_boost", self.effects["temp_defense"], 3)
                return f"You used {self.name} and gained +{self.effects['temp_defense']} defense for 3 turns!"
        
        elif self.item_type == "weapon":
            if "damage" in self.effects:
                player.equip_weapon(self)
                return f"You equipped {self.name}!"
        
        elif self.item_type == "armor":
            if "defense" in self.effects:
                player.equip_armor(self)
                return f"You equipped {self.name}!"
        
        return f"You used {self.name}!"
    
    @classmethod
    def create_random_item(cls, level):
        """Create a random item appropriate for the given level"""
        import random
        
        item_types = {
            "weapon": [
                ("Rusty Sword", "A worn but serviceable blade", 5, {"damage": 3}),
                ("Steel Sword", "A reliable weapon", 10, {"damage": 5}),
                ("Magic Sword", "Glows with mysterious energy", 20, {"damage": 8}),
            ],
            "armor": [
                ("Leather Armor", "Basic protection", 5, {"defense": 2}),
                ("Chain Mail", "Solid metal protection", 15, {"defense": 4}),
                ("Plate Armor", "Heavy but effective", 25, {"defense": 6}),
            ],
            "consumable": [
                ("Health Potion", "Restores HP", 5, {"heal": 20}, True),
                ("Strength Potion", "Temporarily boosts attack", 8, {"temp_attack": 3}, True),
                ("Defense Potion", "Temporarily boosts defense", 8, {"temp_defense": 3}, True),
            ]
        }
        
        # Select random item type and item
        item_type = random.choice(list(item_types.keys()))
        base_item = random.choice(item_types[item_type])
        
        # Scale effects based on level
        effects = base_item[3].copy()
        for key in effects:
            effects[key] = int(effects[key] * (1 + (level - 1) * 0.2))
        
        combat_usable = len(base_item) > 4 and base_item[4]
        
        return cls(
            name=base_item[0],
            description=base_item[1],
            item_type=item_type,
            value=base_item[2] * level,
            combat_usable=combat_usable,
            effects=effects
        )

    def describe(self):
        return f"{self.name}: {self.description}"

class ScrollOfRevelation(Item):
    def __init__(self):
        description = "A weathered scroll inscribed with ancient runes."
        super().__init__(
            name="Scroll of Revelation",
            description=description,
            item_type="scroll",
            value=100,
            combat_usable=False,
            effects={"reveal": True}
        )

    def use(self, player):
        msg = player.learn_spell("Reveal")
        return msg + "\n🕮 The scroll disintegrates in your hands."
