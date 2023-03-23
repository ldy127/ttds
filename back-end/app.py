from search import app
from search.routes import search

DEBUG = True

if __name__ == '__main__':
    app.run(debug=True)
    # search()