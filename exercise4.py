import sqlite3

# 创建数据库并连接
conn = sqlite3.connect('library.db')
c = conn.cursor()

# 创建表Books
c.execute('''CREATE TABLE IF NOT EXISTS Books
             (BookID INTEGER PRIMARY KEY AUTOINCREMENT,
              Title TEXT NOT NULL,
              Author TEXT NOT NULL,
              ISBN TEXT NOT NULL,
              Status TEXT NOT NULL)''')

# 创建表Users
c.execute('''CREATE TABLE IF NOT EXISTS Users
             (UserID INTEGER PRIMARY KEY AUTOINCREMENT,
              Name TEXT NOT NULL,
              Email TEXT NOT NULL)''')

# 创建表Reservations
c.execute('''CREATE TABLE IF NOT EXISTS Reservations
             (ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
              BookID INTEGER,
              UserID INTEGER,
              ReservationDate TEXT,
              FOREIGN KEY (BookID) REFERENCES Books(BookID),
              FOREIGN KEY (UserID) REFERENCES Users(UserID))''')


def add_book(title, author, isbn, status):
    # 添加书籍到Books表
    c.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)",
              (title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")


def find_book_details_by_id(book_id):
    # 根据BookID查找书籍详情
    c.execute("SELECT Books.*, Users.Name, Users.Email FROM Books "
              "INNER JOIN Reservations ON Books.BookID = Reservations.BookID "
              "INNER JOIN Users ON Reservations.UserID = Users.UserID "
              "WHERE Books.BookID = ?", (book_id,))
    result = c.fetchone()
    if result:
        book_id, title, author, isbn, status, user_name, user_email = result
        print("Book ID:", book_id)
        print("Book title:", title)
        print("Author:", author)
        print("ISBN:", isbn)
        print("Status:", status)
        print("Booker Name:", user_name)
        print("Booker Mail:", user_email)
    else:
        print("The book does not exist or has not been booked.")


def find_book_reservation_status(book_info):
    # 根据BookID、Title、UserID和ReservationID查找书籍的预订状态
    if book_info.startswith("LB"):
        # 根据BookID查找
        c.execute("SELECT Status FROM Books WHERE BookID = ?", (book_info,))
    elif book_info.startswith("LU"):
        # 根据UserID查找
        c.execute("SELECT Books.Status FROM Books "
                  "INNER JOIN Reservations ON Books.BookID = Reservations.BookID "
                  "INNER JOIN Users ON Reservations.UserID = Users.UserID "
                  "WHERE Users.UserID = ?", (book_info,))
    elif book_info.startswith("LR"):
        # 根据ReservationID查找
        c.execute("SELECT Books.Status FROM Books "
                  "INNER JOIN Reservations ON Books.BookID = Reservations.BookID "
                  "WHERE Reservations.ReservationID = ?", (book_info,))
    else:
        # 根据Title查找
        c.execute("SELECT Books.Status FROM Books WHERE Title = ?", (book_info,))

    result = c.fetchone()
    if result:
        status = result[0]
        print("Book booking status:", status)
    else:
        print("The book does not exist or has not been booked.")


def find_all_books():
    # 查找所有书籍
    c.execute("SELECT Books.*, Users.Name, Users.Email, Reservations.ReservationDate FROM Books "
              "LEFT JOIN Reservations ON Books.BookID = Reservations.BookID "
              "LEFT JOIN Users ON Reservations.UserID = Users.UserID")
    results = c.fetchall()
    if results:
        for result in results:
            book_id, title, author, isbn, status, user_name, user_email, reservation_date = result
            print("Book ID:", book_id)
            print("Book Name:", title)
            print("Author:", author)
            print("ISBN:", isbn)
            print("Status:", status)
            print("Booker name:", user_name)
            print("Booker mail:", user_email)
            print("Booking date :", reservation_date)
            print("------------------")
    else:
        print("No books were found.")


def modify_book_details(book_id, title=None, author=None, isbn=None, status=None):
    # 根据BookID修改书籍详情
    if title:
        c.execute("UPDATE Books SET Title = ? WHERE BookID = ?", (title, book_id))
    if author:
        c.execute("UPDATE Books SET Author = ? WHERE BookID = ?", (author, book_id))
    if isbn:
        c.execute("UPDATE Books SET ISBN = ? WHERE BookID = ?", (isbn, book_id))
    if status:
        c.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (status, book_id))
        c.execute("UPDATE Reservations SET Status = ? WHERE BookID = ?", (status, book_id))
    conn.commit()
    print("Book details modified successfully!")


def delete_book(book_id):
    # 根据BookID删除书籍
    c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    c.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully!")


def exit_program():
    # 退出程序
    conn.close()
    print("The program has exited.")


# 主程序
while True:
    print("Please select an action:")
    print("1. Add New Book")
    print("2. Find book details based on BookID")
    print("3. Find the booking status of books based on BookID, Title, UserID, and ReservationID")
    print("4. Find all books")
    print("5. Modifying Book Details")
    print("6. Delete books based on BookID")
    print("7. Exit program")
    choice = input("Please enter the option number: ")
    
    if choice == "1":
        title = input("Please enter the book name: ")
        author = input("Please enter the author's name: ")
        isbn = input("Please enter ISBN: ")
        status = input("Please enter the book status: ")
        add_book(title, author, isbn, status)
    elif choice == "2":
        book_id = input("Please enter BookID: ")
        find_book_details_by_id(book_id)
    elif choice == "3":
        book_info = input("Please enter BookID, Title, UserID, or ReservationID: ")
        find_book_reservation_status(book_info)
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        book_id = input("Please enter BookID:")
        title = input("Please enter a new book name (press Enter to skip): ")
        author = input("Please enter the new author name (press Enter to skip): ")
        isbn = input("Please enter a new ISBN (press Enter to skip): ")
        status = input("Please enter the new book status (press Enter to skip): ")
        modify_book_details(book_id, title, author, isbn, status)
    elif choice == "6":
        book_id = input("Please enter BookID: ")
        delete_book(book_id)
    elif choice == "7":
        exit_program()
        break
    else:
        print("Invalid option, please reselect.")
