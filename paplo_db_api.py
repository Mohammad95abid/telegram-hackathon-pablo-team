from config import connection
import db_api_utils as utils
from paplo_exceptions import DBException


def create_user(user_id, user_first_name, user_last_name):
    if not utils.is_valid(user_id, user_first_name, user_last_name):
        raise DBException("Invalid user details.")
    try:
        with connection.cursor() as cursor:
            cols = '(user_id, first_name, last_name)'
            vals = "values ('{}', '{}', '{}')".format(user_id, user_first_name, user_last_name)
            query = 'INSERT into users {} {}'.format(cols, vals)
            cursor.execute(query)
            connection.commit()
    except Exception as e:
        print("Error Occurred: ", str(e) )

'''
Checks if book exists, and if it doesnt, it inserts it into the Books table
'''
def add_book(book_title, book_description, book_purchase_link, book_audio_link, book_genre):
    if not utils.is_valid(book_title, book_description, book_purchase_link, book_audio_link, book_genre):
        raise DBException("Invalid user details.")
    try:
        with connection.cursor() as cursor:
            cols = '(title, description_, link_to_buy, audio_book, genre)'
            vals = "values ('{}', '{}', '{}', '{}', '{}')".format(book_title, book_description,
                                                      book_purchase_link, book_audio_link, book_genre)
            query = 'INSERT into books {} {}'.format(cols, vals)
            cursor.execute(query)
            connection.commit()
    except Exception as e:
        print("Error Occurred: ", str(e))


def get_recommendation(user_id):
    pass


def get_recommendation_genre(user_id, book_title):
    pass


def get_recommendation_author(user_id, book_title):
    pass


def add_book_rating(book_title, user_id, rating: bool):
    pass


def add_book_review(book_title, user_id, review):
    pass


def add_book_rating_review(book_title, user_id, rating = None, review = None):
    pass


'''
takes the book title, the user id, a positive or negative rating and a review. 
In case there isnt a review nor a rating. We create a new row in the Reviews table with the values 
    (user_id, title, rating, review)
In case there is a rating, but not a review. Then we insert a new row in the Reviews table with the values
    (user_id, title, rating, NULL)
In case there is a review without a title. Then we check if there exists a row with the user_id and title of book. If 
    there isnt, then we ask the user for his rating. And then we create a new row with the values 
    (user_id, title, rating_taken_from_user, review). In case there is a rating, then we update that row to include the
    review given to us as a parameter.
'''
def update_review(book_title, user_id, rating = None, review = None):
    if rating is None and review is None:
        raise Exception("There need to be information to add")
    if rating is None:
        #TODO make sure you check that book exists. If it doesnt, ask the user for a rating
        return add_book_review(book_title, user_id, review)
    if review is None:
        add_book_rating(book_title, user_id, rating)
    return add_book_rating_review(book_title, user_id, rating, review)


def get_review_with_specific_rating(book_title, user_id, rating:bool):
    pass


def get_review_without_rating(book_title, user_id):
    pass


def get_review(book_title, user_id, rating: bool = None):
    if rating is None:
        return get_review_without_rating(book_title, user_id)
    return get_review_with_specific_rating(book_title, user_id, rating)


# Queries

def get_review_by_user_id(user_id):
    pass

def get_all_users_id():
    pass


