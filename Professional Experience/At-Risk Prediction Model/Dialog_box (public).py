"""
model-selection dialog using Tkinter.

What it shows:
- A minimal GUI built with Tkinter
- Dropdown (OptionMenu) to pick between model types
- Returns the user’s choice when confirmed

"""

import tkinter as tk

def choose_model(options=None, default="Decision Tree") -> str:
    """
    Display a simple dialog box with a dropdown menu to select a model.
    """
    if options is None:
        options = ["Decision Tree", "Neural Network"]

    root = tk.Tk()
    root.title("Select Model")

    tk.Label(root, text="Choose a model:").pack(padx=10, pady=10)

    var = tk.StringVar(value=default)
    tk.OptionMenu(root, var, *options).pack(padx=10, pady=10)

    tk.Button(root, text="OK", command=root.destroy).pack(padx=10, pady=10)
    root.mainloop()

    return var.get()

# choice = choose_model()
# print("Selected:", choice)

