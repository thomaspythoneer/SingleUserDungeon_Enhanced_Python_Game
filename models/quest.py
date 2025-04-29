# models/quest.py

class Quest:
    def __init__(self, id, description, action, target, count, reward):
        self.id = id
        self.description = description
        self.action = action  # Example: 'kill', 'collect'
        self.target = target  # What object or enemy
        self.count = count
        self.progress = 0
        self.completed = False
        self.reward = reward  # {'gold': 100, 'xp': 50}

    def start(self, player):
        player.quests[self.id] = self
        return f"📝 New Quest Started: {self.description}"

    def advance(self, action, target, player):
        """Advance quest progress based on player actions."""
        if self.completed:
            return ""

        if self.action == action and self.target == target:
            self.progress += 1
            if self.progress >= self.count:
                return self.complete(player)
            else:
                return f"Quest Progress ({self.id}): {self.progress}/{self.count}"
        return ""

    def complete(self, player):
        """Mark quest completed and give rewards."""
        if self.completed:
            return ""  # Already completed

        self.completed = True
        reward_text = ""

        if 'gold' in self.reward:
            player.gold += self.reward['gold']
            reward_text += f"+{self.reward['gold']} gold "

        if 'xp' in self.reward:
            player.xp += self.reward['xp']
            reward_text += f"+{self.reward['xp']} XP "

        return f"✅ Quest '{self.description}' Completed! Rewards: {reward_text}"

    def show_status(self):
        """Return a readable status string for quest log."""
        status = "Completed" if self.completed else f"In Progress ({self.progress}/{self.count})"
        return f"[{self.id}] {self.description} - {status}"
