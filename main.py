import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu, ttk
from tkinter import font as tkfont

class BPlusTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("B+ Programming Language")
        self.root.geometry("1100x800")
        self.root.configure(bg="#2c3e50")
        
        # Custom styles
        self.configure_styles()
        
        # Create UI components
        self.create_header()
        self.create_main_panels()
        self.create_footer()
        
        # Default content
        self.insert_welcome_code()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#2c3e50"
        self.header_color = "#1a2634"
        self.accent_color = "#3498db"
        self.editor_bg = "#1e293b"
        self.text_color = "#ecf0f1"
        
        # Fonts
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.code_font = tkfont.Font(family="Consolas", size=12)
        self.ui_font = tkfont.Font(family="Segoe UI", size=10)

    def create_header(self):
        header = tk.Frame(self.root, bg=self.header_color, height=60)
        header.pack(fill=tk.X)
        
        # B+ Logo
        logo = tk.Label(
            header,
            text="B+",
            font=self.title_font,
            fg=self.accent_color,
            bg=self.header_color,
            padx=20
        )
        logo.pack(side=tk.LEFT)
        
        # Menu
        menubar = Menu(header, tearoff=0, bg=self.editor_bg, fg=self.text_color)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.clear_editor)
        file_menu.add_command(label="Run", command=self.translate_code)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="Examples", command=self.show_examples)

    def create_main_panels(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Editor panel
        editor_frame = tk.LabelFrame(
            main_frame,
            text=" B+ Code Editor ",
            font=self.ui_font,
            fg=self.accent_color,
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=5,
            pady=5,
            bg="#34495e",
            fg="#95a5a6",
            font=self.code_font,
            state='disabled'
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Code editor
        self.editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            bg=self.editor_bg,
            fg=self.text_color,
            insertbackground="white",
            selectbackground="#3d566e",
            font=self.code_font,
            padx=10,
            pady=10
        )
        self.editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.editor.bind("<KeyRelease>", self.update_line_numbers)
        
        # Output panel
        output_frame = tk.LabelFrame(
            main_frame,
            text=" Python Output ",
            font=self.ui_font,
            fg=self.accent_color,
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            state='disabled',
            bg=self.editor_bg,
            fg=self.text_color,
            font=self.code_font,
            padx=10,
            pady=10
        )
        self.output.pack(fill=tk.BOTH, expand=True)

    def create_footer(self):
        footer = tk.Frame(self.root, bg=self.header_color, height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Action buttons
        btn_style = {
            'bg': self.accent_color,
            'fg': 'white',
            'font': self.ui_font,
            'border': 0,
            'padx': 15,
            'pady': 5
        }
        
        tk.Button(footer, text="Run", command=self.translate_code, **btn_style).pack(side=tk.LEFT, padx=10)
        tk.Button(footer, text="Clear", command=self.clear_editor, bg="#e74c3c", fg="white", 
                font=self.ui_font, border=0, padx=15, pady=5).pack(side=tk.LEFT)
        tk.Button(footer, text="Help", command=self.show_docs, bg="#2ecc71", fg="white",
                font=self.ui_font, border=0, padx=15, pady=5).pack(side=tk.RIGHT, padx=10)

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        
        line_count = self.editor.get('1.0', 'end-1c').count('\n') + 1
        numbers = '\n'.join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert(tk.END, numbers)
        self.line_numbers.config(state='disabled')

    def translate_code(self):
        input_lines = self.editor.get('1.0', tk.END).split('\n')
        python_code = []
        indent_level = 0
        control_stack = []
        
        # Add default imports
        python_code.extend([
            "import numpy as np",
            "import pandas as pd",
            ""
        ])
        
        for line in input_lines:
            line = line.strip()
            if not line:
                continue
                
            # Handle B+ syntax (simplified examples)
            if line.startswith("write string "):
                python_code.append(' ' * indent_level + f'print("{line[13:]}")')
            elif line.startswith("write var "):
                python_code.append(' ' * indent_level + f'print({line[10:]})')
            elif line.startswith("var "):
                python_code.append(' ' * indent_level + line.replace("var ", ""))
            elif line.startswith("for "):
                parts = line[4:].split(" in ")
                if len(parts) == 2:
                    python_code.append(' ' * indent_level + f"for {parts[0].strip()} in {parts[1].strip()}:")
                    control_stack.append(('for', indent_level))
                    indent_level += 4
            elif line.startswith("while "):
                python_code.append(' ' * indent_level + f"while {line[6:]}:")
                control_stack.append(('while', indent_level))
                indent_level += 4
            elif line == "end":
                if control_stack:
                    indent_level = control_stack[-1][1]
                    control_stack.pop()
        
        # Display output
        self.output.config(state='normal')
        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, '\n'.join(python_code))
        self.output.config(state='disabled')
        
        # Save to file
        with open("output.py", "w") as f:
            f.write('\n'.join(python_code))
        
        messagebox.showinfo("Success", "B+ code translated to Python!")

    def clear_editor(self):
        self.editor.delete('1.0', tk.END)
        self.output.config(state='normal')
        self.output.delete('1.0', tk.END)
        self.output.config(state='disabled')
        self.update_line_numbers()

    def show_docs(self):
        docs = """B+ LANGUAGE DOCUMENTATION

VARIABLES:
  var int x = 10       # Integer
  var str text = "hi"  # String
  var list data = [1,2,3] # List

LOOPS:
  for item in collection
    write var item
  end

  while x < 10
    var int x = x + 1
  end

FUNCTIONS:
  func greet(name)
    write string "Hello " + name
  end func

I/O:
  write string "Text"  # Print text
  write var x          # Print variable
  input str name       # User input
"""
        self.show_popup("B+ Documentation", docs)

    def show_examples(self):
        examples = """B+ EXAMPLE CODE:

# Fibonacci sequence
var int a = 0
var int b = 1
while a < 100
    write var a
    var int temp = a
    var int a = b
    var int b = temp + b
end

# List processing
var list fruits = ["apple", "banana", "cherry"]
for fruit in fruits
    write string "I love " + fruit
end
"""
        self.show_popup("B+ Examples", examples)

    def show_popup(self, title, content):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("600x400")
        
        text = scrolledtext.ScrolledText(
            popup,
            wrap=tk.WORD,
            font=self.code_font,
            bg=self.editor_bg,
            fg=self.text_color,
            padx=15,
            pady=15
        )
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, content)
        text.config(state='disabled')

    def insert_welcome_code(self):
        welcome_code = """# Welcome to B+ Programming Language!

# Example: Fibonacci Sequence
var int a = 0
var int b = 1
while a < 100
    write var a
    var int temp = a
    var int a = b
    var int b = temp + b
end

# Example: List Processing
var list fruits = ["apple", "banana", "cherry"]
for fruit in fruits
    write string "I love " + fruit
end
"""
        self.editor.insert(tk.END, welcome_code)
        self.update_line_numbers()

if __name__ == "__main__":
    root = tk.Tk()
    app = BPlusTranslator(root)
    root.mainloop()