import sqlite3
import sys
import time
sys.stderr.write("Prices may vary. Data based on 04/04/2024\n")
time.sleep(1)
def create_meal_db():
    with sqlite3.connect('kfc_meal_prices.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS meals
                     (id INTEGER PRIMARY KEY, name TEXT, price REAL, is_discount TEXT, discount_percentage REAL, demand INTEGER, rating REAL)''')

def insert_or_update_meal_into_db(meal_data):
    conn = sqlite3.connect('kfc_meal_prices.db')
    c = conn.cursor()

    # Check if the meal with the same name already exists
    c.execute("SELECT * FROM meals WHERE name = ?", (meal_data[0],))
    existing_meal = c.fetchone()

    if existing_meal:
        print("Meal already exists in the database.")
    else:
        # If meal doesn't exist, insert it
        c.execute("INSERT INTO meals (name, price, is_discount, discount_percentage, demand, rating) VALUES (?, ?, ?, ?, ?, ?)",
                  meal_data)
        conn.commit()
        print("Meal added successfully.")

    conn.close()

def remove_meal_from_db(meal_id):
    conn = sqlite3.connect('kfc_meal_prices.db')
    c = conn.cursor()

    # Check if the meal with the given ID exists
    c.execute("SELECT * FROM meals WHERE id = ?", (meal_id,))
    existing_meal = c.fetchone()

    if existing_meal:
        # If meal exists, remove it
        c.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
        conn.commit()
        print("Meal removed successfully.")
    else:
        print("Meal with the given ID does not exist.")

    conn.close()

def read_meal_data():
    with sqlite3.connect('kfc_meal_prices.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM meals")
        rows = c.fetchall()
        for row in rows:
            print(row)

def find_meal_id_by_name(meal_name):
    with sqlite3.connect('kfc_meal_prices.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM meals WHERE name = ?", (meal_name,))
        meal_id = c.fetchone()
        if meal_id:
            print(f"Meal ID for {meal_name} is {meal_id[0]}")
        else:
            print(f"No meal found with name {meal_name}")

if __name__ == "__main__":
    create_meal_db()

    # Example data to insert
    meals = [
    ('Zinger Burger', 18.99, 'N', 0.0, 0, 4.0),
    ('Kentucky Gold Grander', 24.99, 'N', 0.0, 0, 5.0),
    ('Kentucky Gold Grander Menu', 33.74, 'Y', 5.0, 0, 4.1),
    ('Kentucky Gold Grander Big Box', 39.74, 'Y', 8.0, 0, 3.4),
    ('Grander', 23.99, 'N', 0.0, 0, 5.0),
    ('Grander Menu', 30.74, 'Y', 4.0, 0, 4.8),
    ('Grander Big Box', 38.74, 'Y', 2.0, 0, 4.1),
    ('Zinger Burger Big Box', 34.99, 'Y', 5.0, 0, 3.9),
    ('Zinger Cheese & Bacon', 20.99, 'N', 0.0, 0, 5),
    ('Zinger Cheese & Bacon Menu', 28.74, 'Y', 7.0, 0, 3.5),
    ('Zinger Cheese & Bacon Big Box', 36.74, 'Y', 9.0, 0, 4.5),
    ('Menu Zinger Burger', 26.74, 'Y', 10.0, 0, 4.8),
    ('Halloumi Burger', 20.99, 'N', 0.0, 0, 4.2),
    ('Double Zinger Burger', 24.99, 'N', 0.0, 0, 4.5),
    ('Double Zinger Menu', 32.74, 'Y', 5.0, 0, 3.9),
    ('Double Zinger Big Box', 41.74, 'Y', 5.0, 0, 5),
    ('Halloumi Menu', 28.74, 'Y', 7.0, 0, 3.6),
    ('Double Grander', 29.99, 'N', 0.0, 0, 3.7),
    ('Double Grander Menu', 37.74, 'Y', 3.0, 0, 4.6),
    ('Longer Big Box', 33.99, 'Y', 3.0, 0, 5.0),
    ('Double Grander Big Box', 44.74, 'Y', 6.0, 0, 4.5),
    ('Longer', 6.99, 'N', 0.0, 0, 3.4),
    ('Longer Menu', 24.74, 'Y', 9.0, 0, 3.9),
    ('Cheeseburger', 6.99, 'N', 0.0, 0, 5.0),
    ('Coffee + Longer', 9.75, 'N', 0.0, 0, 4.5)

        # Add more meal data here...
    ]

    # Inserting or updating meals into the database
    for meal in meals:
        insert_or_update_meal_into_db(meal)

    # Reading and printing meal data
    read_meal_data()

    # Example: Find meal ID by name
    #find_meal_id_by_name('Fries')
