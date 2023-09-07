from flask import Flask, redirect, render_template, url_for, request
from init_db import Database


app = Flask(__name__)
db = Database()

# головна сторінка
@app.route('/')
def main():
    return render_template('index.html')


# сторінка з представленням списку всіх письменників
@app.route('/writers')
def writers():
    db.connect()
    db.cursor.execute('SELECT image, name, information FROM writers;')
    writers = db.cursor.fetchall()
    db.disconnect()
    return render_template('writers.html', writers = writers)


# сторінка з представленням списку всіх книг по рейтингу
@app.route('/books')
def books():
    db.connect()
    db.cursor.execute('SELECT books.image, books.name, books.information, books.year, books.raiting, writers.name FROM books JOIN writers ON writers.Id = books.author_id ORDER BY books.raiting;')
    books = db.cursor.fetchall()
    db.disconnect()
    return render_template('books.html', books = books)


# сторінка з представленням інформації про конкретного письменника та перелік його книг
@app.route('/writers/<string:writer_name>')
def writer_info(writer_name):
    db.connect()
    db.cursor.execute(f"SELECT books.image, books.name, books.information, books.year, books.raiting, writers.image, writers.name, writers.information FROM books JOIN writers ON writers.Id = books.author_id WHERE writers.name  = '{writer_name}'")
    writer_info = db.cursor.fetchall()
    if len(writer_info)!=0:
        db.disconnect()
        return render_template('writer.html', writers_info = writer_info)
    else:
        return redirect('/writers')

# сторінка з представленням інформації про конкретну книгу
@app.route('/writers/<string:writer_name>/<string:book_name>')
def book_info(writer_name, book_name):
    db.connect()
    db.cursor.execute(f"SELECT books.image, books.name, books.information, books.year, books.raiting, writers.image, writers.name, writers.information FROM books JOIN writers ON writers.Id = books.author_id WHERE books.name = '{book_name}' AND writers.name = '{writer_name}'")
    books_info = db.cursor.fetchone()
    if books_info!=None:
        db.disconnect()
        return render_template('book.html', books_info = books_info)
    
    db.cursor.execute(f"SELECT books.image, books.name, books.information, books.year, books.raiting, writers.image, writers.name, writers.information FROM books JOIN writers ON writers.Id = books.author_id WHERE writers.name = '{writer_name}'")
    writer_info = db.cursor.fetchall()
    db.disconnect()
    if len(writer_info)!=0:
        return redirect(url_for('writer_info', writer_name = writer_info[0][6]))
    else:
        return redirect('/writers')


# можливість витягувати книги по рейтингу
@app.route('/books/<int:raiting>')
def book_info_by_raiting(raiting):
    db.connect()
    db.cursor.execute(f"SELECT books.image, books.name, books.information, books.year, books.raiting, writers.image, writers.name, writers.information FROM books JOIN writers ON writers.Id = books.author_id WHERE books.raiting = '{raiting}'")
    books_info = db.cursor.fetchone()
    db.disconnect()
    if books_info!=None:
        return render_template('book.html', books_info = books_info)
    else:
        return redirect('/books')
    




# можливість витягувати книги по письменнику та року написання
@app.route('/writers/')
@app.route('/cities/')
def books_by_year():
    writer_name = request.args.get('writers')
    year = request.args.get('year')
    db.connect()
    db.cursor.execute(f"SELECT books.image, books.name, books.information, books.year, books.raiting, writers.image, writers.name, writers.information FROM books JOIN writers ON writers.Id = books.author_id WHERE writers.name  = '{writer_name}' and books.year={year}")
    books_info = db.cursor.fetchone()
    if books_info!=None:
        db.disconnect()
        return render_template('book.html',books_info = books_info)
    db.cursor.execute(f"SELECT books.image, books.name, books.information, books.year, books.raiting, writers.image, writers.name, writers.information FROM books JOIN writers ON writers.Id = books.author_id WHERE writers.name  = '{writer_name}'")
    writer_info = db.cursor.fetchall()
    db.disconnect()
    if len(writer_info)!=0:
        return redirect(url_for('writer_info', writer_name = writer_info[0][6]))
    else:
        return redirect('/writers')
    

# сторінка пошуку
@app.route('/search')
def search():
    return render_template('search.html', books = None)


@app.route('/process_form', methods=['POST'])
def process_form():
    writer_name = request.form['writer_name']
    book_name = request.form['book_name']
    book_year = request.form['book_year']
    db.connect()
    if book_year!='':
        db.cursor.execute(f"SELECT books.image, books.name, books.information, books.year, books.raiting, writers.image, writers.name, writers.information FROM books JOIN writers ON writers.Id = books.author_id WHERE writers.name  ILIKE  '%{writer_name}%' AND books.name  ILIKE  '%{book_name}%' AND books.year = {book_year} ")
        books = db.cursor.fetchall()
        db.disconnect()
        return render_template('search.html', books = books)
    else:
        db.cursor.execute(f"SELECT books.image, books.name, books.information, books.year, books.raiting, writers.image, writers.name, writers.information FROM books JOIN writers ON writers.Id = books.author_id WHERE writers.name  ILIKE  '%{writer_name}%' AND books.name  ILIKE  '%{book_name}%' ")
        books = db.cursor.fetchall()
        db.disconnect()
        return render_template('search.html', books = books)

    
if __name__ == '__main__':
    app.run(debug=True, port=8000)