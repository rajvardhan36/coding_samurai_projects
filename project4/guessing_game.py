"""
guessing_game.py - Main GUI application using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import ttkbootstrap as tb  # For enhanced styling
from game_logic import GameLogic
from themes import GameThemes
from PIL import Image, ImageTk
import os

class NumberGuessingGame:
    """Main GUI application for number guessing game"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game - Coding Samurai")
        self.root.geometry("800x700")
        
        # Initialize game logic
        self.game = GameLogic()
        
        # Current theme
        self.current_theme = "dark"
        self.theme = GameThemes.get_theme(self.current_theme)
        
        # Configure styles
        self.setup_styles()
        
        # Create main container
        self.main_frame = tb.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initialize UI
        self.setup_ui()
        
        # Start with a new game
        self.start_new_game()
    
    def setup_styles(self):
        """Configure widget styles"""
        style = tb.Style(theme="darkly")  # Using ttkbootstrap for better styling
        
        # Custom font
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        self.big_font = font.Font(family="Helvetica", size=36, weight="bold")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tb.Label(
            self.main_frame,
            text="🎯 NUMBER GUESSING GAME",
            font=self.title_font,
            bootstyle="primary"
        )
        title_label.pack(pady=(0, 20))
        
        # Player info frame
        player_frame = tb.Frame(self.main_frame)
        player_frame.pack(fill="x", pady=(0, 10))
        
        tb.Label(player_frame, text="Player:", font=self.normal_font).pack(side="left", padx=5)
        
        self.player_entry = tb.Entry(
            player_frame,
            width=20,
            font=self.normal_font
        )
        self.player_entry.insert(0, self.game.player_name)
        self.player_entry.pack(side="left", padx=5)
        
        tb.Button(
            player_frame,
            text="Update Name",
            command=self.update_player_name,
            bootstyle="info"
        ).pack(side="left", padx=5)
        
        # Difficulty selector
        diff_frame = tb.Frame(self.main_frame)
        diff_frame.pack(fill="x", pady=10)
        
        tb.Label(diff_frame, text="Difficulty:", font=self.normal_font).pack(side="left", padx=5)
        
        self.difficulty_var = tk.StringVar(value=self.game.difficulty)
        difficulty_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty_var,
            values=list(GameLogic.DIFFICULTY_LEVELS.keys()),
            state="readonly",
            width=15,
            font=self.normal_font
        )
        difficulty_combo.pack(side="left", padx=5)
        difficulty_combo.bind("<<ComboboxSelected>>", self.change_difficulty)
        
        # Game info display
        info_frame = tb.LabelFrame(self.main_frame, text="Game Info", padx=10, pady=10)
        info_frame.pack(fill="x", pady=10)
        
        # Create info labels in a grid
        info_grid = tb.Frame(info_frame)
        info_grid.pack(fill="x")
        
        # Row 1
        tb.Label(info_grid, text="Range:", font=self.normal_font).grid(row=0, column=0, sticky="w", padx=5)
        self.range_label = tb.Label(info_grid, text="", font=self.normal_font)
        self.range_label.grid(row=0, column=1, sticky="w", padx=20)
        
        tb.Label(info_grid, text="Score:", font=self.normal_font).grid(row=0, column=2, sticky="w", padx=5)
        self.score_label = tb.Label(info_grid, text="0", font=self.normal_font, bootstyle="success")
        self.score_label.grid(row=0, column=3, sticky="w", padx=20)
        
        # Row 2
        tb.Label(info_grid, text="Attempts Left:", font=self.normal_font).grid(row=1, column=0, sticky="w", padx=5)
        self.attempts_label = tb.Label(info_grid, text="", font=self.normal_font)
        self.attempts_label.grid(row=1, column=1, sticky="w", padx=20)
        
        tb.Label(info_grid, text="Best Score:", font=self.normal_font).grid(row=1, column=2, sticky="w", padx=5)
        self.best_score_label = tb.Label(info_grid, text="0", font=self.normal_font, bootstyle="warning")
        self.best_score_label.grid(row=1, column=3, sticky="w", padx=20)
        
        # Guess input area
        guess_frame = tb.Frame(self.main_frame)
        guess_frame.pack(pady=20)
        
        tb.Label(guess_frame, text="Enter your guess:", font=self.normal_font).pack()
        
        self.guess_var = tk.StringVar()
        self.guess_entry = tb.Entry(
            guess_frame,
            textvariable=self.guess_var,
            width=10,
            font=self.big_font,
            justify="center"
        )
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind("<Return>", lambda e: self.submit_guess())
        
        # Submit button
        self.submit_button = tb.Button(
            guess_frame,
            text="Submit Guess",
            command=self.submit_guess,
            bootstyle="success",
            width=15
        )
        self.submit_button.pack(pady=5)
        
        # Feedback display
        feedback_frame = tb.LabelFrame(self.main_frame, text="Feedback", padx=10, pady=10)
        feedback_frame.pack(fill="both", expand=True, pady=10)
        
        self.feedback_text = tk.Text(
            feedback_frame,
            height=8,
            width=60,
            font=("Courier", 10),
            wrap="word",
            state="disabled"
        )
        self.feedback_text.pack(fill="both", expand=True)
        
        # Control buttons
        control_frame = tb.Frame(self.main_frame)
        control_frame.pack(pady=10)
        
        tb.Button(
            control_frame,
            text="🔄 New Game",
            command=self.start_new_game,
            bootstyle="primary"
        ).pack(side="left", padx=5)
        
        tb.Button(
            control_frame,
            text="📊 Stats",
            command=self.show_stats,
            bootstyle="info"
        ).pack(side="left", padx=5)
        
        tb.Button(
            control_frame,
            text="🎨 Theme",
            command=self.change_theme,
            bootstyle="secondary"
        ).pack(side="left", padx=5)
        
        tb.Button(
            control_frame,
            text="❓ Hint",
            command=self.show_hint_info,
            bootstyle="warning"
        ).pack(side="left", padx=5)
        
        tb.Button(
            control_frame,
            text="❌ Exit",
            command=self.root.quit,
            bootstyle="danger"
        ).pack(side="left", padx=5)
    
    def update_player_name(self):
        """Update player name"""
        name = self.player_entry.get().strip()
        if name:
            self.game.player_name = name
            messagebox.showinfo("Success", f"Player name updated to: {name}")
            self.update_stats_display()
    
    def change_difficulty(self, event=None):
        """Change game difficulty"""
        difficulty = self.difficulty_var.get()
        if self.game.set_difficulty(difficulty):
            messagebox.showinfo("Difficulty Changed", 
                              f"Difficulty set to: {difficulty.capitalize()}\n"
                              f"Starting new game...")
            self.start_new_game()
    
    def start_new_game(self):
        """Start a new game"""
        self.game.start_new_game()
        self.guess_var.set("")
        self.guess_entry.focus()
        self.update_game_display()
        self.clear_feedback()
        self.add_feedback("🎮 New game started!", "info")
        self.add_feedback(f"Guess a number between {self.game.get_range()[0]} and {self.game.get_range()[1]}", "info")
    
    def submit_guess(self):
        """Submit the current guess"""
        try:
            guess = int(self.guess_var.get())
            min_num, max_num = self.game.get_range()
            
            if guess < min_num or guess > max_num:
                messagebox.showerror("Invalid Guess", 
                                   f"Please enter a number between {min_num} and {max_num}")
                return
            
            result = self.game.make_guess(guess)
            
            if "error" in result:
                messagebox.showerror("Error", result["error"])
                return
            
            # Display feedback
            if result["correct"]:
                self.add_feedback(result["message"], "correct")
                self.add_feedback(f"🎉 You guessed it in {len(self.game.guesses)} attempts!", "correct")
                self.add_feedback(f"🏆 Points earned: {result['points_earned']}", "correct")
            else:
                self.add_feedback(f"Guess #{len(self.game.guesses)}: {guess} - {result['message']}", 
                                "incorrect" if result['game_over'] else "hint")
            
            # Update display
            self.update_game_display()
            self.guess_var.set("")
            
            if result.get("game_over", False):
                self.submit_button.config(state="disabled")
                if not result["correct"]:
                    self.add_feedback("💀 Game Over! Try again.", "incorrect")
            else:
                self.add_feedback(f"📉 {result['hint']}", "hint")
                
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_game_display(self):
        """Update all game information displays"""
        state = self.game.get_game_state()
        
        # Update labels
        self.range_label.config(text=f"{state['range'][0]} - {state['range'][1]}")
        self.score_label.config(text=str(state['score']))
        self.attempts_label.config(text=f"{state['attempts_left']}/{state['max_attempts']}")
        
        # Update attempts label color based on remaining attempts
        if state['attempts_left'] <= 2:
            self.attempts_label.config(bootstyle="danger")
        elif state['attempts_left'] <= state['max_attempts'] // 2:
            self.attempts_label.config(bootstyle="warning")
        else:
            self.attempts_label.config(bootstyle="success")
        
        # Update best score
        stats = self.game.get_player_stats()
        self.best_score_label.config(text=str(stats.get('best_score', 0)))
        
        # Enable/disable submit button
        self.submit_button.config(state="normal" if state['game_active'] else "disabled")
    
    def update_stats_display(self):
        """Update statistics display"""
        stats = self.game.get_player_stats()
        self.best_score_label.config(text=str(stats.get('best_score', 0)))
    
    def add_feedback(self, message: str, msg_type: str = "info"):
        """Add message to feedback display"""
        self.feedback_text.config(state="normal")
        
        # Configure tags for different message types
        for tag in ["info", "correct", "incorrect", "hint"]:
            if tag not in self.feedback_text.tag_names():
                self.feedback_text.tag_config(tag, foreground=self.theme[tag])
        
        # Insert message
        self.feedback_text.insert("end", message + "\n", msg_type)
        self.feedback_text.see("end")
        self.feedback_text.config(state="disabled")
    
    def clear_feedback(self):
        """Clear the feedback display"""
        self.feedback_text.config(state="normal")
        self.feedback_text.delete(1.0, "end")
        self.feedback_text.config(state="disabled")
    
    def show_stats(self):
        """Show player statistics in a new window"""
        stats = self.game.get_player_stats()
        
        stats_window = tb.Toplevel(self.root)
        stats_window.title("Player Statistics")
        stats_window.geometry("500x400")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Summary tab
        summary_frame = tb.Frame(notebook)
        notebook.add(summary_frame, text="Summary")
        
        summary_text = f"""
        📊 PLAYER STATISTICS: {self.game.player_name}
        {'='*40}
        
        🎮 Total Games: {stats['total_games']}
        ✅ Wins: {stats['wins']}
        ❌ Losses: {stats['losses']}
        📈 Win Rate: {(stats['wins']/stats['total_games']*100) if stats['total_games'] > 0 else 0:.1f}%
        🏆 Best Score: {stats['best_score']}
        
        {'='*40}
        
        Last 5 Games:
        """
        
        # Add recent games
        for i, game in enumerate(reversed(stats['games'][-5:])):
            result = "✅ Won" if game['won'] else "❌ Lost"
            summary_text += f"\n{i+1}. {game['timestamp'][:16]} - {result} (Score: {game['score']})"
        
        summary_label = tb.Label(summary_frame, text=summary_text, justify="left", font=("Courier", 10))
        summary_label.pack(padx=10, pady=10)
    
    def change_theme(self):
        """Change application theme"""
        # Simple theme cycling
        themes = GameThemes.get_theme_names()
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.current_theme = themes[next_index]
        self.theme = GameThemes.get_theme(self.current_theme)
        
        # Update colors (simplified - in a real app you'd update all widgets)
        self.root.configure(bg=self.theme['bg'])
        messagebox.showinfo("Theme Changed", f"Theme changed to: {self.current_theme.capitalize()}")
    
    def show_hint_info(self):
        """Show hint information"""
        hint_info = """
        💡 HINT SYSTEM:
        
        Based on your guess, you'll get one of these hints:
        
        • "Way too low/high" - More than 50 away
        • "Too low/high" - Between 20-50 away
        • "A bit low/high" - Less than 20 away
        
        📝 TIPS:
        1. Start with the middle number of the range
        2. Use binary search strategy
        3. Pay attention to the hint messages
        4. Try different difficulty levels
        
        Good luck! 🍀
        """
        
        messagebox.showinfo("Hint System", hint_info)

def main():
    """Main function to run the application"""
    # Try to use ttkbootstrap for enhanced styling
    try:
        import ttkbootstrap as tb
        root = tb.Window(themename="darkly")
    except ImportError:
        # Fall back to regular tkinter
        root = tk.Tk()
        root.style = ttk.Style()
        root.style.theme_use("clam")
    
    # Create and run the game
    app = NumberGuessingGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()