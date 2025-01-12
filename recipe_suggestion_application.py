import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import threading
import json
from collections import Counter
from difflib import get_close_matches

class RecipeSuggestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Suggestion Application")
        self.root.geometry("800x600")
        
        # Styles
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 10, "bold"))

        # Frame for input and search
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill='x')

        self.ingredient_label = ttk.Label(input_frame, text="Enter Ingredients (comma-separated):")
        self.ingredient_label.pack(side="left", padx=5)

        self.ingredient_entry = ttk.Entry(input_frame, width=50)
        self.ingredient_entry.pack(side="left", padx=5)

        self.search_button = ttk.Button(input_frame, text="Search Recipes", command=self.search_recipes)
        self.search_button.pack(side="left", padx=5)

        # Frame for updates and warnings
        self.update_frame = ttk.Frame(self.root, relief="groove", borderwidth=2)
        self.update_frame.pack(pady=10, padx=10, fill='x')

        self.update_label = ttk.Label(self.update_frame, text="Updates:", anchor="w")
        self.update_label.pack(fill='x')

        # Frame for displaying recipes
        self.recipe_frame = ttk.Frame(self.root)
        self.recipe_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Branding label
        self.azd_label = ttk.Label(self.root, text="AZD", font=("Arial", 10), anchor="e")
        self.azd_label.pack(side="bottom", fill='x')

        # Pre-load ingredients list from TheMealDB
        self.supported_ingredients = self.fetch_supported_ingredients()

    def fetch_supported_ingredients(self):
        try:
            url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return [item['strIngredient'].lower() for item in data.get('meals', [])]
        except requests.RequestException as e:
            self.update_status(f"Error fetching ingredients list: {e}")
            return []
        except Exception as e:
            self.update_status(f"Unexpected error: {e}")
            return []

    def search_recipes(self):
        ingredients = self.ingredient_entry.get().strip()
        if not ingredients:
            self.update_status("Please enter some ingredients.")
            return

        # Normalize and validate ingredients
        user_ingredients = [ing.strip().lower() for ing in ingredients.split(',')]
        valid_ingredients = self.normalize_ingredients(user_ingredients)

        if not valid_ingredients:
            self.update_status("No valid ingredients found. Please check your input.")
            return

        # Debugging: Log normalized ingredients
        print(f"Normalized Ingredients: {valid_ingredients}")

        # Clear previous results
        for widget in self.recipe_frame.winfo_children():
            widget.destroy()

        self.update_status("Searching for recipes...")

        # Use threading for API call
        threading.Thread(target=self.fetch_recipes, args=(valid_ingredients,)).start()

    def normalize_ingredients(self, user_ingredients):
        normalized = []
        for ing in user_ingredients:
            matches = get_close_matches(ing, self.supported_ingredients, n=1, cutoff=0.6)
            if matches:
                normalized.append(matches[0])
        return normalized

    def fetch_recipes(self, ingredients):
        try:
            all_results = []
            for ingredient in ingredients:
                url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
                print(f"API URL for {ingredient}: {url}")  # Debugging: Log API URL
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                if "meals" in data and data["meals"]:
                    all_results.extend(data["meals"])

            # Count occurrences of each recipe
            recipe_counter = Counter([recipe["idMeal"] for recipe in all_results])

            # Only include recipes that appear in all ingredient searches
            common_recipes = [recipe_id for recipe_id, count in recipe_counter.items() if count == len(ingredients)]

            if common_recipes:
                filtered_recipes = [recipe for recipe in all_results if recipe["idMeal"] in common_recipes]
                unique_recipes = {recipe["idMeal"]: recipe for recipe in filtered_recipes}.values()  # Remove duplicates
                self.display_recipes(list(unique_recipes))
                self.update_status(f"Found {len(unique_recipes)} recipes matching all ingredients.")
            else:
                self.update_status("No recipes found matching all given ingredients.")

        except requests.RequestException as e:
            self.update_status(f"Error fetching recipes: {e}")
        except Exception as e:
            self.update_status(f"Unexpected error: {e}")

    def display_recipes(self, recipes):
        for recipe in recipes:
            frame = ttk.Frame(self.recipe_frame, relief="ridge", borderwidth=2)
            frame.pack(pady=5, padx=5, fill='x')

            name = recipe.get("strMeal")
            thumbnail_url = recipe.get("strMealThumb")
            recipe_id = recipe.get("idMeal")

            name_label = ttk.Label(frame, text=name, font=("Arial", 14, "bold"))
            name_label.pack(side="left", padx=10)

            if thumbnail_url:
                try:
                    response = requests.get(thumbnail_url, stream=True)
                    response.raise_for_status()
                    image = Image.open(response.raw).resize((50, 50), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    img_label = ttk.Label(frame, image=photo)
                    img_label.image = photo  # Keep a reference to prevent garbage collection
                    img_label.pack(side="left", padx=10)
                except:
                    pass

            details_button = ttk.Button(frame, text="Details", command=lambda r_id=recipe_id: self.fetch_recipe_details(r_id))
            details_button.pack(side="right", padx=10)

    def fetch_recipe_details(self, recipe_id):
        try:
            url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}"
            response = requests.get(url)
            response.raise_for_status()
            recipe = response.json().get("meals", [])[0]

            # Show recipe details in a popup window
            self.show_recipe_details(recipe)
        except requests.RequestException as e:
            self.update_status(f"Error fetching recipe details: {e}")
        except Exception as e:
            self.update_status(f"Unexpected error: {e}")

    def show_recipe_details(self, recipe):
        details_window = tk.Toplevel(self.root)
        details_window.title(recipe.get("strMeal", "Recipe Details"))

        name_label = ttk.Label(details_window, text=recipe.get("strMeal"), font=("Arial", 16, "bold"))
        name_label.pack(pady=10)

        instructions = recipe.get("strInstructions", "No instructions available.")
        instructions_label = ttk.Label(details_window, text=instructions, wraplength=500, justify="left")
        instructions_label.pack(pady=10)

    def update_status(self, message):
        self.update_label.config(text=f"Updates: {message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeSuggestionApp(root)
    root.mainloop()
