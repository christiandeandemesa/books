from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.book import Book
from flask_app.models.author import Author

@app.route('/books')
def books_page():
    return render_template('books.html', all_books = Book.read_all())

@app.route('/create/book', methods = ['post'])
def create_book():
    Book.create(request.form)
    return redirect('/books')

@app.route('/books/<int:id>')
def book_favorites(id):
    data = {
        'id': id
    }
    return render_template('book_favorites.html', book = Book.read_one_with_authors(data), author = Author.read_all_not_favorite(data))

@app.route('/create/favorite_author', methods = ['post'])
def add_favorite_author():
    data = {
        'book_id': request.form['book_id'],
        'author_id': request.form['author_id']
    }
    Book.create_favorite_author(data)
    return redirect(f"/books/{request.form['book_id']}")