from paplo_db_api import *
import random
import re
from  paplo_db_api import  is_user_exist as exist
import goodreads_api_client as gr
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def is_user_exist(user_id):
    return exist(user_id)
def get_description(book_title):
    client = gr.Client(developer_key='q5QJR1BpwdBHs7SLjH0mw')
    book = client.Book.title(book_title)
    return book['description']

def rate_book(user_id,book_title,is_like,*args):
    if not exist(user_id):
        first_name=args[0]
        last_name=args[1]
        create_user(user_id,first_name,last_name)

    if not is_book_exist(book_title):
        description=get_description(book_title)
        description=cleanhtml(description)
        description=description[:400]
        description = list(description)
        description.remove("'")
        description=''.join(description)
        #description.replace("\'","")

        add_book(book_title,description,None,None,"action")

    update_review(book_title,user_id,is_like)




def get_recommendation_author(user_id, book_title):
    client = gr.Client(developer_key='q5QJR1BpwdBHs7SLjH0mw')
    book = client.Book.title(book_title)
    random_author=random.randint(0,len(book['authors']['author'])-1)
    auth_id = book['authors']['author'][random_author]['id']
    random_book=random.randint(0,len(client.Author.books(auth_id)['book'])-1)
    book_to_recommend = client.Author.books(auth_id)['book'][random_book]['title']
    return book_to_recommend
def get_review_by_booktitle(user_reviews,book_title):
    for review in user_reviews:
        if review['book_title'] == book_title:
            return review
    return None

def get_recomndition_book(user_id):
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

    return random.choice(new_book_to_recommend)



#print(get_recomndition_book("15egT4"))
#rate_book("123","My Book2",False,"serigio","ramos")
#rate_book("eut12335","Best Mystery Books",False)
#rate_book("eut12335","1984, George Orwell",True)
#print(get_description("The Last Wish (The Witcher, #0.5)"))