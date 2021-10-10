from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/')
def link():
    return redirect('/authors')

@app.route('/authors')
def authors_page():
    return render_template('authors.html', all_authors = Author.read_all())

@app.route('/create/author', methods = ['post'])
def create_author():
    Author.create(request.form)
    return redirect('/')

@app.route('/authors/<int:id>')
def author_favorites(id):
    data = {
        'id': id
    }
    return render_template('author_favorites.html', author = Author.read_one_with_books(data), book = Book.read_all_not_favorite(data))

@app.route('/create/favorite_book', methods = ['post'])
def add_favorite_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    print(request.form)
    Author.create_favorite_book(data)
    return redirect(f"/authors/{request.form['author_id']}")