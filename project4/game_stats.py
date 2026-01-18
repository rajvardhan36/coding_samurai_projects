"""
game_stats.py - Game statistics tracking
"""

class GameStats:
    """Manages game statistics"""
    
    def __init__(self):
        self.stats = {}
    
    def record_game(self, player_name, result):
        """Record a game result"""
        if player_name not in self.stats:
            self.stats[player_name] = []
        self.stats[player_name].append(result)
    
    def get_stats(self, player_name):
        """Get stats for a player"""
        return self.stats.get(player_name, [])
