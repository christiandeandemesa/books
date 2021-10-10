from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);'
        result = connectToMySQL('books_schema').query_db(query, data)
        return result

    @classmethod
    def read_all(cls):
        query = 'SELECT * FROM books ORDER BY title;'
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def read_one_with_authors(cls, data):
        query = 'SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;'
        result = connectToMySQL('books_schema').query_db(query, data)
        book = cls(result[0])
        for row in result:
            authors_data = {
                'id': row['authors.id'],
                'name': row['name'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            book.authors.append(author.Author(authors_data))
        return book

    @classmethod
    def create_favorite_author(cls, data):
        query = "INSERT INTO favorites (book_id, author_id) VALUES (%(book_id)s, %(author_id)s);"
        result = connectToMySQL('books_schema').query_db(query,data)
        return result

    @classmethod
    def read_all_not_favorite(cls,data):
        query = 'SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );'
        results = connectToMySQL('books_schema').query_db(query,data)
        books = []
        for row in results:
            books.append(cls(row))
        return books