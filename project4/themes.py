"""
themes.py - GUI themes and styling
"""

class GameThemes:
    """Defines color themes for the game"""
    
    THEMES = {
        "dark": {
            "bg": "#2c3e50",
            "fg": "#ecf0f1",
            "button_bg": "#3498db",
            "button_fg": "white",
            "button_hover": "#2980b9",
            "entry_bg": "#34495e",
            "entry_fg": "white",
            "text_bg": "#34495e",
            "correct": "#2ecc71",
            "incorrect": "#e74c3c",
            "hint": "#f39c12",
            "title": "#1abc9c",
            "info": "#3498db"
        },
        "light": {
            "bg": "#f8f9fa",
            "fg": "#212529",
            "button_bg": "#007bff",
            "button_fg": "white",
            "button_hover": "#0056b3",
            "entry_bg": "white",
            "entry_fg": "black",
            "text_bg": "white",
            "correct": "#28a745",
            "incorrect": "#dc3545",
            "hint": "#ffc107",
            "title": "#17a2b8",
            "info": "#007bff"
        },
        "retro": {
            "bg": "#0f0f23",
            "fg": "#00cc00",
            "button_bg": "#006600",
            "button_fg": "#00ff00",
            "button_hover": "#009900",
            "entry_bg": "#001a00",
            "entry_fg": "#00ff00",
            "text_bg": "#001a00",
            "correct": "#00ff00",
            "incorrect": "#ff3333",
            "hint": "#ff9900",
            "title": "#66ff66",
            "info": "#00ccff"
        }
    }
    
    @staticmethod
    def get_theme(theme_name: str = "dark") -> dict:
        """Get theme by name"""
        return GameThemes.THEMES.get(theme_name, GameThemes.THEMES["dark"])
    
    @staticmethod
    def get_theme_names() -> list:
        """Get list of available themes"""
        return list(GameThemes.THEMES.keys())