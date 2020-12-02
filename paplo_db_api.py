from config import connection
import db_api_utils as utils
from paplo_exceptions import DBException


def escape_single_quote(text):
    return text.replace("'","`")

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
def add_book(book_title, book_purchase_link, book_audio_link):
    book_title = escape_single_quote(book_title)
    if not utils.is_valid(book_title):
        raise DBException("Invalid book details.")
    try:
        with connection.cursor() as cursor:
            cols = '(title, link_to_buy, audio_book)'
            vals = "values ('{}', '{}', '{}')".format(book_title, book_purchase_link, book_audio_link)
            if book_purchase_link is  None and book_audio_link is  None:
                vals = "values ('{}', NULL, NULL);".format(book_title)
            elif book_purchase_link is  None:
                vals = "values ('{}', NULL, '{}');".format(book_title, book_audio_link)
            elif book_audio_link is  None:
                vals = "values ('{}', '{}', NULL);".format(book_title, book_purchase_link)
            query = 'INSERT into books {} {}'.format(cols, vals)
            print(query)
            cursor.execute(query)
            connection.commit()
            return True
    except Exception as e:
        message = "Error Occurred: " + str(e)
        raise DBException(message)
    return False

def is_book_review_exist(book_title, user_id):
    book_title = escape_single_quote(book_title)
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
    book_title = escape_single_quote(book_title)
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
    book_title = escape_single_quote(book_title)
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
    book_title = escape_single_quote(book_title)
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
    book_title = escape_single_quote(book_title)
    if not utils.is_valid(book_title, user_id):
        raise DBException("Invalid book, user details.")
    elif rating is None and not is_user_exist( user_id ):
        raise DBException("user not exist in the system")
    elif rating is None and not is_book_review_exist(book_title, user_id):
        raise DBException("Book review not exist in the system")
    elif rating is None and review is None:
        raise DBException("There need to be information to add")
    elif rating is None and is_book_review_exist(book_title, user_id):
        #TODO make sure you check that book exists. If it doesnt, ask the user for a rating
        return add_book_review(book_title, user_id, review)
    elif review is None:
        return add_book_rating(book_title, user_id, rating)
    return add_book_rating_review(book_title, user_id, rating, review)


def get_review_with_specific_rating(book_title, user_id, rating:bool):
    book_title = escape_single_quote(book_title)
    with connection.cursor() as cursor:
        rating = 1 if rating else 0
        condition = "user_id like '{}' and book_title like '{}' and like_ = b'{}'"\
            .format(user_id, book_title, rating)
        query = "SELECT * FROM reviews WHERE {}".format(condition)
        cursor.execute(query)
        return cursor.fetchone()


def get_review_without_rating(book_title, user_id):
    book_title = escape_single_quote(book_title)
    with connection.cursor() as cursor:
        query = "SELECT * FROM reviews WHERE user_id like '{}' and book_title like '{}'" \
            .format(user_id, book_title)
        cursor.execute(query)
        return cursor.fetchone()


def get_review(book_title, user_id, rating: bool = None):
    book_title = escape_single_quote(book_title)
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
    book_title = escape_single_quote(book_title)
    if not utils.is_valid(book_title):
        raise DBException("Invalid book title details.")
    with connection.cursor() as cursor:
        condition = "title like '{}' ".format( book_title )
        query = "SELECT * FROM books WHERE {}".format(condition)
        cursor.execute(query)
        return len(cursor.fetchall()) > 0

def get_book(book_title):
    book_title = escape_single_quote(book_title)
    if not utils.is_valid(book_title):
        raise DBException("Invalid book title details.")
    with connection.cursor() as cursor:
        condition = "title like '{}' ".format( book_title )
        query = "SELECT * FROM books WHERE {}".format(condition)
        cursor.execute(query)
        return cursor.fetchone()

def is_user_like_a_book(book_title, user_id):
    book_title = escape_single_quote(book_title)
    if not utils.is_valid(user_id):
        raise DBException("Invalid user details.")
    with connection.cursor() as cursor:
        condition = "user_id like '{}' and book_title like '{}' ".format(user_id, book_title)
        query = "SELECT * FROM reviews WHERE {}".format(condition)
        cursor.execute(query)
        res = cursor.fetchone()
        return int.from_bytes(res['like_'], byteorder='big', signed=True) == 1
    return False

def get_all_positive_reviews():
    with connection.cursor() as cursor:
        condition  = "WHERE like_ = '1' "
        query = "SELECT * FROM reviews {}".format(condition)
        cursor.execute(query)
        res = cursor.fetchall()
        for review in res:
            review['like_'] = True
        return res

def get_all_negative_reviews():
    with connection.cursor() as cursor:
        condition  = "WHERE like_ = '0' "
        query = "SELECT * FROM reviews {}".format(condition)
        cursor.execute(query)
        res = cursor.fetchall()
        for review in res:
            review['like_'] = False
        return res

def convert_bit_to_bool(data):
    for review in data:
        if int.from_bytes(review['like_'], byteorder='big', signed=True) == 1:
            review['like_'] = True
        else:
            review['like_'] = False
    return data

def convert_bool_to_ratting(bool_):
    return 1 if bool_ else 0

def get_all_reviews():
    with connection.cursor() as cursor:
        query = "SELECT * FROM reviews;"
        cursor.execute(query)
        res = cursor.fetchall()
        for review in res:
            if int.from_bytes(review['like_'], byteorder='big', signed=True) == 1:
                review['like_'] = True
            else:
                review['like_'] = False
        return res

def get_all_review_by_book_title(book_title, ratting = None):
    book_title = escape_single_quote(book_title)
    if 
    with connection.cursor() as cursor:
        condition = "book_title like '{}' and like_ = '{}'".format(book_title, convert_bool_to_ratting(ratting))
        if ratting is None:
            condition = "book_title like '{}'".format(book_title)
        query = "SELECT * FROM reviews WHERE {};".format(condition)
        cursor.execute(query)
        res = cursor.fetchall()
        return convert_bit_to_bool(res)

def get_all_users_love_book(book_title):
    book_title = escape_single_quote(book_title)
    data = get_all_review_by_book_title(book_title, True)
    users_by_id = [user['user_id'] for user in data]
    return list(set(users_by_id))

def get_all_pos_ratting_books_by_user(user_id):
    with connection.cursor() as cursor:
        condition = "user_id like '{}' and like_ = '1'".format(user_id)
        query = "SELECT * FROM reviews WHERE {};".format(condition)
        cursor.execute(query)
        res = cursor.fetchall()
        return list(set([review['book_title'] for review in res]))

def git_all_pos_rating_books_of_users(users_id):
    res = []
    for user_id in users_id:
        for book in get_all_pos_ratting_books_by_user(user_id):
            res.append(book)
    return list(set(res))

def get_recommendations_books(user_id, book_title):
    book_title = escape_single_quote(book_title)
    with connection.cursor() as cursor:
        condition = "user_id like '{}' ".format(user_id)
        query = "SELECT * FROM reviews WHERE {};".format(condition)
        cursor.execute(query)
        res = cursor.fetchall()
        user_reviews = list(set([review['book_title'] for review in res]))
        books_to_reco = git_all_pos_rating_books_of_users(get_all_users_love_book(book_title))
        res = [ book for book in books_to_reco if book not in user_reviews ]
        return res


