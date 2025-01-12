import tkinter as tk
from tkinter import ttk
import requests
import asyncio
import threading
from googletrans import Translator

# Translator instance for translation
translator = Translator()

# Open Library API endpoint
API_URL = "http://openlibrary.org/search.json"

class BookRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Recommendation System")

        # Main frame for GUI layout
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Search box
        self.search_label = ttk.Label(self.main_frame, text="Search for a book:")
        self.search_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.search_entry = ttk.Entry(self.main_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.search_button = ttk.Button(self.main_frame, text="Search", command=self.search_books)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Display area for results
        self.result_panel = tk.Text(self.main_frame, wrap=tk.WORD, height=20, width=70, state=tk.DISABLED)
        self.result_panel.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # AZD label at the bottom
        self.azd_label = ttk.Label(self.main_frame, text="AZD", anchor="center", foreground="blue")
        self.azd_label.grid(row=2, column=0, columnspan=3, pady=10)

    def clear_results(self):
        """Clear the result panel."""
        self.result_panel.config(state=tk.NORMAL)
        self.result_panel.delete(1.0, tk.END)
        self.result_panel.config(state=tk.DISABLED)

    def display_message(self, message):
        """Display a message in the result panel."""
        self.result_panel.config(state=tk.NORMAL)
        self.result_panel.insert(tk.END, message + "\n")
        self.result_panel.config(state=tk.DISABLED)
        self.result_panel.see(tk.END)

    def search_books(self):
        """Initiate book search using threading for responsiveness."""
        search_query = self.search_entry.get().strip()
        if not search_query:
            self.display_message("Please enter a search term.")
            return

        # Clear previous results
        self.clear_results()

        # Run the API search in a separate thread
        thread = threading.Thread(target=self.fetch_books, args=(search_query,))
        thread.start()

    def fetch_books(self, query):
        """Fetch books from Open Library API and display results."""
        try:
            self.display_message(f"Searching for books related to: {query}")
            response = requests.get(API_URL, params={"q": query})
            response.raise_for_status()

            data = response.json()
            books = data.get("docs", [])

            if not books:
                self.display_message("No results found.")
                return

            for book in books[:10]:  # Limit to top 10 results
                title = book.get("title", "Unknown Title")
                author = book.get("author_name", ["Unknown Author"])[0]
                translated_title = self.translate_to_english(title)
                translated_author = self.translate_to_english(author)

                if translated_title.lower() == query.lower():
                    continue  # Skip recommending the exact book searched

                self.display_message(f"Title: {translated_title}\nAuthor: {translated_author}\n---")
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

    def translate_to_english(self, text):
        """Translate text to English if not already in English."""
        try:
            translated = translator.translate(text, dest="en")
            return translated.text
        except Exception:
            return text

if __name__ == "__main__":
    root = tk.Tk()
    app = BookRecommendationApp(root)
    root.mainloop()
