from paplo_db_api import *
import random
import re
from  paplo_db_api import  is_user_exist as exist
import goodreads_api_client as gr

def escape_single_quote(text):
    return text.replace("'","`")

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def is_user_exist(user_id):
    return exist(user_id)

def get_description(book_title):
    client = gr.Client(developer_key='q5QJR1BpwdBHs7SLjH0mw')
    book = client.Book.title(book_title)
    description = cleanhtml(book['description'])
    return escape_single_quote( description )

def get_book_id(book_title):
    client = gr.Client(developer_key='<q5QJR1BpwdBHs7SLjH0mw>')
    book = client.Book.title(book_title)
    return book['id']

def get_book_genres(book_title):
    book_id = get_book_id(book_title)
    client = gr.Client(developer_key='<q5QJR1BpwdBHs7SLjH0mw>')
    book = client.Book.show(book_id)
    x = book['popular_shelves']
    res = set()
    for elem in x['shelf']:
        res.add(elem['@name'])
    return res

def get_book_url_from_GR(book_title):
    book_id = get_book_id(book_title)
    client = gr.Client(developer_key='<q5QJR1BpwdBHs7SLjH0mw>')
    book = client.Book.show(book_id)
    return book['link']

def get_buy_link(book_title):
    book_id = get_book_id(book_title)
    client = gr.Client(developer_key='<q5QJR1BpwdBHs7SLjH0mw>')
    book = client.Book.show(book_id)
    isbn = book['isbn']
    if isbn is None:
        return None
    amz = "http://www.amazon.com/dp/{}".format(isbn)
    return amz

def get_book_title_from( book_title ):
    book_id = get_book_id(book_title)
    client = gr.Client(developer_key='<q5QJR1BpwdBHs7SLjH0mw>')
    book = client.Book.show(book_id)
    return book['title']

def rate_book(user_id,book_title,is_like,*args):
    if not exist(user_id):
        first_name=args[0]
        last_name=args[1]
        first_name = escape_single_quote(first_name)
        last_name = escape_single_quote(last_name)
        create_user(user_id,first_name,last_name)

    if not is_book_exist(book_title):
        # description=get_description(book_title)
        # if description is None:
        #     description = "No description found, This is a new book in the system!"
        # description=description[:400]
        # # description = list(description)
        # # if "'" in description:
        # #     description.remove("'")
        # # description=''.join(description)
        # description = escape_single_quote(description)

        add_book(book_title," wow",None,None,"action")

    update_review(book_title,user_id,is_like)




def get_recommendation_author(user_id, book_title):
    client = gr.Client(developer_key='q5QJR1BpwdBHs7SLjH0mw')
    book = client.Book.title(book_title)
    random_author=random.randint(0,len(book['authors']['author'])-1)
    auth_id = book['authors']['author'][random_author]['id']
    random_book=random.randint(0,len(client.Author.books(auth_id)['book'])-1)
    book_to_recommend = client.Author.books(auth_id)['book'][random_book]['title']
    return escape_single_quote(book_to_recommend)

def get_review_by_booktitle(user_reviews,book_title):
    book_title = escape_single_quote(book_title)
    for review in user_reviews:
        if review['book_title'] == book_title:
            return review
    return None

def get_recomndition_book(user_id):
    user_id = str(user_id)
    user_reviews = get_review_by_user_id(user_id)
    all_user = get_all_users_id()
    max = 0
    new_book_to_recommend = None
    max_similarty_user = None

    for user in all_user:
        similarity = 0
        book_to_recommend = []
        if user['user_id'] == user_id:
            continue
        cur_user_reviews = get_review_by_user_id(user['user_id'])
        for review in cur_user_reviews:
            cur_review = get_review_by_booktitle(user_reviews, review['book_title'])
            if cur_review == None:
                book_to_recommend.append(review['book_title'])
                continue
            is_like1=is_user_like_a_book(cur_review['book_title'],cur_review['user_id'])
            is_like2=is_user_like_a_book(review['book_title'],review['user_id'])
            if (is_like1 == True and is_like2 == False) or (is_like1 == False and is_like2 == True):
                similarity-=1

            elif (is_like1 == False and is_like2 == False) or (is_like1 == True and is_like2 == True) :
                similarity+=1

        if max_similarty_user == None:
            max=similarity
            max_similarty_user=user['user_id']
            new_book_to_recommend=book_to_recommend

        elif similarity > max:
            max=similarity
            max_similarty_user=user['user_id']
            new_book_to_recommend = book_to_recommend
    if len(new_book_to_recommend) > 0:
        return random.choice(new_book_to_recommend)

def review_book(user_id, book_title, review):
    return update_review(book_title, user_id, None, review)

def get_book_author(book_title):
    book_id = get_book_id(book_title)
    client = gr.Client(developer_key='<q5QJR1BpwdBHs7SLjH0mw>')
    book = client.Book.show(book_id)
    authors = book['authors']['author']
    res = []
    for elem in authors:
        if elem:
            try:
                res.append( escape_single_quote( elem['name'] ) )
            except TypeError as e:
                res.append(escape_single_quote( authors['name'] ))
                break
    return res

def get_review_from_db(ratting = None):
    if ratting is None:
        return get_all_reviews()
    elif ratting:
        return get_all_positive_reviews()
    else:
        return get_all_negative_reviews()


#print(get_recomndition_book("15egT4"))
#rate_book("123","My Book2",False,"serigio","ramos")
#rate_book("eut12335","Best Mystery Books",False)
#rate_book("eut12335","1984, George Orwell",True)
#print(get_description("The Last Wish (The Witcher, #0.5)"))

