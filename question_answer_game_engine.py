import tkinter as tk
from tkinter import ttk
import threading
import requests
import random
import html

class QAGameEngine:
    def __init__(self, root):
        """Initialize the Q&A Game Engine."""
        self.root = root
        self.root.title("Q&A Game Engine")
        self.root.geometry("800x600")

        # Style Setup
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 14), padding=10)
        self.style.configure('TLabel', font=('Arial', 16))
        self.root.configure(bg="#1A1A2E")

        # Variables
        self.current_question = tk.StringVar()
        self.user_answer = tk.StringVar()
        self.message_log = tk.StringVar()
        self.message_log.set("Welcome to the Q&A Game! Please choose the number of questions.")
        self.score = 0
        self.question_count = tk.IntVar(value=5)
        self.questions = []
        self.current_index = 0

        # Buttons State Tracking
        self.start_button = None
        self.reset_button = None

        # GUI Layout
        self.create_gui()

    def create_gui(self):
        """Create the GUI components."""
        title_frame = tk.Frame(self.root, bg="#16213E")
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text="Q&A Game Engine", font=('Arial', 24, 'bold'), bg="#16213E", fg="#E94560")
        title_label.pack(pady=10)

        setup_frame = tk.Frame(self.root, bg="#1A1A2E")
        setup_frame.pack(pady=20)

        setup_label = ttk.Label(setup_frame, text="Number of Questions:", font=('Arial', 14), background="#1A1A2E", foreground="white")
        setup_label.pack(side=tk.LEFT, padx=5)

        question_count_spinbox = ttk.Spinbox(setup_frame, from_=1, to=20, textvariable=self.question_count, font=('Arial', 14), width=5)
        question_count_spinbox.pack(side=tk.LEFT, padx=5)

        self.start_button = ttk.Button(setup_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = ttk.Button(setup_frame, text="Reset", command=self.reset_game, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        question_frame = tk.Frame(self.root, bg="#1A1A2E")
        question_frame.pack(pady=20, padx=20, fill=tk.X)

        self.question_label = ttk.Label(question_frame, textvariable=self.current_question, wraplength=600, anchor="center", background="#0F3460", foreground="white")
        self.question_label.pack(padx=10, pady=10, fill=tk.X)

        answer_frame = tk.Frame(self.root, bg="#1A1A2E")
        answer_frame.pack(pady=10)

        answer_entry = ttk.Entry(answer_frame, textvariable=self.user_answer, font=('Arial', 14), width=30)
        answer_entry.pack(side=tk.LEFT, padx=10)

        submit_button = ttk.Button(answer_frame, text="Submit", command=self.submit_answer)
        submit_button.pack(side=tk.LEFT, padx=5)

        message_frame = tk.Frame(self.root, bg="#1A1A2E")
        message_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.message_panel = tk.Label(message_frame, textvariable=self.message_log, bg="#16213E", fg="#E94560", font=('Arial', 14), wraplength=600, justify="left", anchor="nw")
        self.message_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        azd_label = tk.Label(self.root, text="AZD", bg="#1A1A2E", fg="#E94560", font=('Arial', 10, 'italic'))
        azd_label.pack(side=tk.BOTTOM, pady=10)

    def start_game(self):
        """Start the game by fetching questions and resetting variables."""
        self.questions = self.fetch_questions(self.question_count.get())
        self.score = 0
        self.current_index = 0

        if self.questions:
            self.message_log.set("Game Started! Answer the questions.")
            self.display_next_question()
            self.start_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
        else:
            self.message_log.set("Failed to load questions. Please try again.")

    def reset_game(self):
        """Reset the game to its initial state."""
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.current_question.set("")
        self.user_answer.set("")
        self.message_log.set("Welcome to the Q&A Game! Please choose the number of questions.")
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

    def submit_answer(self):
        """Check the user's answer and update the score."""
        if not self.questions or self.current_index >= len(self.questions):
            self.message_log.set("No active question. Please start the game.")
            return

        answer = self.user_answer.get().strip().lower()
        correct_answer = self.questions[self.current_index]["correct_answer"].lower()

        if answer == correct_answer:
            self.score += 1
            self.message_log.set(f"Correct! Your score: {self.score}")
        else:
            self.message_log.set(f"Incorrect. The correct answer was: {correct_answer}. Your score: {self.score}")

        self.user_answer.set("")
        self.current_index += 1

        if self.current_index < len(self.questions):
            self.display_next_question()
        else:
            self.message_log.set(f"Game Over. Final Score: {self.score}")
            self.reset_button.config(state=tk.NORMAL)

    def display_next_question(self):
        """Display the next question."""
        question = self.questions[self.current_index]
        self.current_question.set(html.unescape(question["question"]))

    def fetch_questions(self, count):
        """Fetch questions from an API."""
        try:
            response = requests.get(f"https://opentdb.com/api.php?amount={count}&type=multiple")
            response.raise_for_status()
            data = response.json()

            questions = []
            for item in data.get("results", []):
                question = {
                    "question": html.unescape(item["question"]),
                    "correct_answer": html.unescape(item["correct_answer"]),
                }
                questions.append(question)

            return questions
        except Exception as e:
            self.message_log.set(f"Error fetching questions: {e}")
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = QAGameEngine(root)
    root.mainloop()
