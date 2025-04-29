from models.npc import NPC
from models.item import Item
import random

class Enemy(NPC):
    def __init__(self, name, level=1, hp=10, attack=2, defense=1, xp_value=10, gold_value=5, drops=None):
        super().__init__(name=name, hp=hp + (level - 1) * 5, 
                        attack_power=attack + (level - 1) * 2,
                        loot_gold=gold_value * level,
                        xp_reward=xp_value * level,
                        is_boss=False)
        self.level = level
        self.defense = defense + (level - 1)
        self.drops = drops if drops else []
        self.max_hp = self.hp
    
    def is_alive(self):
        return self.hp > 0
    
    def take_damage(self, amount):
        actual_damage = max(1, amount - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def calculate_damage(self):
        # Basic damage calculation with some randomness
        base_damage = self.attack
        variation = random.randint(-2, 2)
        return max(1, base_damage + variation)
    
    @classmethod
    def create_random_enemy(cls, player_level):
        """Create a random enemy appropriate for the player's level"""
        enemy_types = [
            ("Goblin", 8, 2, 1, 8, 4),
            ("Orc", 12, 3, 2, 12, 6),
            ("Troll", 15, 4, 2, 15, 8),
            ("Dragon", 20, 5, 3, 20, 10),
            ("Ghost", 10, 3, 1, 10, 5),
            ("Skeleton", 8, 2, 1, 8, 4),
            ("Zombie", 12, 2, 2, 10, 5),
            ("Witch", 8, 4, 1, 12, 6),
            ("Demon", 15, 4, 2, 15, 8),
            ("Giant Spider", 10, 3, 1, 10, 5)
        ]
        
        # Select random enemy type
        name, base_hp, base_attack, base_defense, base_xp, base_gold = random.choice(enemy_types)
        
        # Scale level based on player level
        level = max(1, player_level + random.randint(-2, 2))
        
        # Create drops list
        drops = []
        if random.random() < 0.3:  # 30% chance to drop an item
            drops.append(Item.create_random_item(level))
        
        return cls(
            name=name,
            level=level,
            hp=base_hp,
            attack=base_attack,
            defense=base_defense,
            xp_value=base_xp,
            gold_value=base_gold,
            drops=drops
        ) 