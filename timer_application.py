import tkinter as tk
from tkinter import ttk
import time
import threading
from datetime import timedelta
import winsound  # For alarm sound

# Define the TimerApplication class
class TimerApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Advanced Timer Application")
        self.geometry("700x650")
        self.configure(bg="#1F1F1F")

        # Initialize variables
        self.timer_running = False
        self.remaining_time = 0
        self.timer_thread = None

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(
            self, text="Advanced Timer Application", font=("Helvetica", 26, "bold"), fg="#FFD700", bg="#1F1F1F"
        )
        self.title_label.pack(pady=15)

        # Timer display
        self.timer_display = tk.Label(
            self, text="00:00:00", font=("Helvetica", 60, "bold"), fg="#00FFFF", bg="#1F1F1F"
        )
        self.timer_display.pack(pady=20)

        # Advanced time entry section
        self.time_entry_label = tk.Label(
            self, text="Set Time:", font=("Helvetica", 16), fg="#FFFFFF", bg="#1F1F1F"
        )
        self.time_entry_label.pack(pady=5)

        entry_frame = tk.Frame(self, bg="#1F1F1F")
        entry_frame.pack(pady=10)

        self.hour_entry = ttk.Entry(entry_frame, width=5, font=("Helvetica", 14), justify="center")
        self.hour_entry.insert(0, "00")
        self.hour_entry.grid(row=0, column=0, padx=5)

        tk.Label(entry_frame, text=":", font=("Helvetica", 16), fg="#FFFFFF", bg="#1F1F1F").grid(row=0, column=1)

        self.minute_entry = ttk.Entry(entry_frame, width=5, font=("Helvetica", 14), justify="center")
        self.minute_entry.insert(0, "00")
        self.minute_entry.grid(row=0, column=2, padx=5)

        tk.Label(entry_frame, text=":", font=("Helvetica", 16), fg="#FFFFFF", bg="#1F1F1F").grid(row=0, column=3)

        self.second_entry = ttk.Entry(entry_frame, width=5, font=("Helvetica", 14), justify="center")
        self.second_entry.insert(0, "00")
        self.second_entry.grid(row=0, column=4, padx=5)

        # Control buttons
        button_frame = tk.Frame(self, bg="#1F1F1F")
        button_frame.pack(pady=15)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=10)

        # Log panel
        self.log_panel = tk.Text(self, height=10, width=60, state="disabled", bg="#2B2B2B", fg="#FFFFFF", font=("Consolas", 12))
        self.log_panel.pack(pady=15)

        # Footer
        self.footer_label = tk.Label(
            self, text="AZD", font=("Helvetica", 10), fg="#AAAAAA", bg="#1F1F1F"
        )
        self.footer_label.pack(side="bottom", pady=5)

    def log_message(self, message):
        """Logs a message to the log panel."""
        self.log_panel.config(state="normal")
        self.log_panel.insert("end", message + "\n")
        self.log_panel.see("end")
        self.log_panel.config(state="disabled")

    def format_time(self, seconds):
        """Formats seconds into HH:MM:SS."""
        return str(timedelta(seconds=seconds))

    def start_timer(self):
        """Starts the timer."""
        if self.timer_running:
            self.log_message("Timer is already running.")
            return

        try:
            hours = int(self.hour_entry.get())
            minutes = int(self.minute_entry.get())
            seconds = int(self.second_entry.get())
            self.remaining_time = hours * 3600 + minutes * 60 + seconds
        except ValueError:
            self.log_message("Invalid time input. Please enter valid numbers.")
            return

        if self.remaining_time <= 0:
            self.log_message("Please set a time greater than 0.")
            return

        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.daemon = True  # Daemon thread stops when the main program exits
        self.timer_thread.start()
        self.log_message(f"Timer started: {self.format_time(self.remaining_time)}")

    def run_timer(self):
        """Runs the timer in a separate thread."""
        while self.timer_running and self.remaining_time > 0:
            time.sleep(1)
            self.remaining_time -= 1
            self.update_timer_display()

        if self.remaining_time == 0:
            self.timer_running = False
            self.log_message("Time is up!")
            self.trigger_alarm()

    def update_timer_display(self):
        """Updates the timer display in the GUI."""
        formatted_time = self.format_time(self.remaining_time)
        self.timer_display.config(text=formatted_time)

    def trigger_alarm(self):
        """Triggers an alarm when the timer reaches zero."""
        for _ in range(5):  # Beep 5 times
            winsound.Beep(1000, 500)  # 1000 Hz frequency, 500 ms duration

    def pause_timer(self):
        """Pauses the timer."""
        if not self.timer_running:
            self.log_message("Timer is not running.")
            return

        self.timer_running = False
        self.log_message("Timer paused.")

    def reset_timer(self):
        """Resets the timer."""
        self.timer_running = False
        self.remaining_time = 0
        self.update_timer_display()
        self.log_message("Timer reset.")

# Run the application
if __name__ == "__main__":
    app = TimerApplication()
    app.mainloop()
