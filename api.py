import flask
from flask import request, jsonify
import sqlite3

# Creates the Flask application object.
app = flask.Flask(__name__)

# Starts the debugger.
app.config["DEBUG"] = True


# Test data in the form of dictionaries.
# books = [
#     {
#         'id': 0,
#         'title': 'A Fire Upon the Deep',
#         'author': 'Vernor Vinge',
#         'first_sentence': 'The coldsleep itself was dreamless.',
#         'year_published': '1992'
#     },
#     {
#         'id': 1,
#         'title': 'The Ones Who Walk Away From Omelas',
#         'author': 'Ursula K. Le Guin',
#         'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#         'published': '1973'
#     },
#     {
#         'id': 2,
#         'title': 'Dhalgren',
#         'author': 'Samuel R. Delany',
#         'first_sentence': 'to wound the autumnal city.',
#         'published': '1975'
#     }
# ]

def dict_factory(cursor, row):
    """Returns items from database as dictionaries rather than lists."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    """Simple home page"""
    return """<h1>Distant Reading Archive</h1>
    <p>This site is a prototype API for distant reading of science fiction novels.</p>"""


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    """
    Connects to the database to retrieve all books data.
    Lets the connection object know how to use the dict_factory function.
    Cursor moves through the database to pull data.
    SQL query is executed and returned as JSON.
    """
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)


@app.errorhandler(404)
def page_not_found(e):
    """Handles errors and invalid route inputs."""
    return '<h1>404</h1>\
        <p>The resource could not be found.</p>', 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    """
    Returns a book based on its id, published, and author.
    Grabs query parameters provided in the URL and binds them to variables.
    SQL query and filters required to pull the correct books from the database.
    Handles error if not a valid query.
    Connects to database and returns JSON data to user.
    """
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = 'SELECT * FROM books WHERE'
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)
    
    # Remove the trailing 'AND', and cap the query with ';' required for SQL.
    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory =  dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)
    
# Method to use if using test data in the form of dictionaries.
# @app.route('/api/v1/resources/books', methods=['GET'])
# def api_id():
#     """
#     Check if an ID was provided as part of the URL.
#     If ID is provided, assign it to a variable.
#     If no ID is provided, display an error in the browser.
#     """
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return 'Error: No id field provided. Please specify an id.'

#     # An empty list of results.
#     results = []


#     # Loop through the data and match results that fit the requested ID.
#     for book in books:
#         if book['id'] == id:
#             results.append(book)

#     # Using jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)

# To run the application on web browser.
app.run()