import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import requests
import qrcode
from io import BytesIO
from PIL import Image, ImageTk
import threading
import os

class URLShortenerQRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener & QR Maker")
        self.root.geometry("600x700")
        self.root.configure(bg="#282c34")

        # Style setup
        self.style = ttk.Style()
        self.style.configure("TLabel", background="#282c34", foreground="white", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ttk.Label(
            self.root, text="URL Shortener & QR Code Maker", font=("Helvetica", 16, "bold"), anchor="center"
        )
        title_label.pack(pady=10)

        # Input Field
        input_label = ttk.Label(self.root, text="Enter URL:")
        input_label.pack(pady=5)

        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        # Action Buttons Frame
        button_frame = ttk.Frame(self.root, style="TButton")
        button_frame.pack(pady=5)

        self.shorten_button = ttk.Button(button_frame, text="Shorten URL", command=self.shorten_url_thread)
        self.shorten_button.grid(row=0, column=0, padx=5)

        self.qr_button = ttk.Button(button_frame, text="Generate QR Code", command=self.generate_qr_thread)
        self.qr_button.grid(row=0, column=1, padx=5)

        # Set background color of button frame to match the root background
        self.style.configure("Custom.TFrame", background="#282c34")
        button_frame.configure(style="Custom.TFrame")

        # Output Section
        output_label = ttk.Label(self.root, text="Output:")
        output_label.pack(pady=5)

        self.output_text = tk.Text(self.root, width=70, height=4, wrap=tk.WORD, state=tk.DISABLED, bg="#353a42", fg="white", font=("Helvetica", 12))
        self.output_text.pack(pady=10)

        # QR Code Panel
        self.qr_panel = ttk.Label(self.root)
        self.qr_panel.pack(pady=10)

        # Info Label
        info_label = ttk.Label(self.root, text="Double-click output to copy it", font=("Helvetica", 10, "italic"))
        info_label.pack(pady=5)

        # Status Panel
        self.status_label = ttk.Label(self.root, text="", font=("Helvetica", 12, "italic"))
        self.status_label.pack(pady=5)

        # AZD Label
        azd_label = ttk.Label(self.root, text="AZD", font=("Helvetica", 10, "italic"), anchor="center")
        azd_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind double-click to copy output
        self.output_text.bind("<Double-1>", self.copy_output)

    def update_status(self, message, error=False):
        self.status_label.config(foreground="red" if error else "green")
        self.status_label.config(text=message)

    def shorten_url_thread(self):
        thread = threading.Thread(target=self.shorten_url)
        thread.start()

    def shorten_url(self):
        url = self.url_entry.get()
        if not url:
            self.update_status("URL cannot be empty!", error=True)
            return
        self.update_status("Shortening URL...")
        try:
            response = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
            if response.status_code == 200:
                short_url = response.text
                self.display_output(short_url)
                self.update_status("URL shortened successfully!")
            else:
                self.update_status("Failed to shorten URL.", error=True)
        except requests.RequestException as e:
            self.update_status(f"Error: {e}", error=True)

    def generate_qr_thread(self):
        thread = threading.Thread(target=self.generate_qr)
        thread.start()

    def generate_qr(self):
        url = self.url_entry.get()
        if not url:
            self.update_status("URL cannot be empty!", error=True)
            return
        self.update_status("Generating QR Code...")
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((300, 300), Image.Resampling.LANCZOS)

            # Save QR Code as PNG
            file_name = self.get_file_name_from_url(url)
            img.save(file_name)
            
            img_tk = ImageTk.PhotoImage(img)

            self.qr_panel.config(image=img_tk)
            self.qr_panel.image = img_tk
            self.update_status(f"QR Code generated and saved as {file_name}!")
        except Exception as e:
            self.update_status(f"Error: {e}", error=True)

    def get_file_name_from_url(self, url):
        if "watch?v=" in url:
            query_part = url.split("watch?v=")[-1]  # Extract part after 'watch?v='
            file_name = query_part.split("&")[0]  # Take only up to the next '&', if any
        else:
            file_name = url.split("//")[-1].split("/")[0]  # Default to domain name
        sanitized_name = file_name.replace(".", "_").replace(":", "_")  # Replace unsafe characters
        return f"{sanitized_name}_qr.png"

    def display_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)

    def copy_output(self, event):
        output = self.output_text.get(1.0, tk.END).strip()
        if output:
            pyperclip.copy(output)
            self.update_status("Output copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortenerQRApp(root)
    root.mainloop()
