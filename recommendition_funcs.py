

from paplo_db_api import get_review_by_user_id,get_all_users_id
import random
import goodreads_api_client as gr

#def get_description(book_title):
 #   client = gr.Client(developer_key='q5QJR1BpwdBHs7SLjH0mw')
  #  book = client.Book.title(book_title)
   # print(book)
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

def get_book(user_id):
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

            if (cur_review['like_'] == True and review['like_'] == False) or (cur_review['like_'] == False and review['like_'] == True):
                similarity-=1

            elif (cur_review['like_'] == True and review['like_'] == True) or (cur_review['like_'] == False and review['like_'] == False):
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


#get_description("The Last Wish (The Witcher, #0.5)")