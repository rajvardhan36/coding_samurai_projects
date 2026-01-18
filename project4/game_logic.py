"""
game_logic.py - Core game mechanics for number guessing
"""

import random
import json
import os
from datetime import datetime
from typing import Tuple, Optional, Dict, Any

class GameLogic:
    """Handles the core number guessing game logic"""
    
    DIFFICULTY_LEVELS = {
        "easy": {"range": (1, 50), "attempts": 10, "points": 10},
        "medium": {"range": (1, 100), "attempts": 7, "points": 20},
        "hard": {"range": (1, 200), "attempts": 5, "points": 50},
        "expert": {"range": (1, 500), "attempts": 3, "points": 100}
    }
    
    def __init__(self, player_name: str = "Player"):
        self.player_name = player_name
        self.difficulty = "medium"
        self.secret_number = None
        self.attempts_left = 0
        self.max_attempts = 0
        self.guesses = []
        self.game_start_time = None
        self.game_active = False
        self.score = 0
        self.stats_file = "game_stats.json"
        self.load_stats()
    
    def load_stats(self) -> None:
        """Load player statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            except:
                self.stats = {}
        else:
            self.stats = {}
    
    def save_stats(self) -> None:
        """Save player statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def set_difficulty(self, difficulty: str) -> bool:
        """Set game difficulty level"""
        if difficulty in self.DIFFICULTY_LEVELS:
            self.difficulty = difficulty
            return True
        return False
    
    def start_new_game(self) -> None:
        """Start a new game with current difficulty"""
        level = self.DIFFICULTY_LEVELS[self.difficulty]
        min_num, max_num = level["range"]
        
        self.secret_number = random.randint(min_num, max_num)
        self.max_attempts = level["attempts"]
        self.attempts_left = self.max_attempts
        self.guesses = []
        self.game_start_time = datetime.now()
        self.game_active = True
        self.score = 0
    
    def make_guess(self, guess: int) -> Dict[str, Any]:
        """Process a player's guess"""
        if not self.game_active:
            return {"error": "Game not active"}
        
        if guess in self.guesses:
            return {"error": "You already guessed this number"}
        
        self.attempts_left -= 1
        self.guesses.append(guess)
        
        # Calculate points for this guess
        base_points = self.DIFFICULTY_LEVELS[self.difficulty]["points"]
        points_earned = max(1, base_points // (len(self.guesses) * 2))
        
        if guess == self.secret_number:
            self.game_active = False
            self.score += points_earned * 2  # Bonus for correct guess
            
            # Record win
            self.record_game_result(win=True)
            
            return {
                "correct": True,
                "message": f"🎉 Correct! The number was {self.secret_number}",
                "attempts_used": len(self.guesses),
                "points_earned": points_earned * 2,
                "game_over": True
            }
        
        if self.attempts_left <= 0:
            self.game_active = False
            self.record_game_result(win=False)
            
            return {
                "correct": False,
                "message": f"💀 Game Over! The number was {self.secret_number}",
                "hint": self.get_hint(guess),
                "game_over": True
            }
        
        hint = self.get_hint(guess)
        self.score += points_earned
        
        return {
            "correct": False,
            "message": f"Not quite! {hint}",
            "hint": hint,
            "attempts_left": self.attempts_left,
            "points_earned": points_earned,
            "game_over": False
        }
    
    def get_hint(self, guess: int) -> str:
        """Provide hint based on the guess"""
        if guess < self.secret_number:
            difference = self.secret_number - guess
            if difference > 50:
                return "Way too low! Try much higher."
            elif difference > 20:
                return "Too low. Go higher."
            else:
                return "A bit low. Getting close!"
        else:
            difference = guess - self.secret_number
            if difference > 50:
                return "Way too high! Try much lower."
            elif difference > 20:
                return "Too high. Go lower."
            else:
                return "A bit high. Getting close!"
    
    def get_range(self) -> Tuple[int, int]:
        """Get current difficulty range"""
        level = self.DIFFICULTY_LEVELS[self.difficulty]
        return level["range"]
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state"""
        return {
            "secret_number": self.secret_number,
            "attempts_left": self.attempts_left,
            "max_attempts": self.max_attempts,
            "guesses": self.guesses.copy(),
            "difficulty": self.difficulty,
            "score": self.score,
            "game_active": self.game_active,
            "range": self.get_range()
        }
    
    def record_game_result(self, win: bool) -> None:
        """Record game result to statistics"""
        if self.player_name not in self.stats:
            self.stats[self.player_name] = {
                "total_games": 0,
                "wins": 0,
                "losses": 0,
                "best_score": 0,
                "games": []
            }
        
        player_stats = self.stats[self.player_name]
        player_stats["total_games"] += 1
        
        if win:
            player_stats["wins"] += 1
        else:
            player_stats["losses"] += 1
        
        if self.score > player_stats["best_score"]:
            player_stats["best_score"] = self.score
        
        game_record = {
            "timestamp": datetime.now().isoformat(),
            "difficulty": self.difficulty,
            "won": win,
            "score": self.score,
            "attempts_used": len(self.guesses),
            "secret_number": self.secret_number
        }
        
        player_stats["games"].append(game_record)
        
        # Keep only last 50 games
        if len(player_stats["games"]) > 50:
            player_stats["games"] = player_stats["games"][-50:]
        
        self.save_stats()
    
    def get_player_stats(self) -> Dict[str, Any]:
        """Get statistics for current player"""
        if self.player_name in self.stats:
            return self.stats[self.player_name].copy()
        return {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "best_score": 0,
            "games": []
        }