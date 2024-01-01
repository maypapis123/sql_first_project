from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("library.db", check_same_thread=False)
cur = con.cursor()

try:
    cur.execute("CREATE TABLE IF NOT EXISTS books (name TEXT, author TEXT)")
except Exception as e:
    print(f"Error: {e}")

@app.route('/')
def home():
    cur.execute("SELECT rowid,* FROM books")
    books = cur.fetchall()
    return render_template("main.html", books=books)

@app.route('/books')
def books():
    cur.execute("SELECT rowid,* FROM books")
    books = cur.fetchall()
    print(books)
    return render_template("books.html", msg="Welcome to my library", books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        cur.execute("INSERT INTO books (name, author) VALUES (?, ?)", (name, author))
        con.commit()
        return redirect(url_for('home'))
    return render_template("add_book.html")

@app.route('/books_list')
def books_list():
    cur.execute("SELECT rowid,* FROM books")
    books = cur.fetchall()
    return render_template("books_list.html", books=books)

@app.route('/delete_book/<int:book_id>', methods=['POST', 'GET'])
def delete_book(book_id):
    if request.method == 'POST':
        cur.execute("DELETE FROM books WHERE rowid=?", (book_id,))
        con.commit()
        return redirect('/books_list')
    return redirect('/books_list')  # Redirect to book list page if accessed with GET method



if __name__ == '__main__':
    app.run(debug=True)

# Close the database connection when the application is terminated
con.close()
