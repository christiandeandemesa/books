from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []
    
    @classmethod
    def create(cls, data):
        query = 'INSERT INTO authors (name) VALUES (%(name)s);'
        result = connectToMySQL('books_schema').query_db(query, data)
        return result

    @classmethod
    def read_all(cls):
        query = 'SELECT * FROM authors ORDER BY name;'
        results = connectToMySQL('books_schema').query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def read_one_with_books(cls, data):
        query = 'SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;'
        result = connectToMySQL('books_schema').query_db(query, data)
        author = cls(result[0])
        for row in result:
            books_data = {
                'id': row['books.id'],
                'title': row['title'],
                'num_of_pages': row['num_of_pages'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            author.books.append(book.Book(books_data))
        return author

    @classmethod
    def create_favorite_book(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        result = connectToMySQL('books_schema').query_db(query,data)
        return result

    @classmethod
    def read_all_not_favorite(cls,data):
        query = 'SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );'
        results = connectToMySQL('books_schema').query_db(query,data)
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors