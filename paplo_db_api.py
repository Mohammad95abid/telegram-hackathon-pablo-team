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
            return True
    except Exception as e:
        message = "Error Occurred: " + str(e)
        raise DBException(message)
    return False

'''
Checks if book exists, and if it doesnt, it inserts it into the Books table
'''
def add_book(book_title, book_description, book_purchase_link, book_audio_link, book_genre):
    if not utils.is_valid(book_title, book_description, book_purchase_link, book_audio_link, book_genre):
        raise DBException("Invalid book details.")
    try:
        with connection.cursor() as cursor:
            cols = '(title, description_, link_to_buy, audio_book, genre)'
            vals = "values ('{}', '{}', '{}', '{}', '{}')".format(book_title, book_description,
                                                      book_purchase_link, book_audio_link, book_genre)
            query = 'INSERT into books {} {}'.format(cols, vals)
            cursor.execute(query)
            connection.commit()
            return True
    except Exception as e:
        message = "Error Occurred: " + str(e)
        raise DBException(message)
    return False

"""
def get_recommendation(user_id):
    pass


def get_recommendation_genre(user_id, book_title):
    pass


def get_recommendation_author(user_id, book_title):
    pass

"""

def is_book_review_exist(book_title, user_id):
    with connection.cursor() as cursor:
        condition = "user_id like '{}' and book_title like '{}' ".format(user_id, book_title)
        query = "SELECT * FROM reviews WHERE {}".format(condition)
        cursor.execute(query)
        return len(cursor.fetchall()) > 0

def is_user_exist(user_id):
    ust = type( user_id )
    with connection.cursor() as cursor:
        condition = "user_id like '{}' ".format(user_id)
        query = "SELECT * FROM users WHERE {}".format(condition)
        cursor.execute(query)
        return len( cursor.fetchall() ) > 0

def add_book_rating(book_title, user_id, rating: bool):
    try:
        with connection.cursor() as cursor:
            # there are two cases, add new review when no instance of both book_title, user_id in the table
            # otherwise just update the exist raw with new rating
            # make add query
            like_ = 1 if rating else 0
            cols = '(user_id, book_title, like_)'
            vals = "('{}', '{}', b'{}')".format(user_id, book_title, like_)
            query = 'INSERT into reviews {} values {}'.format(cols, vals)
            if is_book_review_exist(book_title, user_id):
                # make update query
                condition = "user_id = '{}' and book_title = '{}'".format(user_id, book_title)
                query = "UPDATE reviews SET like_ = b'{}' WHERE {}".format(like_, condition)
            cursor.execute(query)
            connection.commit()
            return True
    except Exception as e:
        message = "Error Occurred: " + str(e)
        raise DBException(message)
    return False


def add_book_review(book_title, user_id, review):
    try:
        with connection.cursor() as cursor:
            condition = "user_id = '{}' and book_title = '{}'".format(user_id, book_title)
            query = "UPDATE reviews SET review = '{}' WHERE {}".format(review, condition)
            cursor.execute(query)
            connection.commit()
            return True
    except Exception as e:
        message = "Error Occurred: " + str(e)
        raise DBException(message)
    return False

def add_book_rating_review(book_title, user_id, rating = None, review = None):
    try:
        with connection.cursor() as cursor:
            like_  = 1 if rating else 0
            cols = '(user_id, book_title, like_, review)'
            vals = "('{}', '{}', b'{}', '{}')".format(user_id, book_title, like_, review)
            query = 'INSERT into reviews {} values {}'.format(cols, vals)
            cursor.execute(query)
            connection.commit()
            return True
    except Exception as e:
        message = "Error Occurred: " + str(e)
        raise DBException(message)
    return False

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
    if not utils.is_valid(book_title, user_id):
        raise DBException("Invalid book, user details.")
    elif rating is None and not is_user_exist(user_id):
        raise DBException("user not exist in the system")
    elif rating is None and review is None:
        raise DBException("There need to be information to add")
    elif rating is None and is_book_review_exist(book_title, user_id):
        #TODO make sure you check that book exists. If it doesnt, ask the user for a rating
        return add_book_review(book_title, user_id, review)
    elif review is None:
        return add_book_rating(book_title, user_id, rating)
    return add_book_rating_review(book_title, user_id, rating, review)


def get_review_with_specific_rating(book_title, user_id, rating:bool):
    with connection.cursor() as cursor:
        rating = 1 if rating else 0
        condition = "user_id like '{}' and book_title like '{}' and like_ = b'{}'"\
            .format(user_id, book_title, rating)
        query = "SELECT * FROM reviews WHERE {}".format(condition)
        cursor.execute(query)
        return cursor.fetchone()


def get_review_without_rating(book_title, user_id):
    with connection.cursor() as cursor:
        query = "SELECT * FROM reviews WHERE user_id like '{}' and book_title like '{}'" \
            .format(user_id, book_title)
        cursor.execute(query)
        return cursor.fetchone()


def get_review(book_title, user_id, rating: bool = None):
    if not utils.is_valid(book_title, user_id):
        raise DBException("Invalid book, user details.")
    if rating is None:
        return get_review_without_rating(book_title, user_id)
    return get_review_with_specific_rating(book_title, user_id, rating)


# Queries
'''
a function to get all book reviews for this user
parameters: user id
return a list of dictionaries, each one is the book reviewed by the user
'''
def get_review_by_user_id(user_id):
    if not utils.is_valid(user_id):
        raise DBException("Invalid user details.")
    with connection.cursor() as cursor:
        query = "SELECT * FROM reviews WHERE user_id like '{}'".format(user_id)
        cursor.execute(query)
        return cursor.fetchall()

def get_all_users_id():
    with connection.cursor() as cursor:
        query = "SELECT user_id FROM users"
        cursor.execute(query)
        return cursor.fetchall()


def show_table(table_name):
    if not utils.is_valid(table_name):
        raise DBException("Invalid table name details.")
    with connection.cursor() as cursor:
        query = "SELECT * FROM {}".format(table_name)
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)

def is_book_exist(book_title):
    if not utils.is_valid(book_title):
        raise DBException("Invalid book title details.")
    with connection.cursor() as cursor:
        condition = "title like '{}' ".format( book_title )
        query = "SELECT * FROM books WHERE {}".format(condition)
        cursor.execute(query)
        return len(cursor.fetchall()) > 0

def get_book(book_title):
    if not utils.is_valid(book_title):
        raise DBException("Invalid book title details.")
    with connection.cursor() as cursor:
        condition = "title like '{}' ".format( book_title )
        query = "SELECT * FROM books WHERE {}".format(condition)
        cursor.execute(query)
        return cursor.fetchone()

def is_user_like_a_book(book_title, user_id):
    if not utils.is_valid(user_id):
        raise DBException("Invalid user details.")
    with connection.cursor() as cursor:
        condition = "user_id like '{}' and book_title like '{}' ".format(user_id, book_title)
        query = "SELECT * FROM reviews WHERE {}".format(condition)
        cursor.execute(query)
        res = cursor.fetchone()
        return int.from_bytes(res['like_'], byteorder='big', signed=True) == 1
    return False