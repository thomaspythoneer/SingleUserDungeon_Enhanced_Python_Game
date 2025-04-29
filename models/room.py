import random
from models.enemy import Enemy
from models.item import Item

class Room:
    def __init__(self, name, description, room_type="normal"):
        self.name = name
        self.description = description
        self.room_type = room_type  # normal, combat, boss, shop, rest
        self.exits = {}  # direction: room
        self.items = []
        self.npcs = []  # List of NPCs (including enemies) in the room
        self.enemy_spawn_chance = 0.3 if room_type == "normal" else 1.0 if room_type == "combat" else 0
        self.cleared = False  # For combat rooms
        self.visited = False
        self.shop_inventory = []  # For shop rooms
        
        # Special room features
        self.has_chest = False
        self.chest_opened = False
        self.trap = None  # {type: str, damage: int, detected: bool}
        self.special_features = {}  # For quest-related or unique room features
        self.events = {}
        self.is_secret = name == "Hidden Chamber"
        self.door_state = "closed" if self.is_secret else "open"
    
    def connect(self, direction, room):
        """Connect this room to another in the given direction with proper bidirectional linking"""
        self.exits[direction] = room
        # Add reverse connection if not already present
        reverse_dirs = {
            "north": "south", "south": "north",
            "east": "west", "west": "east",
            "up": "down", "down": "up"
        }
        if direction in reverse_dirs and reverse_dirs[direction] not in room.exits:
            room.exits[reverse_dirs[direction]] = self
    
    def add_exit(self, direction, room):
        """Legacy method - redirects to connect for consistency"""
        self.connect(direction, room)
    
    def remove_exit(self, direction):
        """Remove an exit and its corresponding reverse connection"""
        if direction in self.exits:
            other_room = self.exits[direction]
            reverse_dirs = {
                "north": "south", "south": "north",
                "east": "west", "west": "east",
                "up": "down", "down": "up"
            }
            if direction in reverse_dirs:
                reverse_dir = reverse_dirs[direction]
                if reverse_dir in other_room.exits:
                    del other_room.exits[reverse_dir]
            del self.exits[direction]
    
    def get_exits(self):
        """Get available exits from the room"""
        return list(self.exits.keys())
    
    def add_item(self, item):
        """Add an item to the room"""
        self.items.append(item)
    
    def remove_item(self, item):
        """Remove an item from the room"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def add_npc(self, npc):
        """Add an NPC to the room"""
        self.npcs.append(npc)
    
    def remove_npc(self, npc):
        """Remove an NPC from the room"""
        if npc in self.npcs:
            self.npcs.remove(npc)
            if not any(isinstance(n, Enemy) for n in self.npcs) and self.room_type in ["combat", "boss"]:
                self.cleared = True
    
    def add_trap(self, trap_type, damage):
        """Add a trap to the room"""
        self.trap = {"type": trap_type, "damage": damage, "detected": False}
    
    def detect_trap(self):
        """Mark trap as detected"""
        if self.trap:
            self.trap["detected"] = True
    
    def trigger_trap(self, player):
        """Trigger the room's trap if it exists"""
        if not self.trap:
            return None
        
        if self.trap["detected"]:
            return f"You carefully avoid the {self.trap['type']} trap."
        
        damage = self.trap["damage"]
        actual_damage = player.take_damage(damage)
        self.trap = None  # Trap is expended
        return f"You triggered a {self.trap['type']} trap! Took {actual_damage} damage."
    
    def add_chest(self, is_locked=False):
        """Add a treasure chest to the room"""
        self.has_chest = True
        self.chest_opened = False
        self.special_features["chest_locked"] = is_locked
    
    def open_chest(self, player):
        """Open a chest in the room if it exists"""
        if not self.has_chest or self.chest_opened:
            return "There is no unopened chest here."
        
        if self.special_features.get("chest_locked", False):
            key_name = "Rusty Key"  # Example key name
            has_key = any(item.name == key_name for item in player.inventory)
            if not has_key:
                return "The chest is locked. You need a key to open it."
        
        self.chest_opened = True
        # Generate chest loot based on player level
        loot = []
        gold = player.level * 50 + random.randint(10, 100)
        item = Item.create_random_item(player.level)
        loot.append(item)
        
        # Add items to room
        self.items.extend(loot)
        player.gold += gold
        
        return f"You found {gold} gold and {item.name} in the chest!"
    
    def enter(self, player):
        """Handle room entry events"""
        self.visited = True
        events = []
        
        # Check for traps
        if self.trap and not self.trap["detected"]:
            trap_result = self.trigger_trap(player)
            if trap_result:
                events.append(trap_result)
        
        # Spawn enemies in normal rooms
        if not self.cleared and not any(isinstance(n, Enemy) for n in self.npcs) and random.random() < self.enemy_spawn_chance:
            enemy = Enemy.create_random_enemy(player.level)
            self.add_npc(enemy)
            events.append(f"A {enemy.name} appears!")
        
        return "\n".join(events) if events else None
    
    def describe(self, show_items=True, show_npcs=True):
        """Get a full description of the room"""
        desc = f"{self.name}\n{self.description}"
        
        if self.trap and self.trap["detected"]:
            desc += f"\nYou notice a {self.trap['type']} trap here!"
        
        if self.has_chest and not self.chest_opened:
            desc += "\nThere is a treasure chest here."
        
        if show_items and self.items:
            items_desc = "\nItems here:\n" + "\n".join(f"- {item.name}" for item in self.items)
            desc += items_desc
        
        if show_npcs and self.npcs:
            npcs_desc = "\nBeings present:\n" + "\n".join(f"- {npc.describe()}" for npc in self.npcs)
            desc += npcs_desc
        
        exits = self.get_exits()
        if exits:
            desc += f"\nExits: {', '.join(exits)}"
        
        return desc

    def look(self):
        """Enhanced look method with special handling for Hidden Chamber"""
        desc = f"\n🏰 {self.name} 🏰\n\n{self.description}\n"

        if self.items:
            desc += "\n🧺 Items here:\n"
            for item in self.items:
                desc += f"- {item.name}\n"

        if self.npcs:
            desc += "\n👹 Creatures present:\n"
            for npc in self.npcs:
                desc += f"- {npc.describe()}\n"

        if self.exits:
            desc += "\n🚪 Exits:\n"
            for direction in self.exits:
                if direction == "down" and self.name == "Whispering Caverns":
                    desc += f"- {direction} (A mysterious passage...)\n"
                else:
                    desc += f"- {direction}\n"

        # Special description for Hidden Chamber
        if self.is_secret:
            desc += "\n🔮 Ancient runes glow faintly on the walls...\n"
            if self.door_state == "closed":
                desc += "The chamber entrance is sealed.\n"
            else:
                desc += "The magical barrier is open.\n"

        return desc

    def add_event(self, event_name, event_function):
        """Add an event handler to the room."""
        self.events[event_name] = event_function

    def trigger_event(self, event_name, player):
        """Trigger a specific event in the room."""
        if event_name in self.events:
            return self.events[event_name](player)
        return None

    def on_enter(self, player):
        """Enhanced room entry handler"""
        self.visited = True
        
        # Special handling for Hidden Chamber
        if self.is_secret and not player.found_secret:
            player.found_secret = True
            return "\n🌟 You have discovered the Hidden Chamber! Ancient magic fills the air..."
            
        # Special handling for Whispering Caverns
        if self.name == "Whispering Caverns" and "down" not in self.exits:
            return "\n🔮 The walls seem to whisper ancient secrets..."
            
        # Trigger any custom events
        if "on_enter" in self.events:
            return self.events["on_enter"](player)
            
        return None

    def get_item(self, item_name):
        """Get an item from the room by name."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def validate_secret_phrase(self, phrase):
        """Validate the secret phrase for the Hidden Chamber"""
        if not self.is_secret:
            return False
        from models.world import SECRET_PHRASE
        return phrase.lower() == SECRET_PHRASE.lower()

    def play_door_animation(self, opening=True):
        """Return the door animation frames for opening/closing the secret door."""
        from models.world import DOOR_FRAMES
        frames = DOOR_FRAMES if opening else list(reversed(DOOR_FRAMES))
        return frames

    def spawn_chamber_loot(self):
        """Add special loot to the Hidden Chamber."""
        from models.world import CHAMBER_LOOT
        for item in CHAMBER_LOOT:
            if item not in self.items:
                self.items.append(item)

    def remove_chamber_loot(self):
        """Remove special loot from the Hidden Chamber."""
        from models.world import CHAMBER_LOOT
        for item in CHAMBER_LOOT:
            if item in self.items:
                self.items.remove(item)

    def seal_entrance(self):
        """Seal the entrance to the Hidden Chamber"""
        if self.is_secret:
            self.door_state = "closed"
            # Remove the exit to prevent access
            self.remove_exit("up")

    def unseal_entrance(self):
        """Unseal the entrance to the Hidden Chamber"""
        if self.is_secret:
            self.door_state = "open"
            # Restore the exit
            from models.world import World
            self.connect("up", World().rooms["Whispering Caverns"])
