import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import json

class Recipe:
    def __init__(self, name, category, ingredients, instructions):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.instructions = instructions

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        }

class RecipeBook:
    def __init__(self):
        self.recipes = []

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def search_recipe(self, query):
        results = []
        for recipe in self.recipes:
            if query.lower() in recipe.name.lower():
                results.append(recipe)
        return results

    def get_recipes_by_category(self, category):
        results = []
        for recipe in self.recipes:
            if recipe.category.lower() == category.lower():
                results.append(recipe)
        return results

    def to_dict(self):
        return {"recipes": [recipe.to_dict() for recipe in self.recipes]}

    def from_dict(cls, data):
        book = cls()
        for recipe_data in data.get("recipes", []):
            recipe = Recipe(
                recipe_data.get("name", ""),
                recipe_data.get("category", ""),
                recipe_data.get("ingredients", []),
                recipe_data.get("instructions", "")
            )
            book.add_recipe(recipe)
        return book

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f)

    def load_from_file(cls, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

recipe_book = RecipeBook()

try:
    recipe_book = RecipeBook.load_from_file("Snake_database.json")
except FileNotFoundError:
    pass

password = ""
while not password:
    password = simpledialog.askstring("Password", "Enter password: ", show="*")

root = tk.Tk()
root.title("Cook Snake Book")
root.geometry("920x720")
root.iconbitmap("Cook_Snake.ico")

text_widget = tk.Text(root, font=("Helvetica", 12))
text_widget.pack(expand=True, fill="both")

while True:
    text_widget.delete("1.0", tk.END)

    text_widget.insert(tk.END, "Welcome to your Snake Recipe Book!\n\n")
    for recipe in recipe_book.recipes:
        text_widget.insert(tk.END, f"Name: {recipe.name}\n")
        text_widget.insert(tk.END, f"Category: {recipe.category}\n")
        text_widget.insert(tk.END, f"Ingredients: {', '.join(recipe.ingredients)}\n")
        text_widget.insert(tk.END, f"Instructions: {recipe.instructions}\n\n")

    text_widget.insert(tk.END, "Make a choice!\n")
    text_widget.insert(tk.END, "1. Add recipe\n")
    text_widget.insert(tk.END, "2. Search recipe\n")
    text_widget.insert(tk.END, "3. Browse by category\n")
    text_widget.insert(tk.END, "4. Exit\n")

    choice = simpledialog.askstring("Input", "Enter your choice: ")

    if choice == "1":
        name = simpledialog.askstring("Input", "Enter recipe name: ")
        category = simpledialog.askstring("Input", "Enter recipe category: ")
        ingredients = simpledialog.askstring("Input", "Enter ingredients separated by commas: ").split(",")
        instructions = simpledialog.askstring("Input", "Enter instructions: ")
        recipe = Recipe(name, category, ingredients, instructions)
        recipe_book.add_recipe(recipe)
        text_widget.insert(tk.END, "Recipe added to your Recipe Book!\n")

    elif choice == "2":
        query = simpledialog.askstring("Input", "Enter search query: ")
        results = recipe_book.search_recipe(query)
        if len(results) == 0:
            text_widget.insert(tk.END, "Not found.\n")
        else:
            text_widget.insert(tk.END, f"Search: {query}\n")
            for recipe in results:
                text_widget.insert(tk.END, f"Name: {recipe.name}\n")
                text_widget.insert(tk.END, f"Category: {recipe.category}\n")
                text_widget.insert(tk.END, f"Ingredients: {', '.join(recipe.ingredients)}\n")
                text_widget.insert(tk.END, f"Instructions: {recipe.instructions}\n\n")

    elif choice == "3":
        category = simpledialog.askstring("Input", "Enter category name:")
        if category:
            results = recipe_book.get_recipes_by_category(category)
            if len(results) == 0:
                text_widget.insert(tk.END, "No recipes found for the category.\n")
            else:
                text_widget.insert(tk.END, f"{category} recipes:\n")
                for recipe in results:
                    text_widget.insert(tk.END, f"Name: {recipe.name}\n")
                    text_widget.insert(tk.END, f"Category: {recipe.category}\n")
                    text_widget.insert(tk.END, f"Ingredients: {', '.join(recipe.ingredients)}\n")
                    text_widget.insert(tk.END, f"Instructions: {recipe.instructions}\n\n")
        else:
            text_widget.insert(tk.END, "Please enter a valid category name.\n")

    elif choice == "4":
        confirm_exit = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm_exit:
            text_widget.insert(tk.END, "Goodbye!")
            root.after(2000, root.destroy)
            break
