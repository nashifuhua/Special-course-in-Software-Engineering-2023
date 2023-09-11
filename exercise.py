import sqlite3
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = file.readlines()
b = sqlite3.connect('stephen_king_adaptations.db')
a = b.cursor()
a.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table 
             (movieID TEXT,
             movieName TEXT,
             movieYear INTEGER,
             imdbRating REAL)''')
for line in stephen_king_adaptations_list:
    movie_data = line.strip().split(',')
    a.execute("INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)",
              (movie_data[0], movie_data[1], int(movie_data[2]), float(movie_data[3])))
b.commit()
while True:
    print("\n1. Movie name")
    print("2. Movie year")
    print("3. Movie rating")
    print("4. STOP")
    choice = input("Enter your choice: ")
    if choice == '1':
        movie_name = input("Enter the name of the movie: ")
        a.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
        result = a.fetchone()
        if result:
            print("Movie ID:", result[0])
            print("Movie Name:", result[1])
            print("Movie Year:", result[2])
            print("IMDB Rating:", result[3])
        else:
            print("No such movie exists in our database.")
    elif choice == '2':
        movie_year = input("Enter the year of the movies: ")
        a.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (int(movie_year),))
        result = a.fetchall()
        if result:
            print("Movies found in", movie_year, ":")
            for movie in result:
                print("Movie ID:", movie[0])
                print("Movie Name:", movie[1])
                print("Movie Year:", movie[2])
                print("IMDB Rating:", movie[3])
        else:
            print("No movies were found for that year in our database.")
    elif choice == '3':
        rating = input("Enter the minimum rating: ")
        a.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating>=?", (float(rating),))
        result = a.fetchall()
        if result:
            print("Movies with a rating of", rating, "or higher:")
            for movie in result:
                print("Movie ID:", movie[0])
                print("Movie Name:", movie[1])
                print("Movie Year:", movie[2])
                print("IMDB Rating:", movie[3])
        else:
            print("No movies at or above that rating were found in the database.")
    elif choice == '4':
        break
    else:
        print("Can not identify what you input.")
b.close()
