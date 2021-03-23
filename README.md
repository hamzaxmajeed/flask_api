# Distant Reading Archive API using Flask and SQLite

Contains the id, published, author, title and first_sentence on books that won the Hugo award in the year under the published heading.

## Setup

Ensure you have python 3.6+ installed.

```bash
pip install -r requirements
```

## To Run Application

In the terminal, enter the command:
```bash
python api.py
```

After running the application, try out the filtering functionality with these HTTP requests:

[All books](http://127.0.0.1:5000/api/v1/resources/books/all)
[Author: Connie Willis](http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis)
[Author: Connie Willis & Published: 1999](http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis&published=1999)
[Published: 2019](http://127.0.0.1:5000/api/v1/resources/books?published=2010)
