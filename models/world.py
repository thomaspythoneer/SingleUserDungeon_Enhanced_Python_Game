# models/world.py

from models.room import Room
from models.npc import NPC
from models.enemy import Enemy
from models.item import Item
from models.item import ScrollOfRevelation
from models.shop_npc import ShopNPC

# Hidden Chamber Constants
SECRET_PHRASE = "whispers of the ancients"
HINT_TEXT = "Listen to the whispers of the cavern walls..."

# Door Animation Frames
DOOR_FRAMES = [
    """
    +----------+
    |    ||    |
    |    ||    |
    |    ||    |
    +----------+
    """,
    """
    +----------+
    |   |  |   |
    |   |  |   |
    |   |  |   |
    +----------+
    """,
    """
    +----------+
    |  |    |  |
    |  |    |  |
    |  |    |  |
    +----------+
    """,
    """
    +----------+
    | |      | |
    | |      | |
    | |      | |
    +----------+
    """,
    """
    +----------+
    |          |
    |          |
    |          |
    +----------+
    """
]

# Special Chamber Loot
CHAMBER_LOOT = [
    Item("Ancient Relic", "A mysterious artifact pulsing with magical energy", item_type="artifact", value=500),
    Item("Enchanted Scroll", "Contains powerful forgotten spells", item_type="scroll", value=300),
    Item("Crystal Shard", "A fragment of pure magical essence", item_type="material", value=250)
]

class World:
    def __init__(self):
        """Initialize the game world with all rooms and connections."""
        self.rooms = {}
        self.build_world()

    def build_world(self):
        """Create and connect all rooms in the game world."""
        # Create base rooms
        sacred_grove = Room(
            "Sacred Grove",
            "A peaceful grove bathed in ethereal light. Ancient trees whisper secrets of forgotten magic."
        )
        
        forest = Room(
            "Enchanted Forest",
            "Tall, twisting trees and faint whispers fill the air. Magic seems to pulse through the very ground."
        )
        
        caverns = Room(
            "Whispering Caverns",
            "Dark tunnels echo with mysterious sounds. Crystal formations cast eerie shadows on the walls."
        )
        
        castle = Room(
            "Abandoned Castle",
            "Once-grand halls now lie in ruins. Moonlight streams through broken windows."
        )
        
        clearing = Room(
            "Hidden Clearing",
            "A serene clearing bathed in perpetual twilight. Fireflies dance through the air."
        )
        
        tower = Room(
            "Forgotten Tower",
            "A crumbling tower that seems to touch the clouds. Strange energies emanate from within."
        )
        
        # Connect rooms
        sacred_grove.add_exit("south", forest)
        forest.add_exit("north", sacred_grove)
        forest.add_exit("east", caverns)
        forest.add_exit("south", clearing)
        caverns.add_exit("west", forest)
        caverns.add_exit("east", castle)
        castle.add_exit("west", caverns)
        clearing.add_exit("north", forest)
        clearing.add_exit("east", tower)
        tower.add_exit("west", clearing)

        # Create and place NPCs
        forest_guardian = NPC("Forest Guardian", hp=80, attack_power=15, 
                            loot_gold=50, xp_reward=100, is_boss=False)
        forest.npcs.append(forest_guardian)
        
        cave_lurker = NPC("Cave Lurker", hp=60, attack_power=12,
                         loot_gold=30, xp_reward=75, is_boss=False)
        caverns.npcs.append(cave_lurker)

        # Create and place items
        healing_potion = Item("Healing Potion", "Restores 50 HP", "potion", 50)
        sacred_grove.items.append(healing_potion)
        
        rusty_sword = Item("Rusty Sword", "An old but serviceable blade", "weapon", 10)
        forest.items.append(rusty_sword)
        
        # Create shopkeeper and inventory
        shop_inventory = {
            Item("Health Potion", "Restores 50 HP", "potion", 50): 30,
            Item("Iron Sword", "A reliable weapon", "weapon", 25): 100,
            Item("Leather Armor", "Basic protection", "armor", 15): 80
        }
        merchant = ShopNPC("Wandering Merchant", shop_inventory)
        clearing.npcs.append(merchant)

        # Store all rooms
        self.rooms = {
            "Sacred Grove": sacred_grove,
            "Enchanted Forest": forest,
            "Whispering Caverns": caverns,
            "Abandoned Castle": castle,
            "Hidden Clearing": clearing,
            "Forgotten Tower": tower
        }

    def get_starting_room(self):
        """Return the starting room (Sacred Grove)."""
        return self.rooms["Sacred Grove"]

# Constants
SECRET_PHRASE = "whispers of the ancients"
DOOR_OPENING_FRAMES = [
    "╔════╗\n║    ║\n║    ║\n╚════╝",
    "╔════╗\n║ ░░ ║\n║ ░░ ║\n╚════╝",
    "╔════╗\n║ ▒▒ ║\n║ ▒▒ ║\n╚════╝",
    "╔════╗\n║ ▓▓ ║\n║ ▓▓ ║\n╚════╝",
    "╔════╗\n║ ██ ║\n║ ██ ║\n╚════╝"
]

DOOR_CLOSING_FRAMES = DOOR_OPENING_FRAMES[::-1]

SPECIAL_CHAMBER_LOOT = [
    Item("Ancient Scroll", "A mysterious scroll covered in glowing runes", "scroll", "legendary"),
    Item("Crystal Staff", "A staff humming with magical energy", "weapon", "epic"),
    Item("Mystic Amulet", "An amulet that pulses with an otherworldly light", "accessory", "rare")
]
