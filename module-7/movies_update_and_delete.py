# Alrich Rigonios
# Module 7 - Movies Update & Deletes

import mysql.connector
from dotenv import dotenv_values

secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

def show_films(cursor, title):
    print("\n-- {} --".format(title))

    query = """
    SELECT film_name,
           film_director,
           genre_name,
           studio_name
    FROM film
    INNER JOIN genre ON film.genre_id = genre.genre_id
    INNER JOIN studio ON film.studio_id = studio.studio_id
    """

    cursor.execute(query)
    films = cursor.fetchall()

    for film in films:
        print("Film Name: {}".format(film[0]))
        print("Director: {}".format(film[1]))
        print("Genre Name ID: {}".format(film[2]))
        print("Studio Name: {}".format(film[3]))
        print()

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # 1. Show original films
    show_films(cursor, "DISPLAYING FILMS")

    # 2. Insert new film (NOT Star Wars)
    cursor.execute("""
    INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
    VALUES ('Interstellar', 2014, 169, 'Christopher Nolan', 3, 2)
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # 3. Update Alien → Horror (genre_id = 1)
    cursor.execute("""
    UPDATE film
    SET genre_id = 1
    WHERE film_name = 'Alien'
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

    # 4. Delete Gladiator
    cursor.execute("""
    DELETE FROM film
    WHERE film_name = 'Gladiator'
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

    input("\nPress any key to continue...")

except mysql.connector.Error as err:
    print(err)

finally:
    if 'db' in locals() and db.is_connected():
        db.close()