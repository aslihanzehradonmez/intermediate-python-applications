import tkinter as tk
from tkinter import ttk
import threading
import time
import geocoder
import requests

# Helper function to fetch weather data without API
def fetch_weather_without_api(lat, lon):
    try:
        # Scrape weather data from a public website (example: wttr.in)
        response = requests.get(f"https://wttr.in/{lat},{lon}?format=%C+%t")
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

# Helper function to fetch city and country name
def fetch_location_details(lat, lon):
    try:
        response = requests.get(f"https://geocode.xyz/{lat},{lon}?geoit=json")
        response.raise_for_status()
        data = response.json()
        return data.get("city", "Unknown City"), data.get("country", "Unknown Country")
    except Exception as e:
        print(f"Error fetching location details: {e}")
        return "Unknown City", "Unknown Country"

# Main GUI Application
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Application")
        self.root.geometry("400x350")  # Adjusted height to ensure footer visibility
        self.root.configure(bg="#2c3e50")

        # Title Label
        self.title_label = tk.Label(root, text="Weather Application", font=("Helvetica", 20, "bold"), bg="#34495e", fg="white")
        self.title_label.pack(fill=tk.X, pady=10)

        # Weather Display Frame
        self.weather_frame = tk.Frame(root, bg="#2c3e50")
        self.weather_frame.pack(fill=tk.BOTH, expand=False, pady=(10, 0))  # Reduced bottom padding to create space for footer

        self.weather_output = tk.Text(self.weather_frame, font=("Courier", 12), bg="#34495e", fg="white", state=tk.DISABLED, height=10, wrap=tk.WORD)
        self.weather_output.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

        # Status Frame
        self.status_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#34495e", fg="yellow")
        self.status_label.pack(fill=tk.X, pady=5)

        # Footer
        self.footer_label = tk.Label(root, text="AZD", font=("Helvetica", 10, "italic"), bg="#34495e", fg="white")
        self.footer_label.pack(fill=tk.X, pady=5)

        self.update_status("Fetching your location...")
        threading.Thread(target=self.get_location_and_weather).start()

    def update_status(self, message):
        self.status_label.config(text=message)

    def display_weather(self, city, country, weather_data):
        self.weather_output.config(state=tk.NORMAL)
        self.weather_output.delete(1.0, tk.END)
        self.weather_output.insert(tk.END, f"Location: {city}, {country}\n\n")
        self.weather_output.insert(tk.END, weather_data)
        self.weather_output.config(state=tk.DISABLED)

    def get_location_and_weather(self):
        try:
            g = geocoder.ip('me')
            if g.latlng:
                lat, lon = g.latlng
                self.update_status("Fetching location details...")
                city, country = fetch_location_details(lat, lon)
                self.update_status("Fetching weather data...")
                weather_data = fetch_weather_without_api(lat, lon)
                if weather_data is None:
                    self.update_status("Failed to fetch weather data. Check your connectivity.")
                else:
                    self.display_weather(city, country, weather_data)
                    self.update_status("Weather data updated.")
            else:
                self.update_status("Unable to determine your location. Ensure geolocation services are enabled.")
        except Exception as e:
            print(f"Error determining location: {e}")
            self.update_status("Error determining location. Check geolocation settings.")

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
