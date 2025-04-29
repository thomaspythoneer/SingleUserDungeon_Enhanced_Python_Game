# models/shop_npc.py

from models.npc import NPC

class ShopNPC(NPC):
    def __init__(self, name, shop_inventory):
        # Shop NPC is a non-combatant: 100 hp, 0 attack, no loot
        super().__init__(name=name, hp=100, attack_power=0, loot_gold=0, xp_reward=0, is_boss=False)
        self.shop_inventory = shop_inventory  # Dictionary: {Item: price}

    def list_items(self):
        """List items available for sale."""
        if not self.shop_inventory:
            return "This shop has nothing in stock."
        
        shop_list = "\n🛒 Items for Sale:\n"
        for item, price in self.shop_inventory.items():
            shop_list += f"- {item.name}: {price} gold\n"
        return shop_list

    def buy_from(self, player, item_name):
        """Player buys an item from the shop."""
        for item, price in self.shop_inventory.items():
            if item.name.lower() == item_name.lower():
                if player.gold >= price:
                    player.gold -= price
                    player.inventory.append(item)
                    return f"✅ You bought {item.name} for {price} gold."
                else:
                    return "❌ You don't have enough gold."
        return "❓ That item is not sold here."

    def sell_to(self, player, item_name):
        """Player sells an item to the shopkeeper."""
        for item in player.inventory:
            if item.name.lower() == item_name.lower():
                sell_price = 10  # Default fixed sell price
                if hasattr(item, "value"):  # Allow better dynamic prices later
                    sell_price = item.value // 2  # Half value if value attribute exists

                player.gold += sell_price
                player.inventory.remove(item)
                return f"💰 You sold {item.name} for {sell_price} gold."
        return "❌ You don't have that item in your inventory."

    def describe(self):
        """Override the default NPC description for shopkeepers."""
        return f"{self.name} - Shopkeeper"
