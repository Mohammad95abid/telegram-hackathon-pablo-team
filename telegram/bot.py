from flask import request
import recommendition_funcs as funcs
import config
import requests
from telegram.node import Node

''' 
Commands:

1)/start
2)/description of bot
3)/rate_book
4)/get_recommendation
5)/get_library
6)/review_book
7)/get_review
8)/get_recommendation_by_genre
9)/get_recommendation_by_author
10)/get_purchase_link
11)/get_audio_link
12)/connect_to_user
'''


class Bot:


    actionDict = dict()
    # @staticmethod
    # def fill_empty_action_dict(empty_dict):
    #     empty_dict["start"] = 0
    #     empty_dict["rate_book"] = 0
    #     empty_dict["get_recommendation"] = 0
    #     empty_dict["get_library"] = 0
    #     empty_dict["review_book"] = 0
    #     empty_dict["get_review"] = 0
    #     empty_dict["get_recommendation_by_genre"] = 0
    #     empty_dict["get_recommendation_by_author"] = 0
    #     empty_dict["get_purchase_link"] = 0
    #     empty_dict["get_audio_link"] = 0
    #     empty_dict["connect_to_user"] = 0

    @staticmethod
    def get_action_dict():
        return Bot.actionDict

    @staticmethod
    def get_action(user_id):
        action_dict = Bot.get_action_dict()
        if action_dict.get(user_id, None) is None:
            action_dict[user_id] = None
        return action_dict[user_id]

    @staticmethod
    def set_action(user_id, action):
        action_dict = Bot.get_action_dict()
        action_dict[user_id] = action

    def __init__(self, myrequest):
        self.first_name = None
        self.last_name = None
        self.user_id = None
        self.__handler = dict()
        self.my_request = myrequest
        self.fill_bot_data()

    def fill_bot_data(self):
        request_json = self.my_request.get_json()['message']
        personal_data = request_json['from']
        self.first_name = personal_data['first_name']
        self.last_name = personal_data['last_name']
        self.user_id = personal_data['id']
        self.create_handler_of_bot()

    def create_handler_of_bot(self):
        self.__handler["/start"] = self.start
        self.__handler["/description"] = self.get_bot_description
        self.__handler["/menu"] = self.get_menu_of_bot
        self.__handler["/rate_book"] = self.rate_book
        self.__handler["/get_recommendation"] = self.get_recommendation
        self.__handler["/get_library"] = self.get_library
        self.__handler["/review_book"] = self.review_book
        self.__handler["/get_review"] = self.get_review
        self.__handler["/get_recommendation_by_genre"] = self.get_recommendation_by_genre
        self.__handler["/get_recommendation_by_author"] = self.get_recommendation_by_author
        self.__handler["/get_purchase_link"] = self.get_purchase_link
        self.__handler["/get_audio_link"] = self.get_audio_link
        self.__handler["/connect_to_user"] = self.connect_to_user

    def check_uncompleted_actions(self):
        pass

    def function_handler(self):
        full_request = self.my_request.get_json()["message"]["text"]
        if Bot.get_action(self.user_id) is not None:
            return Bot.get_action(self.user_id)(full_request)

        try:
            index_of_func_sepperator = full_request.index(' ')
        except:
            index_of_func_sepperator = len(full_request)
        command = full_request[:index_of_func_sepperator]
        text = full_request[index_of_func_sepperator + 1:]
        try:
            return self.__handler.get(command)(text)
        except:
            return
        pass

    def start(self, text):
        if funcs.is_user_exist(self.user_id):
            message = f"Welcome back {self.first_name} {self.last_name}"
            res = self.send_message_to_user(message)
            return
        funcs.create_user(self.user_id, self.first_name, self.last_name)
        message = f"Greetings {self.first_name} {self.last_name}. And welcome to Pablo\n" \
            f"Please enter three books, one by one, so that you liked so that Pablo can understand you taste"
        Bot.set_action(self.user_id, self.start_2_1)
        res = self.send_message_to_user(message)
        return

    def start_2_1(self, text):
        funcs.rate_book(self.user_id, text, True)
        message = f"first book received"
        Bot.set_action(self.user_id, self.start_2_2)
        res = self.send_message_to_user(message)
        return

    def start_2_2(self, text):
        funcs.rate_book(self.user_id, text, True)
        message = f"second book received"
        Bot.set_action(self.user_id, self.start_2_3)
        res = self.send_message_to_user(message)
        return

    def start_2_3(self, text):
        funcs.rate_book(self.user_id, text, True)
        message = f"third book received\n" \
            f"Your profile has been made. Feel free to enrich it by rating additional books using the command \\rate"
        #TODO check if the command still the same
        Bot.set_action(self.user_id, None)
        res = self.send_message_to_user(message)
        return


    def review_book(self, *args):
        pass



    def get_menu_of_bot(self, text):
        message = '''
        1)/start: welcomes back old users and create a new user for new users\n
        2)/description: returns a description of the bot\n
        3)/rate_book: given the name of a book and a rating, we will add that book to your profile\n
        4)/get_recommendation: Presents you with 3 books that will be tailored to your taste\n
        5)/get_library: Shows you the books you have enjoyed\n
        6)/review_book: Given the name of a book, gives you the freedom to write a review of the book, whether you liked it or not\n
        7)/get_review: Given the name of a book, returns a review of the book\n
        8)/get_recommendation_by_genre: Given the name of a book, returns 3 books from the same genre\n
        9)/get_recommendation_by_author: Given the name of a book, returns other books from the same author\n
        10)/get_purchase_link: Given the name of a book, returns an online link to purchase it\n
        11)/get_audio_link: Given the name of a book, returns a link for the audio book version of that book\n
        12)/connect_to_user: Returns the first name and last name of 3 other people who share a similar taste to you\n
        '''
        res = self.send_message_to_user(message)
        return

    def get_bot_description(self, text):
        message = '''
        This Bot is made to help Bookworms through their thrilling learning odyssey.Pablo is a personal assistant to 
        bookworms who would like to get to know new books tailored to their taste.
        '''#TODO complete the description
        res = self.send_message_to_user(message)
        return


    def rate_book(self, text):
        try:
            split_index = text.index(',')
            book_title = text[:split_index].strip()
            rating = text[split_index + 1:].strip()
            boolean_rating = True if rating == "pos" else False
            funcs.rate_book(self.user_id, book_title, boolean_rating)
            message = "Your rating has been saved"
        except :
            message = "Your operation failed. Please follow this format:\n" \
                      "/rate_book <bookname> , <pos/neg>"

        self.send_message_to_user(message)
        pass



    def get_recommendation(self, *args):
        title = funcs.get_book(self.user_id)
        message = f"I hope you enjoy reading {title}"
        self.send_message_to_user(message)
        return

    def get_library(self, *args):
        pass



    def get_review(self, *args):
        pass

    def get_recommendation_by_genre(self, *args):
        pass

    def get_recommendation_by_author(self, *args):
        pass

    def get_purchase_link(self, *args):
        pass

    def get_audio_link(self, *args):
        pass

    def connect_to_user(self, *args):
        pass

    def send_message_to_user(self, message):
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(config.TOKEN, self.user_id, message))
        return res