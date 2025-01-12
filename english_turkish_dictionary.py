import tkinter as tk
from tkinter import ttk
from googletrans import Translator

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English-Turkish Dictionary")
        
        # Styling
        self.root.geometry("700x500")
        self.root.configure(bg="#34495e")

        # Translator instance
        self.translator = Translator()

        # GUI Layout
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="English ↔ Turkish Translator", font=("Arial", 24, "bold"), bg="#34495e", fg="#ecf0f1")
        title_label.pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#34495e")
        input_frame.pack(pady=20, padx=20, fill=tk.X)

        tk.Label(input_frame, text="Enter Text:", font=("Arial", 16), bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=5)
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var, font=("Arial", 16), width=50, relief="solid", bd=2)
        self.input_entry.pack(pady=5, padx=10)

        # Translate Button
        translate_button = tk.Button(input_frame, text="Translate", command=self.translate_text, font=("Arial", 16), bg="#3498db", fg="white", relief="flat", cursor="hand2")
        translate_button.pack(pady=10)

        # Output Frame
        output_frame = tk.Frame(self.root, bg="#34495e")
        output_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(output_frame, text="Translation:", font=("Arial", 16), bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=5)
        self.output_label = tk.Label(output_frame, text="", font=("Arial", 16), bg="#2c3e50", fg="#ecf0f1", wraplength=650, justify="left", relief="solid", bd=2, padx=10, pady=10)
        self.output_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Footer
        footer = tk.Label(self.root, text="AZD Translator", font=("Arial", 12), bg="#34495e", fg="#bdc3c7")
        footer.pack(side=tk.BOTTOM, pady=10)

    def translate_text(self):
        input_text = self.input_var.get().strip()
        if not input_text:
            self.output_label.config(text="Please enter text to translate.")
            return

        try:
            # Automatically detect source language and translate to the other
            detected_lang = self.translator.detect(input_text).lang
            target_lang = "tr" if detected_lang == "en" else "en"

            # Perform translation
            result = self.translator.translate(input_text, src=detected_lang, dest=target_lang)
            self.output_label.config(text=result.text)
        except Exception as e:
            self.output_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
