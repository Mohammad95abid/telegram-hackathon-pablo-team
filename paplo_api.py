from flask import Flask, request

app = Flask(__name__)

# @app.route("/")
# def add_new_user():
#     pass

@app.route('/get_recommendation/<user_id>',)
def get_recommendation(user_id):
    pass

@app.route('/add_rating', methods=["POST"])
def like_book(book_title, user_id, ratting: bool):
    pass

@app.route('/add_review', methods=["POST"])
def add_review():
    pass

@app.route('/get_review', methods=["POST"])
def get_review(book_title, user_id, ratting: bool):
    pass