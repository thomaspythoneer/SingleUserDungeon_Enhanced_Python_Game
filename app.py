import streamlit as st
import time
import random
from game.full import World, Room, Player, Item, NPC, ShopNPC

# Must be the first Streamlit command
st.set_page_config(
    page_title="Mystic Realms",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class GameStateManager:

    
    @staticmethod
    def initialize():

        if 'state_manager' not in st.session_state:
            st.session_state.state_manager = {
                'initialized': True,
                'game_phase': 'intro',
                'previous_phase': None,
                'character_creation_completed': False,
                'game_started': False,
                'last_action_time': time.time()
            }
        elif not st.session_state.state_manager.get('initialized', False):
            st.session_state.state_manager.update({
                'initialized': True,
                'game_phase': 'intro',
                'previous_phase': None,
                'character_creation_completed': False,
                'game_started': False,
                'last_action_time': time.time()
            })
    
    @staticmethod
    def can_show_character_creation():

        if not st.session_state.get('state_manager'):
            GameStateManager.initialize()
            return True
            
        manager = st.session_state.state_manager
        
        if manager.get('character_creation_completed') or manager.get('game_started'):
            return False
            

        if manager.get('previous_phase') != 'intro' and manager.get('game_phase') != 'character_select':
            return False
            
        return True
    
    @staticmethod
    def lock_character_creation():
        """Lock character creation permanently."""
        if 'state_manager' in st.session_state:
            st.session_state.state_manager['character_creation_completed'] = True
            st.session_state.state_manager['game_started'] = True
    
    @staticmethod
    def reset():
        """Reset the game state."""
        st.session_state.clear()
        GameStateManager.initialize()

def intro_sequence():
    """Display the game introduction sequence."""

    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Global styles */
        .stApp {
            background-color: #000000;
            background-image: radial-gradient(circle at center, #001100 0%, #000000 100%);
        }
        
        /* Container styles */
        .game-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            min-height: 80vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        /* RGB Split Title Effect */
        .game-title {
            font-family: 'VT323', monospace;
            font-size: 5em;
            color: #fff;
            text-align: center;
            margin-bottom: 2em;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            position: relative;
            animation: rgb-split 2s infinite;
        }

        .game-title::before,
        .game-title::after {
            content: 'MYSTIC REALMS';
            position: absolute;
            width: 100%;
            height: 100%;
            left: 0;
            top: 0;
            mix-blend-mode: screen;
            pointer-events: none;
        }

        .game-title::before {
            color: #f0f;
            animation: rgb-split-red 3s infinite linear;
        }

        .game-title::after {
            color: #0ff;
            animation: rgb-split-blue 2s infinite linear;
        }

        @keyframes rgb-split {
            0%, 100% { text-shadow: 0 0 10px #0f0; }
            50% { text-shadow: 0 0 20px #0f0, 0 0 30px #0f0; }
        }

        @keyframes rgb-split-red {
            0%, 100% { transform: translate(-4px, 2px); }
            25% { transform: translate(-2px, -2px); }
            50% { transform: translate(4px, -1px); }
            75% { transform: translate(1px, 3px); }
        }

        @keyframes rgb-split-blue {
            0%, 100% { transform: translate(4px, -2px); }
            25% { transform: translate(2px, 2px); }
            50% { transform: translate(-4px, 1px); }
            75% { transform: translate(-1px, -3px); }
        }

        /* Button styles */
        .custom-button {
            background-color: transparent;
            border: 3px solid #00ff00;
            color: #00ff00;
            font-family: 'VT323', monospace;
            font-size: 2em;
            padding: 1em 3em;
            margin: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            position: relative;
            overflow: hidden;
            width: 100%;
            max-width: 400px;
        }
        
        .custom-button:hover {
            background-color: #00ff00;
            color: #000000;
            box-shadow: 0 0 20px #00ff00;
            transform: translateY(-2px);
        }

        /* Transitions */
        .fade-in {
            animation: fadeIn 1s ease-in forwards;
        }
        
        .fade-out {
            animation: fadeOut 1s ease-out forwards;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        </style>
    """, unsafe_allow_html=True)

  
    st.markdown("""
        <div class="game-container fade-in">
            <h1 class="game-title">MYSTIC REALMS</h1>
            <div style="font-family: 'VT323', monospace; font-size: 2em; color: #00ff00; text-align: center; margin: 2em 0;">
                In an age where magic fades and darkness rises...<br>
                A hero must emerge to reclaim the ancient powers.
            </div>
        </div>
    """, unsafe_allow_html=True)
    

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("BEGIN YOUR JOURNEY", key="begin_button", use_container_width=True):
            st.session_state.state_manager['previous_phase'] = 'intro'
            st.session_state.state_manager['game_phase'] = 'character_select'
            st.rerun()

def show_character_creation():
    """Display the character creation page with proper parameter handling."""
    st.markdown("""
        <style>
        .character-creation {
            background: linear-gradient(to bottom, #000000, #1a1a2e);
            padding: 2rem;
            border-radius: 10px;
            border: 2px solid #4a9eff;
            margin-bottom: 2rem;
        }
        .character-card {
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #4a9eff;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        .character-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(74, 158, 255, 0.3);
        }
        .input-field {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #4a9eff;
            color: white;
            padding: 0.5rem;
            border-radius: 4px;
        }
        .stat-value {
            color: #4a9eff;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("✨ Create Your Character")

    with st.container():
        # Step 1: Name Input
        player_name = st.text_input("Enter your name 🌟", key="player_name", 
                                  placeholder="Your adventurer's name...")

        if player_name:
            # Step 2: Class Selection
            st.subheader("Choose Your Class")
            
            class_stats = {
                "Knight": {"hp": 100, "attack": 15, "defense": 20},
                "Mage": {"hp": 80, "attack": 25, "defense": 10},
                "Archer": {"hp": 90, "attack": 20, "defense": 15}
            }

            selected_class = st.radio(
                "Select your class",
                options=["Knight", "Mage", "Archer"],
                format_func=lambda x: f"{x} {'⚔️' if x == 'Knight' else '🔮' if x == 'Mage' else '🏹'}"
            )

            # Display class stats
            st.markdown(f"""
                <div class='character-card'>
                    <h3>{selected_class} Stats</h3>
                    <p>HP: <span class='stat-value'>{class_stats[selected_class]['hp']}</span> ❤️</p>
                    <p>Attack: <span class='stat-value'>{class_stats[selected_class]['attack']}</span> ⚔️</p>
                    <p>Defense: <span class='stat-value'>{class_stats[selected_class]['defense']}</span> 🛡️</p>
                </div>
            """, unsafe_allow_html=True)

            # Step 3: Confirmation
            if st.button("Begin Adventure 🚀"):
                if initialize_game(selected_class, player_name):
                    st.session_state.state_manager['game_phase'] = 'game'
                    st.rerun()
                else:
                    st.error("Failed to initialize game. Please try again.")

def initialize_game(character_class, player_name):
    """Initialize the game state with the given character class and player name."""
    try:
        # Create the game world
        world = World()
        
        # Ensure quest_state is initialized
        if not hasattr(world, 'quest_state'):
            world.quest_state = {
                'sacred_grove_cleared': False,
                'shadow_temple_unlocked': False,
                'hidden_chamber_discovered': False,
                'final_boss_defeated': False
            }
        
        # Create basic world structure with all rooms first
        grove = Room("Sacred Grove", "A peaceful grove bathed in ethereal light. Ancient trees whisper secrets of forgotten magic.")
        temple = Room("Shadow Temple", "An ancient temple shrouded in darkness. Dark energies pulse within its walls.")
        cave = Room("Crystal Cave", "A cave filled with glowing crystals. The air hums with magical resonance.")
        hidden = Room("Hidden Chamber", "A mysterious chamber filled with ancient artifacts and forgotten treasures.")
        
        # Set up the world's rooms dictionary first
        world.rooms = {
            "Sacred Grove": grove,
            "Shadow Temple": temple,
            "Crystal Cave": cave,
            "Hidden Chamber": hidden
        }
        
        # Set starting room in world
        world.starting_room = grove
        world.current_room = grove
        
        # Set connections
        grove.add_exit("north", temple)
        temple.add_exit("south", grove)
        temple.add_exit("east", cave)
        cave.add_exit("west", temple)
        
        # Add NPCs
        forest_guardian = NPC("Forest Guardian", hp=100, attack_power=15, loot_gold=50, xp_reward=30, is_boss=True)
        shadow_knight = NPC("Shadow Knight", hp=150, attack_power=20, loot_gold=100, xp_reward=50, is_boss=True)
        cave_wyrm = NPC("Cave Wyrm", hp=120, attack_power=18, loot_gold=75, xp_reward=40, is_boss=True)
        
        # Add merchant with items
        merchant_inventory = {
            Item("Health Potion", "Restores 20 HP", "potion", 20): 50,
            Item("Iron Sword", "A basic sword", "weapon", 10): 100,
            Item("Leather Armor", "Basic protection", "armor", 5): 80,
            Item("Magic Staff", "A staff imbued with magic", "weapon", 15): 150
        }
        merchant = ShopNPC("Wandering Merchant", merchant_inventory)
        
        # Add NPCs to rooms
        grove.npcs.append(forest_guardian)
        grove.npcs.append(merchant)
        temple.npcs.append(shadow_knight)
        cave.npcs.append(cave_wyrm)
        
        # Add items to rooms
        grove.items.append(Item("Ancient Scroll", "A mysterious scroll with magical writings", "quest", 0))
        temple.items.append(Item("Shadow Essence", "A dark, swirling essence", "quest", 0))
        cave.items.append(Item("Crystal Shard", "A shard of pure magical crystal that resonates with hidden power", "quest", 0))
        hidden.items.append(Item("Legendary Sword", "A powerful ancient weapon", "weapon", 30))
        
        # Create the player with explicit current_room
        player = Player(player_name, grove)  # Use grove directly instead of world.starting_room
        player.current_room = grove  # Explicitly set current_room
        
        # Set class and initial stats
        if character_class == "Knight":
            player.player_class = "Knight"
            player.hp = 100
            player.gold = 50
            player.title = "Stalwart Knight"
        elif character_class == "Mage":
            player.player_class = "Mage"
            player.hp = 80
            player.gold = 75
            player.title = "Mystic Mage"
        elif character_class == "Archer":
            player.player_class = "Archer"
            player.hp = 90
            player.gold = 60
            player.title = "Swift Archer"
        
        # Initialize other player attributes
        player.discovered_rooms = {grove.name}  # Initialize with starting room
        player.inventory = []
        player.quests = {}
        player.status_effects = []
        player.weapon = None
        player.armor = None
        
        # Initialize game state
        if 'game_state' not in st.session_state:
            st.session_state.game_state = {}
        
        # Store game state
        st.session_state.game_state['world'] = world
        st.session_state.game_state['player'] = player
        st.session_state.game_state['current_room'] = grove  # Use grove directly
        st.session_state.game_state['initialization_time'] = time.time()
        st.session_state.game_state['discovered_secrets'] = set()
        st.session_state.game_state['combat_state'] = None
        st.session_state.game_state['shop_state'] = None
        
        # Update state manager
        st.session_state.state_manager['character_creation_completed'] = True
        st.session_state.state_manager['game_started'] = True
        st.session_state.state_manager['game_phase'] = 'game'
        
        return True
    except Exception as e:
        st.error(f"Error during game initialization: {str(e)}")
        return False

def game_interface():
    """Display the main game interface with state validation."""
    if 'game_state' not in st.session_state:
        st.error("⚠️ Game state was lost. Starting new game.")
        GameStateManager.reset()
        return

    try:
        # Get player and world from game state
        player = st.session_state.game_state.get('player')
        world = st.session_state.game_state.get('world')
        
        if not player or not world:
            raise ValueError("Player or world not found in game state")
            
        # Get current room from player object
        current_room = player.current_room
        if not current_room:
            raise ValueError("Player's current room not set")

        # Check for Crystal Shard in Crystal Cave
        if current_room.name == "Crystal Cave":
            crystal_shard = next((item for item in player.inventory if item.name == "Crystal Shard"), None)
            if crystal_shard and not world.quest_state.get('hidden_chamber_discovered', False):
                st.markdown("""
                    <div style='padding: 1rem; background: rgba(0,0,255,0.1); border-radius: 10px; border: 2px solid #4a9eff;'>
                        <h3>🔮 The Crystal Shard pulses with energy...</h3>
                        <p>You sense there might be more to discover in this cave. The shard seems to react to your surroundings.</p>
                    </div>
                """, unsafe_allow_html=True)

        # Handle Hidden Chamber special items
        if current_room.name == "Hidden Chamber":
            handle_hidden_chamber_items(player)

        # Initialize message log if it doesn't exist
        if 'message_log' not in st.session_state:
            st.session_state.message_log = []

        # Main game interface layout with two columns
        col1, col2 = st.columns([2, 1])

        # Status Bar in top right (col2)
        with col2:
            st.markdown("### 📊 Character Status")
            
            # Health Bar
            health_percent = (player.hp / (player.level * 100)) * 100
            st.markdown(f"""
                <div class="status-bar">
                    <div class="health-bar" style="width: {health_percent}%">
                        ❤️ HP: {player.hp}/{player.level * 100}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # XP Bar
            xp_percent = (player.xp / (player.level * 100)) * 100
            st.markdown(f"""
                <div class="status-bar">
                    <div class="xp-bar" style="width: {xp_percent}%">
                        ⭐ XP: {player.xp}/{player.level * 100}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="status-panel">
                    <div class="status-item">⚔️ Class: {player.player_class}</div>
                    <div class="status-item">👑 Level: {player.level}</div>
                    <div class="status-item">💰 Gold: {player.gold}</div>
                    <div class="status-item">🎯 Title: {player.title}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Inventory Section with improved layout
            st.markdown("### 🎒 Inventory")
            if player.inventory:
                for item in player.inventory:
                    # Create a single row with three columns for each item
                    item_cols = st.columns([3, 1, 1])
                    
                    # Item name and description
                    with item_cols[0]:
                        if hasattr(item, 'effect_value') and item.effect_value > 0:
                            st.write(f"📦 {item.name} (+{item.effect_value})")
                        else:
                            st.write(f"📦 {item.name}")
                    
                    # Use/Equip button
                    with item_cols[1]:
                        if st.button("Use", key=f"use_{item.name}"):
                            if hasattr(item, 'use'):
                                result = item.use(player)
                                player.inventory.remove(item)
                                add_to_message_log(result)
                                st.session_state.game_state['player'] = player  # Update player in game state
                                st.rerun()
                            elif item.item_type in ["weapon", "armor"]:
                                if item.item_type == "weapon":
                                    player.weapon = item
                                else:
                                    player.armor = item
                                add_to_message_log(f"Equipped {item.name}!")
                                st.session_state.game_state['player'] = player  # Update player in game state
                                st.rerun()
                    
                    # Drop button
                    with item_cols[2]:
                        if st.button("Drop", key=f"drop_{item.name}"):
                            player.inventory.remove(item)
                            current_room.items.append(item)
                            add_to_message_log(f"Dropped {item.name}")
                            st.rerun()
            else:
                st.write("Your inventory is empty")
            
            # Equipment
            st.markdown("### ⚔️ Equipment")
            st.write(f"Weapon: {player.weapon.name if player.weapon else 'None'}")
            st.write(f"Armor: {player.armor.name if player.armor else 'None'}")

            # Message Log at bottom right
            st.markdown("### 📜 Message Log")
            message_container = st.container()
            with message_container:
                for message in st.session_state.message_log[-10:]:  # Show last 10 messages
                    st.markdown(message)

        # Main Game Area (col1)
        with col1:
            # Room information
            st.markdown(f"""
                <div class="game-interface">
                    <h1 class="location-title">🏰 {current_room.name}</h1>
                    <p class="location-description">{current_room.description}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Navigation
            st.markdown("### 🧭 Available Exits")
            if current_room.exits:
                nav_cols = st.columns(len(current_room.exits))
                for i, (direction, room) in enumerate(current_room.exits.items()):
                    with nav_cols[i]:
                        if st.button(f"Go {direction.title()} ➡️", key=f"nav_{direction}"):
                            handle_movement(direction)
            
            # Items in room
            if current_room.items:
                st.markdown("### 🎁 Items in Room")
                for item in current_room.items:
                    col_item, col_action = st.columns([3, 1])
                    with col_item:
                        st.write(f"📦 {item.name}: {item.description}")
                    with col_action:
                        if st.button(f"Pick up {item.name}", key=f"pickup_{item.name}"):
                            player.inventory.append(item)
                            current_room.items.remove(item)
                            add_to_message_log(f"Picked up {item.name}")
                            st.rerun()
            
            # NPCs in room
            if current_room.npcs:
                st.markdown("### 👥 Characters Present")
                for npc in current_room.npcs:
                    col_npc, col_action = st.columns([3, 1])
                    with col_npc:
                        st.write(f"{npc.describe()}")
                    with col_action:
                        if isinstance(npc, ShopNPC):
                            if st.button("Trade 🛍️", key=f"trade_{npc.name}"):
                                st.session_state.game_state['shop_state'] = npc
                                st.rerun()
                        elif npc.is_alive():
                            if st.button("Attack ⚔️", key=f"attack_{npc.name}"):
                                st.session_state.game_state['combat_state'] = {'enemy': npc, 'turn': 0, 'log': []}
                                st.rerun()
        
        # Handle combat state - Badges appear in center
        if st.session_state.game_state.get('combat_state'):
            handle_combat_interface(st.session_state.game_state['combat_state'])
        
        # Handle shop state
        if st.session_state.game_state.get('shop_state'):
            handle_shop_interface(st.session_state.game_state['shop_state'])

        # Add custom CSS for status bars and badges
        st.markdown("""
            <style>
            .status-bar {
                width: 100%;
                height: 20px;
                background-color: #1a1a2e;
                border-radius: 10px;
                margin: 5px 0;
                overflow: hidden;
            }
            .health-bar {
                height: 100%;
                background: linear-gradient(90deg, #ff0000, #ff4444);
                border-radius: 10px;
                transition: width 0.3s ease;
                text-align: center;
                color: white;
                line-height: 20px;
            }
            .xp-bar {
                height: 100%;
                background: linear-gradient(90deg, #4a9eff, #4a4aff);
                border-radius: 10px;
                transition: width 0.3s ease;
                text-align: center;
                color: white;
                line-height: 20px;
            }
            .victory-badge {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(45deg, #00ff00, #00aa00);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 24px;
                margin: 20px 0;
                animation: badge-pop 0.5s ease-out;
                z-index: 1000;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            }
            .defeat-badge {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(45deg, #ff0000, #aa0000);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 24px;
                margin: 20px 0;
                animation: badge-pop 0.5s ease-out;
                z-index: 1000;
                box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            }
            @keyframes badge-pop {
                0% { transform: translate(-50%, -50%) scale(0); }
                70% { transform: translate(-50%, -50%) scale(1.1); }
                100% { transform: translate(-50%, -50%) scale(1); }
            }
            .game-interface {
                background: rgba(0, 0, 0, 0.7);
                padding: 20px;
                border-radius: 10px;
                border: 2px solid #4a9eff;
                margin-bottom: 20px;
            }
            .location-title {
                color: #4a9eff;
                text-shadow: 0 0 10px rgba(74, 158, 255, 0.5);
            }
            .location-description {
                color: #ffffff;
                font-size: 16px;
                line-height: 1.5;
            }
            </style>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error in game interface: {str(e)}")
        if st.button("🔄 Reset Game"):
            GameStateManager.reset()

def handle_combat_interface(combat_state):
    """Display combat interface and handle combat actions."""
    st.markdown("### ⚔️ Combat")
    enemy = combat_state['enemy']
    
    # Display combat status
    st.markdown(f"""
        <div class="combat-status">
            <h3>Battle with {enemy.name}</h3>
            <div>Enemy HP: {enemy.hp}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Combat actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Attack 🗡️"):
            handle_combat(enemy)
            st.rerun()
    with col2:
        if st.button("Flee 🏃"):
            st.session_state.game_state['combat_state'] = None
            st.success("You fled from combat!")
            st.rerun()
    
    # Combat log
    if combat_state['log']:
        st.markdown("### 📜 Combat Log")
        for entry in combat_state['log']:
            st.write(entry)

def handle_shop_interface(shop_npc):
    """Display shop interface and handle trading."""
    st.markdown("### 🛍️ Shop")
    
    # Display shop inventory
    st.markdown(shop_npc.list_items())
    
    # Buy items
    st.markdown("### 💰 Buy Items")
    for item, price in shop_npc.shop_inventory.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{item.name}: {price} gold")
        with col2:
            if st.button(f"Buy {item.name}", key=f"buy_{item.name}"):
                result = shop_npc.buy_from(st.session_state.game_state['player'], item.name)
                st.success(result)
                st.session_state.game_state['player'] = st.session_state.game_state['player']  # Update player in game state
                st.rerun()
    
    # Sell items
    st.markdown("### 💎 Sell Items")
    player = st.session_state.game_state['player']
    if player.inventory:
        for item in player.inventory:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{item.name}")
            with col2:
                if st.button(f"Sell {item.name}", key=f"sell_{item.name}"):
                    result = shop_npc.sell_to(player, item.name)
                    st.success(result)
                    st.session_state.game_state['player'] = player  # Update player in game state
                    st.rerun()
    
    if st.button("Leave Shop 🚶"):
        st.session_state.game_state['shop_state'] = None
        st.rerun()

def handle_movement(direction):
    """Handle player movement between rooms with error checking."""
    try:
        player = st.session_state.game_state['player']
        current_room = player.current_room
        world = st.session_state.game_state['world']

        # Check for Crystal Shard and reveal Hidden Chamber
        if current_room.name == "Crystal Cave":
            crystal_shard = next((item for item in player.inventory if item.name == "Crystal Shard"), None)
            if crystal_shard and not world.quest_state.get('hidden_chamber_discovered', False):
                world.quest_state['hidden_chamber_discovered'] = True
                hidden_chamber = world.rooms["Hidden Chamber"]
                current_room.add_exit("down", hidden_chamber)
                hidden_chamber.add_exit("up", current_room)
                add_to_message_log("🔮 The Crystal Shard resonates with the cave walls, revealing a hidden passage downward!")
                st.rerun()

        if direction not in current_room.exits:
            st.error("You cannot go that way.")
            return

        next_room = current_room.exits[direction]
        
        # Check for combat
        if st.session_state.game_state.get('combat_state'):
            st.error("Cannot move while in combat!")
            return

        # Special handling for Hidden Chamber entrance
        if next_room.name == "Hidden Chamber":
            show_hidden_chamber_entrance()
        
        # Special handling for exiting Hidden Chamber
        if current_room.name == "Hidden Chamber" and direction == "up":
            show_hidden_chamber_exit()

        # Move player
        player.current_room = next_room
        st.session_state.game_state['current_room'] = next_room

        # Process room entry
        entry_message = next_room.on_enter(player)
        if entry_message:
            st.success(entry_message)

        st.rerun()

    except Exception as e:
        st.error(f"Movement error: {str(e)}")

def show_hidden_chamber_entrance():
    """Display the animated entrance to the Hidden Chamber."""
    st.markdown("""
        <style>
        @keyframes doorOpen {
            0% { transform: scaleY(0); opacity: 0; }
            100% { transform: scaleY(1); opacity: 1; }
        }
        
        @keyframes glowPulse {
            0% { text-shadow: 0 0 10px #4a9eff; }
            50% { text-shadow: 0 0 20px #4a9eff, 0 0 30px #4a9eff; }
            100% { text-shadow: 0 0 10px #4a9eff; }
        }
        
        .chamber-entrance {
            background: linear-gradient(180deg, #000000, #1a1a2e);
            padding: 2rem;
            border-radius: 10px;
            border: 2px solid #4a9eff;
            margin: 2rem 0;
            animation: doorOpen 2s ease-out forwards;
            text-align: center;
        }
        
        .chamber-title {
            font-size: 2em;
            color: #4a9eff;
            animation: glowPulse 2s infinite;
            margin-bottom: 1rem;
        }
        
        .chamber-text {
            color: #ffffff;
            font-size: 1.2em;
            line-height: 1.6;
            margin: 1rem 0;
        }
        </style>
        
        <div class="chamber-entrance">
            <div class="chamber-title">🏛️ Ancient Hidden Chamber 🏛️</div>
            <div class="chamber-text">
                The crystal shard resonates with the cave walls, revealing an ancient doorway. 
                As you approach, mystical runes illuminate the path, their light dancing across the stone.
                <br><br>
                Legend speaks of this sacred place - a sanctuary of the Ancient Gods, where they stored 
                their most powerful artifacts. The very air crackles with divine energy.
                <br><br>
                The massive stone doors slowly part, revealing a chamber untouched by mortal hands for millennia...
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2)  # Pause for dramatic effect

def show_hidden_chamber_exit():
    """Display the animated exit from the Hidden Chamber."""
    st.markdown("""
        <style>
        @keyframes doorClose {
            0% { transform: scaleY(1); opacity: 1; }
            100% { transform: scaleY(0); opacity: 0; }
        }
        
        .chamber-exit {
            background: linear-gradient(180deg, #1a1a2e, #000000);
            padding: 2rem;
            border-radius: 10px;
            border: 2px solid #4a9eff;
            margin: 2rem 0;
            animation: doorClose 2s ease-in forwards;
            text-align: center;
        }
        </style>
        
        <div class="chamber-exit">
            <div class="chamber-title">🏛️ Departing the Sacred Ground 🏛️</div>
            <div class="chamber-text">
                As you ascend from the ancient chamber, the massive doors begin to close behind you.
                The magical runes fade, sealing the divine sanctuary once more.
                <br><br>
                The power of the gods' artifacts courses through you, their blessing evident in your enhanced strength.
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2)  # Pause for dramatic effect

def handle_hidden_chamber_items(player):
    """Handle the free items in the Hidden Chamber."""
    if 'hidden_chamber_visited' not in st.session_state:
        st.session_state.hidden_chamber_visited = False

    if not st.session_state.hidden_chamber_visited and player.current_room.name == "Hidden Chamber":
        st.markdown("""
            <div class="divine-items">
                <h2>🌟 Divine Artifacts 🌟</h2>
                <p>
                    Before you stand pedestals of pure light, each holding an artifact of immense power.
                    The gods themselves once wielded these weapons in their eternal battles.
                    Their power now awaits a worthy champion.
                </p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Take Divine Sword ⚔️"):
                divine_sword = Item("Divine Sword", 
                                  "A blade forged by the gods themselves", 
                                  "weapon", 50)
                player.inventory.append(divine_sword)
                add_to_message_log("🌟 You obtained the Divine Sword!")
                st.session_state.hidden_chamber_visited = True
                st.session_state.game_state['player'] = player  # Update player in game state
                st.rerun()

        with col2:
            if st.button("Take Divine Shield 🛡️"):
                divine_shield = Item("Divine Shield", 
                                   "A shield that once protected the gods", 
                                   "armor", 40)
                player.inventory.append(divine_shield)
                add_to_message_log("🌟 You obtained the Divine Shield!")
                st.session_state.hidden_chamber_visited = True
                st.session_state.game_state['player'] = player  # Update player in game state
                st.rerun()

        with col3:
            if st.button("Take Divine Elixir 🧪"):
                divine_elixir = Item("Divine Elixir", 
                                   "A potion containing the essence of the gods", 
                                   "potion", 100)
                player.inventory.append(divine_elixir)
                add_to_message_log("🌟 You obtained the Divine Elixir!")
                st.session_state.hidden_chamber_visited = True
                st.session_state.game_state['player'] = player  # Update player in game state
                st.rerun()

def handle_combat(enemy):
    """Handle combat interactions with enhanced state management and random damage."""
    if 'game_state' not in st.session_state:
        return

    game_state = st.session_state.game_state
    player = game_state['player']
    combat_state = game_state['combat_state']

    if not combat_state or not enemy.is_alive() or player.hp <= 0:
        game_state['combat_state'] = None
        return

    try:
        # Player turn with random damage
        base_damage = random.randint(3, 8) * player.level  # Random base damage scaled with level
        if player.weapon:
            base_damage += random.randint(1, player.weapon.effect_value)
        
        # Critical hit chance (10%)
        is_critical = random.random() < 0.1
        if is_critical:
            base_damage *= 2
            
        enemy.hp -= base_damage
        combat_state['log'].append(f"⚔️ You deal {base_damage} {'CRITICAL ' if is_critical else ''}damage to {enemy.name}!")
        combat_state['log'].append(f"👾 {enemy.name}'s HP: {max(0, enemy.hp)}")

        # Enemy turn if still alive
        if enemy.is_alive():
            # Boss special attack chance (30% for bosses)
            if enemy.is_boss and random.random() < 0.3:
                special_log = enemy.special_attack(player)
                if special_log:
                    combat_state['log'].append(special_log)
                    combat_state['log'].append(f"🧝‍♂️ Your HP: {max(0, player.hp)}")
            else:
                # Random enemy damage
                enemy_base_damage = random.randint(2, 6)
                if enemy.is_boss:
                    enemy_base_damage *= 1.5  # Bosses deal more damage
                
                # Apply armor reduction if player has armor
                if player.armor:
                    damage_reduction = min(enemy_base_damage * 0.3, player.armor.effect_value)
                    enemy_base_damage = max(1, enemy_base_damage - damage_reduction)
                    combat_state['log'].append(f"🛡️ Your armor absorbs {damage_reduction:.1f} damage!")
                
                player.hp -= enemy_base_damage
                combat_state['log'].append(f"💢 {enemy.name} deals {enemy_base_damage} damage to you!")
                combat_state['log'].append(f"🧝‍♂️ Your HP: {max(0, player.hp)}")

            # Process status effects
            status_log = process_status_effects(player, enemy)
            if status_log:
                combat_state['log'].extend(status_log)

        combat_state['turn'] += 1

        # Check combat end conditions
        if not enemy.is_alive():
            handle_combat_victory(player, enemy)
            game_state['combat_state'] = None
        elif player.hp <= 0:
            handle_player_defeat()
            game_state['combat_state'] = None

        # Update game state
        st.session_state.game_state = game_state

    except Exception as e:
        st.error(f"Combat error: {str(e)}")
        game_state['combat_state'] = None
        st.session_state.game_state = game_state

def process_status_effects(player, enemy):
    """Process status effects for both player and enemy."""
    log = []
    
    # Process player status effects
    player_status_log = player.apply_status_damage()
    if player_status_log:
        log.append(player_status_log)
    
    # Process enemy status effects
    if hasattr(enemy, 'process_status_effects'):
        enemy_status_log = enemy.process_status_effects()
        if enemy_status_log:
            log.append(enemy_status_log)
    
    return log

def handle_combat_victory(player, enemy):
    """Handle player victory in combat with enhanced rewards and victory badge."""
    game_state = st.session_state.game_state
    
    # Base rewards with random bonus
    gold_reward = enemy.loot_gold + random.randint(1, 20)
    xp_reward = enemy.xp_reward + random.randint(5, 15)

    # Bonus rewards for boss enemies
    if enemy.is_boss:
        gold_reward *= 2
        xp_reward *= 2
        
        # Special quest completion checks
        if enemy.name == "Ancient Dragon":
            player.quests["slay_dragon"] = True
            game_state['discovered_secrets'].add("Dragon Slayer")
            add_to_message_log("🎯 Quest Complete: Slay the Ancient Dragon!")
        elif enemy.name == "Shadow Knight":
            player.quests["found_amulet"] = True
            game_state['discovered_secrets'].add("Shadow Knight Defeated")
            add_to_message_log("🎯 Quest Complete: Defeat the Shadow Knight!")

    # Award loot and experience
    player.gold += gold_reward
    level_up_message = player.gain_xp(xp_reward)

    # Clear combat state
    game_state['combat_state'] = None
    
    # Clear combat-related status effects
    player.status_effects = [effect for effect in player.status_effects 
                           if effect not in ["Burning", "Poisoned", "Stunned"]]

    # Victory message with enhanced badge
    victory_message = f"""
    <div class="victory-badge">
        <div style="font-size: 48px;">🎉</div>
        <div style="font-size: 32px;">GLORIOUS VICTORY!</div>
        <div style="font-size: 24px;">You defeated {enemy.name}!</div>
        <div style="margin-top: 10px;">
            <span style="color: #ffd700;">+{gold_reward} Gold 💰</span><br>
            <span style="color: #00ff00;">+{xp_reward} XP ⭐</span>
        </div>
        <div style="font-size: 36px; margin-top: 10px;">⚔️ 🏆 ⚔️</div>
    </div>
    """
    st.markdown(victory_message, unsafe_allow_html=True)
    
    # Add to message log
    add_to_message_log(f"🎉 Victory! Defeated {enemy.name} (+{xp_reward} XP, +{gold_reward} gold)")
    if level_up_message:
        add_to_message_log(level_up_message)

def handle_player_defeat():
    """Handle player defeat in combat with enhanced defeat badge."""
    # Display enhanced defeat badge
    defeat_message = """
    <div class="defeat-badge">
        <div style="font-size: 48px;">💀</div>
        <div style="font-size: 32px;">DEFEATED!</div>
        <div style="font-size: 24px;">Your journey ends here...</div>
        <div style="margin-top: 10px; font-style: italic;">
            But legends never truly die!
        </div>
        <div style="font-size: 36px; margin-top: 10px;">⚔️ 🏰 ⚔️</div>
    </div>
    """
    st.markdown(defeat_message, unsafe_allow_html=True)
    
    # Lose some gold as penalty
    player = st.session_state.game_state['player']
    lost_gold = player.gold // 2
    player.gold -= lost_gold
    
    # Reset player state
    player.hp = player.level * 50  # Restore some HP based on level
    player.status_effects.clear()  # Clear status effects
    
    # Return to starting room
    player.current_room = st.session_state.game_state['world'].starting_room
    
    # Add to message log
    add_to_message_log(f"💀 Defeated! Lost {lost_gold} gold")
    add_to_message_log("🌟 Resurrected at the Sacred Grove")
    
    if st.button("Rise Again 🌟"):
        st.session_state.game_state['combat_state'] = None
        st.rerun()

def main():
    """Main game loop with strict state management."""
    # Initialize state manager if not already initialized
    GameStateManager.initialize()
    
    try:
        current_phase = st.session_state.state_manager.get('game_phase', 'intro')
        
        # Check if game is already started and initialized
        if st.session_state.state_manager.get('game_started', False) and st.session_state.get('game_state', {}).get('player'):
            game_interface()
            return
            
        # Handle different game phases
        if current_phase == 'intro':
            intro_sequence()
        elif current_phase == 'character_select':
            show_character_creation()
        elif current_phase == 'game':
            if not st.session_state.get('game_state', {}).get('player'):
                st.error("⚠️ Game state was lost. Starting new game.")
                reset_game_state()
            else:
                game_interface()
        else:
            # If no valid game phase is set, start from intro
            st.session_state.state_manager['game_phase'] = 'intro'
            st.rerun()
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        reset_game_state()

def reset_game_state():
    """Reset the game state to initial values."""
    st.session_state.clear()
    st.session_state.state_manager = {
        'initialized': True,
        'game_phase': 'intro',
        'previous_phase': None,
        'character_creation_completed': False,
        'game_started': False,
        'last_action_time': time.time()
    }
    st.rerun()

def add_to_message_log(message):
    """Add a message to the game's message log."""
    if 'message_log' not in st.session_state:
        st.session_state.message_log = []
    st.session_state.message_log.append(f"🕒 {message}")
    # Keep only the last 50 messages
    if len(st.session_state.message_log) > 50:
        st.session_state.message_log = st.session_state.message_log[-50:]

if __name__ == "__main__":
    main()
