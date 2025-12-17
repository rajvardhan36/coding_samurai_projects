"""
MODERN SCIENTIFIC CALCULATOR
A powerful calculator with modern UI, scientific functions, and advanced features
"""

import tkinter as tk
from tkinter import ttk, font, messagebox
import math
import json
from datetime import datetime
import re

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Modern Scientific Calculator")
        self.root.geometry("500x700")
        self.root.resizable(True, True)
        self.root.minsize(450, 650)
        
        # Variables
        self.expression = ""
        self.result = ""
        self.history = []
        self.current_theme = "dark"
        self.memory = 0
        self.deg_rad_mode = "deg"  # deg or rad
        
        # Modern color themes
        self.themes = {
            "dark": {
                "bg": "#1a1a2e",
                "display_bg": "#16213e",
                "display_fg": "#e6e6e6",
                "button_bg": "#0f3460",
                "button_fg": "#ffffff",
                "num_bg": "#2d4059",
                "num_fg": "#ffffff",
                "operator_bg": "#f05454",
                "operator_fg": "#ffffff",
                "sci_bg": "#3a506b",
                "sci_fg": "#ffffff",
                "equal_bg": "#4cc9f0",
                "equal_fg": "#000000",
                "memory_bg": "#9d65c9",
                "memory_fg": "#ffffff"
            },
            "light": {
                "bg": "#f5f7fa",
                "display_bg": "#ffffff",
                "display_fg": "#333333",
                "button_bg": "#e4e7eb",
                "button_fg": "#333333",
                "num_bg": "#ffffff",
                "num_fg": "#333333",
                "operator_bg": "#ff6b6b",
                "operator_fg": "#ffffff",
                "sci_bg": "#a5d8ff",
                "sci_fg": "#333333",
                "equal_bg": "#4d96ff",
                "equal_fg": "#ffffff",
                "memory_bg": "#c5a3ff",
                "memory_fg": "#ffffff"
            },
            "blue": {
                "bg": "#0a192f",
                "display_bg": "#112240",
                "display_fg": "#ccd6f6",
                "button_bg": "#233554",
                "button_fg": "#a8b2d1",
                "num_bg": "#1d2d50",
                "num_fg": "#e6f1ff",
                "operator_bg": "#64ffda",
                "operator_fg": "#0a192f",
                "sci_bg": "#3a506b",
                "sci_fg": "#ccd6f6",
                "equal_bg": "#5271ff",
                "equal_fg": "#ffffff",
                "memory_bg": "#ff6b9d",
                "memory_fg": "#ffffff"
            }
        }
        
        self.current_colors = self.themes[self.current_theme]
        
        # Configure styles
        self.setup_styles()
        
        # Load history if exists
        self.load_history()
        
        # Create UI
        self.create_widgets()
        
        # Bind keyboard
        self.bind_keyboard()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        for theme_name, colors in self.themes.items():
            style.configure(f"{theme_name}.TButton",
                           padding=10,
                           font=('Segoe UI', 12),
                           borderwidth=0,
                           focusthickness=0,
                           focuscolor='none')
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.current_colors["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top bar with theme switcher and mode
        self.create_top_bar(main_container)
        
        # Display area
        self.create_display(main_container)
        
        # History panel (collapsible)
        self.create_history_panel(main_container)
        
        # Button area with tabs
        self.create_button_tabs(main_container)
        
    def create_top_bar(self, parent):
        """Create top bar with controls"""
        top_frame = tk.Frame(parent, bg=self.current_colors["bg"])
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Theme switcher
        theme_frame = tk.Frame(top_frame, bg=self.current_colors["bg"])
        theme_frame.pack(side=tk.LEFT)
        
        tk.Label(theme_frame, text="Theme:", 
                bg=self.current_colors["bg"], 
                fg=self.current_colors["display_fg"],
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                  values=list(self.themes.keys()),
                                  state="readonly", width=10)
        theme_combo.pack(side=tk.LEFT)
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        # Deg/Rad toggle
        mode_frame = tk.Frame(top_frame, bg=self.current_colors["bg"])
        mode_frame.pack(side=tk.LEFT, padx=20)
        
        self.mode_var = tk.StringVar(value=self.deg_rad_mode)
        tk.Radiobutton(mode_frame, text="DEG", variable=self.mode_var,
                      value="deg", command=self.toggle_mode,
                      bg=self.current_colors["bg"],
                      fg=self.current_colors["display_fg"],
                      selectcolor=self.current_colors["button_bg"],
                      activebackground=self.current_colors["bg"],
                      activeforeground=self.current_colors["display_fg"]).pack(side=tk.LEFT)
        
        tk.Radiobutton(mode_frame, text="RAD", variable=self.mode_var,
                      value="rad", command=self.toggle_mode,
                      bg=self.current_colors["bg"],
                      fg=self.current_colors["display_fg"],
                      selectcolor=self.current_colors["button_bg"],
                      activebackground=self.current_colors["bg"],
                      activeforeground=self.current_colors["display_fg"]).pack(side=tk.LEFT, padx=(10, 0))
        
        # Memory indicator
        memory_frame = tk.Frame(top_frame, bg=self.current_colors["bg"])
        memory_frame.pack(side=tk.RIGHT)
        
        self.memory_label = tk.Label(memory_frame, 
                                    text=f"M: {self.memory}",
                                    bg=self.current_colors["bg"],
                                    fg=self.current_colors["memory_fg"],
                                    font=('Segoe UI', 10, 'bold'))
        self.memory_label.pack()
        
    def create_display(self, parent):
        """Create calculator display"""
        display_frame = tk.Frame(parent, bg=self.current_colors["display_bg"],
                                height=120, relief=tk.RAISED, bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        display_frame.pack_propagate(False)
        
        # Expression display
        self.expression_var = tk.StringVar(value="")
        self.expression_label = tk.Label(display_frame,
                                        textvariable=self.expression_var,
                                        bg=self.current_colors["display_bg"],
                                        fg=self.current_colors["display_fg"],
                                        font=('Segoe UI', 16),
                                        anchor=tk.E,
                                        padx=20,
                                        pady=(20, 0))
        self.expression_label.pack(fill=tk.X)
        
        # Result display
        self.result_var = tk.StringVar(value="0")
        self.result_label = tk.Label(display_frame,
                                    textvariable=self.result_var,
                                    bg=self.current_colors["display_bg"],
                                    fg=self.current_colors["display_fg"],
                                    font=('Segoe UI', 36, 'bold'),
                                    anchor=tk.E,
                                    padx=20)
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
    def create_history_panel(self, parent):
        """Create collapsible history panel"""
        self.history_frame = tk.Frame(parent, bg=self.current_colors["bg"])
        self.history_frame.pack(fill=tk.X, pady=(0, 10))
        
        # History header
        history_header = tk.Frame(self.history_frame, bg=self.current_colors["button_bg"])
        history_header.pack(fill=tk.X)
        
        history_btn = tk.Button(history_header,
                               text="📜 History",
                               font=('Segoe UI', 10, 'bold'),
                               bg=self.current_colors["button_bg"],
                               fg=self.current_colors["button_fg"],
                               bd=0,
                               command=self.toggle_history)
        history_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        clear_btn = tk.Button(history_header,
                             text="🗑️ Clear",
                             font=('Segoe UI', 9),
                             bg=self.current_colors["button_bg"],
                             fg=self.current_colors["button_fg"],
                             bd=0,
                             command=self.clear_history)
        clear_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # History list
        self.history_listbox = tk.Listbox(self.history_frame,
                                         bg=self.current_colors["display_bg"],
                                         fg=self.current_colors["display_fg"],
                                         font=('Segoe UI', 10),
                                         height=4,
                                         bd=0,
                                         selectbackground=self.current_colors["operator_bg"])
        self.history_listbox.pack(fill=tk.X)
        self.history_listbox.bind("<Double-Button-1>", self.use_history_item)
        
        # Initially hidden
        self.history_visible = False
        self.history_listbox.pack_forget()
        
    def create_button_tabs(self, parent):
        """Create button area with tabs"""
        # Notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Basic tab
        basic_frame = tk.Frame(self.notebook, bg=self.current_colors["bg"])
        self.notebook.add(basic_frame, text="Basic")
        self.create_basic_buttons(basic_frame)
        
        # Scientific tab
        sci_frame = tk.Frame(self.notebook, bg=self.current_colors["bg"])
        self.notebook.add(sci_frame, text="Scientific")
        self.create_scientific_buttons(sci_frame)
        
        # Memory tab
        mem_frame = tk.Frame(self.notebook, bg=self.current_colors["bg"])
        self.notebook.add(mem_frame, text="Memory")
        self.create_memory_buttons(mem_frame)
        
    def create_basic_buttons(self, parent):
        """Create basic calculator buttons"""
        # Button grid for basic operations
        basic_buttons = [
            ['C', 'CE', '⌫', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        for i, row in enumerate(basic_buttons):
            btn_frame = tk.Frame(parent, bg=self.current_colors["bg"])
            btn_frame.pack(fill=tk.BOTH, expand=True, pady=1)
            
            for j, text in enumerate(row):
                btn = self.create_button(btn_frame, text, self.get_button_color(text))
                btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1)
                
    def create_scientific_buttons(self, parent):
        """Create scientific calculator buttons"""
        # Scientific buttons in two columns
        sci_buttons = [
            ['sin', 'cos', 'tan', 'π'],
            ['asin', 'acos', 'atan', 'e'],
            ['log', 'ln', '√', 'x²'],
            ['x^y', '10^x', 'e^x', '|x|'],
            ['(', ')', 'n!', '1/x']
        ]
        
        for i, row in enumerate(sci_buttons):
            btn_frame = tk.Frame(parent, bg=self.current_colors["bg"])
            btn_frame.pack(fill=tk.BOTH, expand=True, pady=1)
            
            for j, text in enumerate(row):
                btn = self.create_button(btn_frame, text, self.current_colors["sci_bg"])
                btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1)
    
    def create_memory_buttons(self, parent):
        """Create memory operation buttons"""
        mem_buttons = [
            ['MC', 'MR', 'M+', 'M-'],
            ['MS', 'M←', 'M→', 'MClear']
        ]
        
        for i, row in enumerate(mem_buttons):
            btn_frame = tk.Frame(parent, bg=self.current_colors["bg"])
            btn_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            for j, text in enumerate(row):
                btn = self.create_button(btn_frame, text, self.current_colors["memory_bg"])
                btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    
    def create_button(self, parent, text, bg_color):
        """Create a styled button"""
        fg_color = self.current_colors["button_fg"]
        
        # Special colors for specific buttons
        if text in ['=', 'Enter']:
            bg_color = self.current_colors["equal_bg"]
            fg_color = self.current_colors["equal_fg"]
        elif text in ['+', '-', '×', '÷', '^', 'x^y']:
            bg_color = self.current_colors["operator_bg"]
            fg_color = self.current_colors["operator_fg"]
        elif text in ['C', 'CE', 'MC', 'MClear']:
            bg_color = "#ff4757"  # Red for clear
        elif text in ['M+', 'M-', 'MR', 'MS', 'M←', 'M→']:
            bg_color = self.current_colors["memory_bg"]
            fg_color = self.current_colors["memory_fg"]
        
        btn = tk.Button(parent,
                       text=text,
                       font=('Segoe UI', 14, 'bold'),
                       bg=bg_color,
                       fg=fg_color,
                       activebackground=self.lighten_color(bg_color, 30),
                       activeforeground=fg_color,
                       bd=0,
                       relief=tk.RAISED,
                       cursor="hand2",
                       command=lambda: self.on_button_click(text))
        
        # Add hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=self.lighten_color(bg_color, 20)))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        
        return btn
    
    def get_button_color(self, text):
        """Get appropriate button color based on text"""
        if text.isdigit() or text == '.':
            return self.current_colors["num_bg"]
        elif text in ['C', 'CE', '⌫', '±']:
            return self.current_colors["button_bg"]
        else:
            return self.current_colors["operator_bg"]
    
    def lighten_color(self, color, amount=20):
        """Lighten a hex color"""
        color = color.lstrip('#')
        r = min(255, int(color[0:2], 16) + amount)
        g = min(255, int(color[2:4], 16) + amount)
        b = min(255, int(color[4:6], 16) + amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_button_click(self, text):
        """Handle button clicks"""
        if text == '=':
            self.calculate()
        elif text == 'C':
            self.clear_all()
        elif text == 'CE':
            self.clear_entry()
        elif text == '⌫':
            self.backspace()
        elif text == '±':
            self.negate()
        elif text in ['+', '-', '×', '÷', '^']:
            self.append_operator(text)
        elif text == 'π':
            self.append_value(str(math.pi))
        elif text == 'e':
            self.append_value(str(math.e))
        elif text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                     'log', 'ln', '√', 'x²', '10^x', 'e^x', '|x|', 'n!', '1/x']:
            self.scientific_function(text)
        elif text == 'x^y':
            self.append_operator('^')
        elif text in ['(', ')']:
            self.append_value(text)
        elif text in ['MC', 'MR', 'M+', 'M-', 'MS', 'M←', 'M→', 'MClear']:
            self.memory_operation(text)
        else:
            self.append_value(text)
    
    def append_value(self, value):
        """Append value to expression"""
        if self.result and self.result != "Error":
            self.expression = self.result
            self.result = ""
        
        self.expression += value
        self.update_display()
    
    def append_operator(self, operator):
        """Append operator to expression"""
        if not self.expression:
            if self.result and self.result != "Error":
                self.expression = self.result
            else:
                return
        
        # Replace symbols
        operator = operator.replace('×', '*').replace('÷', '/')
        
        # Add operator with space
        if self.expression and self.expression[-1] not in ['+', '-', '*', '/', '^', '(']:
            self.expression += f" {operator} "
            self.update_display()
    
    def scientific_function(self, func):
        """Handle scientific functions"""
        try:
            if self.result and self.result != "Error":
                value = float(self.result)
            elif self.expression:
                # Try to get last number from expression
                numbers = re.findall(r'[-+]?\d*\.\d+|\d+', self.expression)
                if numbers:
                    value = float(numbers[-1])
                else:
                    value = 0
            else:
                value = 0
            
            # Apply function
            if self.deg_rad_mode == "deg":
                angle = math.radians(value)
            else:
                angle = value
            
            if func == 'sin':
                result = math.sin(angle)
            elif func == 'cos':
                result = math.cos(angle)
            elif func == 'tan':
                result = math.tan(angle)
            elif func == 'asin':
                result = math.asin(value)
                if self.deg_rad_mode == "deg":
                    result = math.degrees(result)
            elif func == 'acos':
                result = math.acos(value)
                if self.deg_rad_mode == "deg":
                    result = math.degrees(result)
            elif func == 'atan':
                result = math.atan(value)
                if self.deg_rad_mode == "deg":
                    result = math.degrees(result)
            elif func == 'log':
                result = math.log10(value) if value > 0 else float('nan')
            elif func == 'ln':
                result = math.log(value) if value > 0 else float('nan')
            elif func == '√':
                result = math.sqrt(value) if value >= 0 else float('nan')
            elif func == 'x²':
                result = value ** 2
            elif func == '10^x':
                result = 10 ** value
            elif func == 'e^x':
                result = math.exp(value)
            elif func == '|x|':
                result = abs(value)
            elif func == 'n!':
                result = math.factorial(int(value)) if value >= 0 and value == int(value) else float('nan')
            elif func == '1/x':
                result = 1 / value if value != 0 else float('nan')
            
            if math.isnan(result):
                self.result = "Error"
            else:
                self.result = self.format_number(result)
                self.add_to_history(f"{func}({value}) = {self.result}")
            
            self.expression = ""
            self.update_display()
            
        except Exception as e:
            self.result = "Error"
            self.update_display()
    
    def calculate(self):
        """Calculate expression"""
        try:
            # Replace display symbols with calculation symbols
            expr = self.expression.replace('×', '*').replace('÷', '/')
            
            # Handle exponent
            expr = expr.replace('^', '**')
            
            # Evaluate
            result = eval(expr, {"__builtins__": {}}, 
                         {"sin": math.sin, "cos": math.cos, "tan": math.tan,
                          "asin": math.asin, "acos": math.acos, "atan": math.atan,
                          "log": math.log10, "ln": math.log, "sqrt": math.sqrt,
                          "exp": math.exp, "pi": math.pi, "e": math.e,
                          "radians": math.radians, "degrees": math.degrees})
            
            self.result = self.format_number(result)
            self.add_to_history(f"{self.expression} = {self.result}")
            
            # Clear expression for next calculation
            self.expression = ""
            self.update_display()
            
        except Exception as e:
            self.result = "Error"
            self.update_display()
    
    def format_number(self, num):
        """Format number for display"""
        if isinstance(num, (int, float)):
            if num == int(num):
                return str(int(num))
            
            # Format with appropriate precision
            if abs(num) > 1e10 or (abs(num) < 1e-5 and num != 0):
                return f"{num:.6e}"
            else:
                return f"{num:.10f}".rstrip('0').rstrip('.')
        return str(num)
    
    def clear_all(self):
        """Clear everything"""
        self.expression = ""
        self.result = "0"
        self.update_display()
    
    def clear_entry(self):
        """Clear current entry"""
        self.expression = ""
        self.update_display()
    
    def backspace(self):
        """Remove last character"""
        if self.expression:
            self.expression = self.expression[:-1]
            self.update_display()
    
    def negate(self):
        """Negate current value"""
        try:
            if self.result and self.result != "Error":
                value = float(self.result)
                self.result = str(-value)
            elif self.expression:
                # Negate last number in expression
                parts = self.expression.split()
                if parts and parts[-1].replace('.', '').replace('-', '').isdigit():
                    parts[-1] = str(-float(parts[-1]))
                    self.expression = ' '.join(parts)
            self.update_display()
        except:
            pass
    
    def memory_operation(self, op):
        """Handle memory operations"""
        try:
            current = float(self.result) if self.result and self.result != "Error" else 0
            
            if op == 'MC':
                self.memory = 0
            elif op == 'MR':
                self.append_value(str(self.memory))
            elif op == 'M+':
                self.memory += current
            elif op == 'M-':
                self.memory -= current
            elif op == 'MS':
                self.memory = current
            elif op == 'M←':
                if self.expression:
                    self.expression += str(self.memory)
            elif op == 'M→':
                self.result = str(self.memory)
            elif op == 'MClear':
                self.memory = 0
            
            self.update_memory_display()
            self.update_display()
            
        except Exception as e:
            self.result = "Error"
            self.update_display()
    
    def update_memory_display(self):
        """Update memory display"""
        self.memory_label.config(text=f"M: {self.format_number(self.memory)}")
    
    def add_to_history(self, entry):
        """Add calculation to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {entry}"
        self.history.append(history_entry)
        
        # Update listbox
        self.history_listbox.insert(0, history_entry)
        
        # Keep only last 50 entries
        if len(self.history) > 50:
            self.history.pop()
            self.history_listbox.delete(50)
        
        # Save history
        self.save_history()
    
    def use_history_item(self, event):
        """Use selected history item"""
        selection = self.history_listbox.curselection()
        if selection:
            entry = self.history_listbox.get(selection[0])
            # Extract result from history entry
            match = re.search(r'=\s*(.+)$', entry)
            if match:
                self.result = match.group(1)
                self.expression = ""
                self.update_display()
    
    def clear_history(self):
        """Clear calculation history"""
        self.history.clear()
        self.history_listbox.delete(0, tk.END)
        self.save_history()
    
    def toggle_history(self):
        """Toggle history panel visibility"""
        if self.history_visible:
            self.history_listbox.pack_forget()
            self.history_visible = False
        else:
            self.history_listbox.pack(fill=tk.X)
            self.history_visible = True
    
    def change_theme(self, event=None):
        """Change calculator theme"""
        self.current_theme = self.theme_var.get()
        self.current_colors = self.themes[self.current_theme]
        
        # Update all widgets
        self.root.configure(bg=self.current_colors["bg"])
        
        # Update all child widgets
        self.update_widget_colors(self.root)
        
        # Force update
        self.root.update_idletasks()
    
    def update_widget_colors(self, widget):
        """Recursively update widget colors"""
        try:
            # Update widget if it has bg/fg properties
            if 'bg' in widget.keys():
                widget.configure(bg=self.current_colors["bg"])
            if 'fg' in widget.keys() and isinstance(widget, (tk.Label, tk.Button)):
                widget.configure(fg=self.current_colors["display_fg"])
            
            # Special handling for specific widgets
            if isinstance(widget, tk.Label) and widget == self.result_label:
                widget.configure(bg=self.current_colors["display_bg"])
            elif isinstance(widget, tk.Label) and widget == self.expression_label:
                widget.configure(bg=self.current_colors["display_bg"])
            elif isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children():
                    self.update_widget_colors(child)
        
        except tk.TclError:
            pass
    
    def toggle_mode(self):
        """Toggle between degrees and radians"""
        self.deg_rad_mode = self.mode_var.get()
    
    def update_display(self):
        """Update display widgets"""
        self.expression_var.set(self.expression)
        
        if self.result:
            self.result_var.set(self.result)
        else:
            self.result_var.set(self.expression if self.expression else "0")
    
    def bind_keyboard(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Delete>', lambda e: self.clear_entry())
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        if key.isdigit() or key == '.':
            self.append_value(key)
        elif key in '+-*/':
            operator = key
            if key == '*':
                operator = '×'
            elif key == '/':
                operator = '÷'
            self.append_operator(operator)
        elif key == '^':
            self.append_operator('^')
    
    def save_history(self):
        """Save history to file"""
        try:
            with open('calculator_history.json', 'w') as f:
                json.dump(self.history[-20:], f)  # Save last 20 entries
        except:
            pass
    
    def load_history(self):
        """Load history from file"""
        try:
            with open('calculator_history.json', 'r') as f:
                self.history = json.load(f)
                for entry in reversed(self.history):
                    self.history_listbox.insert(0, entry)
        except:
            self.history = []
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconbitmap('calculator.ico')
    except:
        pass
    
    app = ModernCalculator(root)
    app.run()

if __name__ == "__main__":
    main()