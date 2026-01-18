"""
test_game.py - Unit tests for the Number Guessing Game
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open
import json
from datetime import datetime

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_logic import GameLogic
from utils import format_wind_direction, get_weather_icon

class TestGameLogic(unittest.TestCase):
    """Test cases for GameLogic class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.game = GameLogic("TestPlayer")
        self.game.stats = {}  # Clear stats for testing
    
    def test_initialization(self):
        """Test game initialization"""
        self.assertEqual(self.game.player_name, "TestPlayer")
        self.assertEqual(self.game.difficulty, "medium")
        self.assertFalse(self.game.game_active)
        self.assertEqual(self.game.score, 0)
    
    def test_set_difficulty_valid(self):
        """Test setting valid difficulty levels"""
        self.assertTrue(self.game.set_difficulty("easy"))
        self.assertEqual(self.game.difficulty, "easy")
        
        self.assertTrue(self.game.set_difficulty("hard"))
        self.assertEqual(self.game.difficulty, "hard")
    
    def test_set_difficulty_invalid(self):
        """Test setting invalid difficulty"""
        self.assertFalse(self.game.set_difficulty("impossible"))
        self.assertEqual(self.game.difficulty, "medium")  # Should remain default
    
    def test_start_new_game(self):
        """Test starting a new game"""
        self.game.set_difficulty("easy")
        self.game.start_new_game()
        
        # Check game state
        self.assertTrue(self.game.game_active)
        self.assertEqual(self.game.attempts_left, 10)  # Easy has 10 attempts
        self.assertEqual(self.game.max_attempts, 10)
        self.assertEqual(len(self.game.guesses), 0)
        self.assertIsNotNone(self.game.secret_number)
        
        # Check number is in range
        min_num, max_num = self.game.get_range()
        self.assertGreaterEqual(self.game.secret_number, min_num)
        self.assertLessEqual(self.game.secret_number, max_num)
    
    def test_get_range(self):
        """Test getting range for each difficulty"""
        test_cases = [
            ("easy", (1, 50)),
            ("medium", (1, 100)),
            ("hard", (1, 200)),
            ("expert", (1, 500))
        ]
        
        for difficulty, expected_range in test_cases:
            with self.subTest(difficulty=difficulty):
                self.game.set_difficulty(difficulty)
                self.assertEqual(self.game.get_range(), expected_range)
    
    @patch('game_logic.random.randint')
    def test_make_guess_correct(self, mock_randint):
        """Test making a correct guess"""
        # Set up mock secret number
        mock_randint.return_value = 42
        self.game.start_new_game()
        
        # Make correct guess
        result = self.game.make_guess(42)
        
        # Verify result
        self.assertTrue(result["correct"])
        self.assertIn("🎉 Correct!", result["message"])
        self.assertFalse(self.game.game_active)  # Game should end
        self.assertEqual(self.game.score, 20)  # 10 * 2 for correct guess
        self.assertIn(42, self.game.guesses)
    
    @patch('game_logic.random.randint')
    def test_make_guess_too_low(self, mock_randint):
        """Test making a guess that's too low"""
        mock_randint.return_value = 50
        self.game.start_new_game()
        
        result = self.game.make_guess(10)
        
        # Verify result
        self.assertFalse(result["correct"])
        self.assertIn("low", result["message"].lower())
        self.assertTrue(self.game.game_active)  # Game should continue
        self.assertEqual(self.game.attempts_left, 6)  # 7-1 for medium difficulty
        self.assertIn(10, self.game.guesses)
    
    @patch('game_logic.random.randint')
    def test_make_guess_too_high(self, mock_randint):
        """Test making a guess that's too high"""
        mock_randint.return_value = 10
        self.game.start_new_game()
        
        result = self.game.make_guess(90)
        
        # Verify result
        self.assertFalse(result["correct"])
        self.assertIn("high", result["message"].lower())
        self.assertTrue(self.game.game_active)
    
    @patch('game_logic.random.randint')
    def test_make_guess_game_over(self, mock_randint):
        """Test running out of attempts"""
        mock_randint.return_value = 42
        self.game.set_difficulty("expert")  # Only 3 attempts
        self.game.start_new_game()
        
        # Make wrong guesses until game over
        results = []
        for guess in [10, 20, 30]:
            results.append(self.game.make_guess(guess))
        
        # Last guess should end game
        self.assertFalse(self.game.game_active)
        self.assertTrue(results[-1]["game_over"])
        self.assertIn("Game Over", results[-1]["message"])
    
    def test_make_guess_duplicate(self):
        """Test making duplicate guess"""
        self.game.start_new_game()
        self.game.make_guess(10)
        
        # Try same guess again
        result = self.game.make_guess(10)
        
        self.assertIn("error", result)
        self.assertIn("already guessed", result["error"])
    
    def test_make_guess_game_not_active(self):
        """Test guessing when game is not active"""
        self.game.game_active = False
        result = self.game.make_guess(10)
        
        self.assertIn("error", result)
        self.assertIn("Game not active", result["error"])
    
    def test_get_hint(self):
        """Test hint generation"""
        self.game.secret_number = 50
        
        test_cases = [
            (10, "Way too low"),  # 40 away
            (30, "Too low"),      # 20 away
            (45, "A bit low"),    # 5 away
            (55, "A bit high"),   # 5 away
            (70, "Too high"),     # 20 away
            (90, "Way too high")  # 40 away
        ]
        
        for guess, expected_hint in test_cases:
            with self.subTest(guess=guess):
                hint = self.game.get_hint(guess)
                self.assertIn(expected_hint, hint)
    
    def test_get_game_state(self):
        """Test getting game state"""
        self.game.start_new_game()
        state = self.game.get_game_state()
        
        expected_keys = [
            "secret_number", "attempts_left", "max_attempts",
            "guesses", "difficulty", "score", "game_active", "range"
        ]
        
        for key in expected_keys:
            self.assertIn(key, state)
        
        self.assertEqual(state["difficulty"], "medium")
        self.assertEqual(state["attempts_left"], 7)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_stats(self, mock_json_load, mock_file):
        """Test loading statistics from file"""
        # Mock data to return
        mock_stats = {
            "TestPlayer": {
                "total_games": 10,
                "wins": 7,
                "losses": 3,
                "best_score": 150
            }
        }
        mock_json_load.return_value = mock_stats
        
        # Create new game instance (will load stats)
        game = GameLogic("TestPlayer")
        
        self.assertEqual(game.stats, mock_stats)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_stats(self, mock_json_dump, mock_file):
        """Test saving statistics to file"""
        # Add some stats
        self.game.stats = {"TestPlayer": {"total_games": 5}}
        
        # Trigger save
        self.game.save_stats()
        
        # Verify json.dump was called
        mock_json_dump.assert_called_once()
    
    @patch('game_logic.datetime')
    def test_record_game_result(self, mock_datetime):
        """Test recording game results"""
        # Mock current time
        mock_now = datetime(2024, 1, 15, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        
        # Set up game
        self.game.score = 100
        self.game.difficulty = "medium"
        self.game.secret_number = 42
        self.game.guesses = [10, 20, 30, 42]
        
        # Record win
        self.game.record_game_result(win=True)
        
        # Verify stats
        self.assertIn("TestPlayer", self.game.stats)
        player_stats = self.game.stats["TestPlayer"]
        
        self.assertEqual(player_stats["total_games"], 1)
        self.assertEqual(player_stats["wins"], 1)
        self.assertEqual(player_stats["losses"], 0)
        self.assertEqual(player_stats["best_score"], 100)
        self.assertEqual(len(player_stats["games"]), 1)
        
        game_record = player_stats["games"][0]
        self.assertEqual(game_record["won"], True)
        self.assertEqual(game_record["score"], 100)
        self.assertEqual(game_record["attempts_used"], 4)
    
    def test_get_player_stats_new_player(self):
        """Test getting stats for new player"""
        stats = self.game.get_player_stats()
        
        expected_stats = {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "best_score": 0,
            "games": []
        }
        
        self.assertEqual(stats, expected_stats)
    
    def test_get_player_stats_existing_player(self):
        """Test getting stats for existing player"""
        # Add stats first
        self.game.stats = {
            "TestPlayer": {
                "total_games": 5,
                "wins": 3,
                "losses": 2,
                "best_score": 80,
                "games": [{"score": 80}]
            }
        }
        
        stats = self.game.get_player_stats()
        
        self.assertEqual(stats["total_games"], 5)
        self.assertEqual(stats["best_score"], 80)
        self.assertEqual(len(stats["games"]), 1)

class TestHintPrecision(unittest.TestCase):
    """Test hint precision based on distance"""
    
    def test_hint_precision_ranges(self):
        """Test that hints are accurate based on distance"""
        game = GameLogic()
        game.secret_number = 100
        
        # Test exact boundaries
        test_cases = [
            (49, "Way too low"),   # 51 away
            (50, "Too low"),       # 50 away (boundary)
            (79, "Too low"),       # 21 away
            (80, "A bit low"),     # 20 away (boundary)
            (99, "A bit low"),     # 1 away
            (100, ""),             # Correct (won't reach hint)
            (101, "A bit high"),   # 1 away
            (120, "Too high"),     # 20 away (boundary)
            (121, "Too high"),     # 21 away
            (150, "Way too high"), # 50 away (boundary)
            (151, "Way too high")  # 51 away
        ]
        
        for guess, expected in test_cases:
            with self.subTest(guess=guess):
                if guess != 100:  # Skip correct guess
                    hint = game.get_hint(guess)
                    if expected:  # Non-empty expected hint
                        self.assertIn(expected, hint)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""
    
    def test_min_max_range(self):
        """Test guessing at range boundaries"""
        game = GameLogic()
        game.set_difficulty("easy")  # Range 1-50
        
        # Mock secret number at boundaries
        with patch('game_logic.random.randint') as mock_rand:
            # Test minimum
            mock_rand.return_value = 1
            game.start_new_game()
            result = game.make_guess(1)
            self.assertTrue(result["correct"])
            
            # Test maximum
            mock_rand.return_value = 50
            game.start_new_game()
            result = game.make_guess(50)
            self.assertTrue(result["correct"])
    
    def test_negative_input_handling(self):
        """Test handling negative numbers (should be caught by validation)"""
        game = GameLogic()
        game.start_new_game()
        
        # This should be caught by validation in the GUI
        # But game logic should handle it gracefully
        result = game.make_guess(-10)
        self.assertFalse(result.get("correct", True))
    
    def test_out_of_range_guess(self):
        """Test guessing outside valid range"""
        game = GameLogic()
        game.set_difficulty("easy")  # Range 1-50
        game.start_new_game()
        
        # Guess outside range
        result = game.make_guess(100)
        self.assertFalse(result["correct"])
        # Hint should still work
        self.assertIn("high", result.get("hint", "").lower())


class TestScoreCalculation(unittest.TestCase):
    """Test score calculation logic"""
    
    @patch('game_logic.random.randint')
    def test_score_for_correct_guess(self, mock_randint):
        """Test score calculation for correct guess"""
        mock_randint.return_value = 42
        
        # Test each difficulty
        difficulties = ["easy", "medium", "hard", "expert"]
        base_points = [10, 20, 50, 100]
        
        for diff, base in zip(difficulties, base_points):
            with self.subTest(difficulty=diff):
                game = GameLogic()
                game.set_difficulty(diff)
                game.start_new_game()
                
                # Correct guess on first try
                result = game.make_guess(42)
                
                # Score should be base * 2 for correct guess
                expected_score = base * 2
                self.assertEqual(game.score, expected_score)
                self.assertEqual(result.get("points_earned"), expected_score)
    
    @patch('game_logic.random.randint')
    def test_score_for_multiple_guesses(self, mock_randint):
        """Test score accumulation over multiple guesses"""
        mock_randint.return_value = 42
        game = GameLogic()
        game.set_difficulty("medium")  # Base 20 points
        game.start_new_game()
        
        # Make wrong guesses
        game.make_guess(10)  # Should earn ~10 points (20 / 2)
        game.make_guess(20)  # Should earn ~5 points (20 / 4)
        game.make_guess(30)  # Should earn ~3 points (20 / 6)
        
        # Final correct guess
        result = game.make_guess(42)  # Should earn ~7 * 2 points (20 / 8 * 2)
        
        # Total should be sum of all
        self.assertGreater(game.score, 0)
        self.assertGreater(result.get("points_earned", 0), 0)


class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_format_wind_direction(self):
        """Test wind direction formatting"""
        # Test cardinal directions
        self.assertEqual(format_wind_direction(0), "N")
        self.assertEqual(format_wind_direction(90), "E")
        self.assertEqual(format_wind_direction(180), "S")
        self.assertEqual(format_wind_direction(270), "W")
        
        # Test intermediate directions
        self.assertEqual(format_wind_direction(45), "NE")
        self.assertEqual(format_wind_direction(135), "SE")
        self.assertEqual(format_wind_direction(225), "SW")
        self.assertEqual(format_wind_direction(315), "NW")
        
        # Test wrap-around
        self.assertEqual(format_wind_direction(360), "N")
        self.assertEqual(format_wind_direction(720), "N")  # Two full circles
    
    def test_get_weather_icon(self):
        """Test weather icon selection"""
        # Test specific codes
        self.assertEqual(get_weather_icon(0), "☀️")   # Clear
        self.assertEqual(get_weather_icon(1), "🌤️")   # Mainly clear
        self.assertEqual(get_weather_icon(3), "☁️")   # Overcast
        self.assertEqual(get_weather_icon(95), "⛈️")  # Thunderstorm
        
        # Test ranges
        self.assertEqual(get_weather_icon(45), "🌫️")   # Fog
        self.assertEqual(get_weather_icon(61), "🌧️")   # Rain
        self.assertEqual(get_weather_icon(71), "❄️")   # Snow
        
        # Test default
        self.assertEqual(get_weather_icon(999), "🌡️")  # Default


class TestIntegration(unittest.TestCase):
    """Integration tests for game flow"""
    
    def test_complete_game_flow(self):
        """Test a complete game from start to finish"""
        game = GameLogic("IntegrationTest")
        
        # Set difficulty and start
        game.set_difficulty("easy")
        game.start_new_game()
        
        # Get initial state
        initial_state = game.get_game_state()
        self.assertTrue(initial_state["game_active"])
        self.assertEqual(initial_state["attempts_left"], 10)
        
        # Play until win (we'll cheat by knowing the number)
        secret = initial_state["secret_number"]
        result = game.make_guess(secret)
        
        # Should win
        self.assertTrue(result["correct"])
        self.assertFalse(game.game_active)
        
        # Check stats were recorded
        stats = game.get_player_stats()
        self.assertEqual(stats["total_games"], 1)
        self.assertEqual(stats["wins"], 1)
    
    def test_game_state_persistence(self):
        """Test that game state is maintained during play"""
        game = GameLogic()
        game.start_new_game()
        
        # Store initial state
        secret = game.secret_number
        initial_attempts = game.attempts_left
        
        # Make a guess
        guess = secret - 10 if secret > 10 else secret + 10
        game.make_guess(guess)
        
        # State should be updated
        self.assertEqual(game.attempts_left, initial_attempts - 1)
        self.assertIn(guess, game.guesses)
        self.assertTrue(game.game_active)  # Still playing
        
        # Make correct guess
        result = game.make_guess(secret)
        self.assertTrue(result["correct"])
        self.assertFalse(game.game_active)


# Mock classes for testing UI components
class MockTkinterWidget:
    """Mock Tkinter widget for testing"""
    def __init__(self):
        self.text = ""
        self.state = "normal"
        self.config_calls = []
    
    def config(self, **kwargs):
        self.config_calls.append(kwargs)
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'state' in kwargs:
            self.state = kwargs['state']
    
    def insert(self, index, text, tags=None):
        self.text += text
    
    def delete(self, start, end):
        self.text = ""


class TestUIMocks(unittest.TestCase):
    """Test UI-related functionality with mocks"""
    
    def test_feedback_display(self):
        """Test feedback display logic"""
        # Create mock text widget
        mock_text = MockTkinterWidget()
        
        # Simulate adding feedback
        test_messages = [
            ("Game started", "info"),
            ("Too low", "hint"),
            ("Correct!", "correct")
        ]
        
        for msg, msg_type in test_messages:
            mock_text.insert("end", f"{msg}\n", msg_type)
        
        # Verify text was added
        self.assertIn("Game started", mock_text.text)
        self.assertIn("Correct!", mock_text.text)
    
    def test_ui_state_updates(self):
        """Test UI state updates"""
        # Create mock labels
        mock_score_label = MockTkinterWidget()
        mock_attempts_label = MockTkinterWidget()
        
        # Simulate game state changes
        mock_score_label.config(text="100")
        mock_attempts_label.config(text="3/7")
        
        # Verify updates
        self.assertEqual(mock_score_label.text, "100")
        self.assertEqual(mock_attempts_label.text, "3/7")
        
        # Test disabled state
        mock_button = MockTkinterWidget()
        mock_button.config(state="disabled")
        self.assertEqual(mock_button.state, "disabled")


def run_tests():
    """Run all tests and print results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGameLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestHintPrecision))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestScoreCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestUIMocks))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run tests when script is executed directly
    success = run_tests()
    sys.exit(0 if success else 1)