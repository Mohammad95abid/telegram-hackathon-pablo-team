from flask import request
import recommendition_funcs as funcs
import config
import requests
import random
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

    action_dict = dict()
    connection_dict = dict()
    bot_dict = dict()

    @staticmethod
    def get_action_dict():
        return Bot.action_dict

    @staticmethod
    def get_action(user_id):
        action_dict = Bot.get_action_dict()
        if action_dict.get(user_id, None) is None:
            action_dict[user_id] = None
            Bot.connection_dict[user_id] = None
        try:
            return action_dict[user_id]["func"]
        except:
            return None

    @staticmethod
    def get_parameters(user_id):
        action_dict = Bot.get_action_dict()
        return action_dict[user_id]["text"]
        pass

    @staticmethod
    def set_action(user_id, action, text = None):
        action_dict = Bot.get_action_dict()
        action_dict[user_id] = dict()
        action_dict[user_id]["func"] = action
        action_dict[user_id]["text"] = text

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
        Bot.bot_dict[self.user_id] = self
        print(Bot.bot_dict[self.user_id])

    def create_handler_of_bot(self):
        self.__handler["/start"] = self.start
        self.__handler["/description"] = self.get_bot_description
        self.__handler["/get_book_information"] = self.get_book_information
        self.__handler["/review_book"] = self.review_book
        self.__handler["/menu"] = self.get_menu_of_bot
        self.__handler["/get_recommendation"] = self.get_recommendation
        self.__handler["/get_library"] = self.get_library
        self.__handler["/connect_to_user"] = self.connect_to_user
        # self.__handler["/rate_book"] = self.rate_book
        # self.__handler["/get_review"] = self.get_review
        # self.__handler["/get_recommendation_by_genre"] = self.get_recommendation_by_genre
        # self.__handler["/get_recommendation_by_author"] = self.get_recommendation_by_author
        # self.__handler["/get_purchase_link"] = self.get_purchase_link
        # self.__handler["/get_audio_link"] = self.get_audio_link

    def check_uncompleted_actions(self):
        pass

    def function_handler(self):
        full_request = self.my_request.get_json()["message"]["text"]
        if Bot.get_action(self.user_id) is not None:
            return Bot.get_action(self.user_id)(full_request)
        if Bot.connection_dict[self.user_id] is not None:
            return self.connect_to_user_recieve_late(Bot.connection_dict[self.user_id]["text"])

        try:
            index_of_func_sepperator = full_request.index(' ')
        except:
            index_of_func_sepperator = len(full_request)
        command = full_request[:index_of_func_sepperator]
        text = full_request[index_of_func_sepperator + 1:]
        try:
            return self.__handler.get(command)(text)
        except:
            return self.unknown_commands_handler()
        pass
    #todo
    def unknown_commands_handler(self):
        message = '''
        Pablo couldnt understand your command. Use /menu to see a list of all commands.
        '''
        res = self.send_message_to_user(message)
        return

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
        title = funcs.get_book_title_from(text)
        funcs.rate_book(self.user_id, title, True)
        message = f"first book received"
        Bot.set_action(self.user_id, self.start_2_2)
        res = self.send_message_to_user(message)
        return

    def start_2_2(self, text):
        title = funcs.get_book_title_from(text)
        funcs.rate_book(self.user_id, title, True)
        message = f"second book received"
        Bot.set_action(self.user_id, self.start_2_3)
        res = self.send_message_to_user(message)
        return

    def start_2_3(self, text):
        title = funcs.get_book_title_from(text)
        funcs.rate_book(self.user_id, title, True)
        message = f"third book received\n" \
            f"Your profile has been made. Feel free to enrich it by rating additional books using the command: /review_book"
        #TODO check if the command still the same
        Bot.set_action(self.user_id, None)
        res = self.send_message_to_user(message)
        self.check_if_exist_connection()
        return

    def review_book(self, text):
        message = '''
        Reviewing books updates your profile by learning which books you like and dislike.\n
        Please enter the name of the book you'd like to rate
        '''
        Bot.set_action(self.user_id, self.review_book_1)
        res = self.send_message_to_user(message)
        return

    def review_book_1(self, text):
        title = funcs.get_book_title_from(text)
        message ='''
        Please rate the book by inserting:\n y for a positive rating \n n for a negative rating
        '''
        Bot.set_action(self.user_id, self.review_book_2, title)
        res = self.send_message_to_user(message)
        return

    def review_book_2(self, text):
        if text != 'y' and text !='n':
            message = '''
            Input invalid. Please rate the book by inserting:\n y for a positive rating \n n for a negative rating'''
            res = self.send_message_to_user(message)
            return
        rating = True if text == 'y' else False
        title = Bot.get_parameters(self.user_id)
        funcs.rate_book(self.user_id, title, rating)
        Bot.set_action(self.user_id, self.review_book_3, title)
        message = '''
        Your rating has been saved. Would you like to write a review?\n
        Please insert:\n y to write a review. \n n to end the process of rating the book.
        '''
        res = self.send_message_to_user(message)
        return

    def review_book_3(self, text):
        if text != 'y' and text !='n':
            message = '''
            Input invalid. Please pick whether you'd like to review the book by inserting:\n
             y to write a review. \n n to end the process of rating the book.'''
            res = self.send_message_to_user(message)
            return
        if text == 'n':
            message = 'Book has been rated'
            Bot.set_action(self.user_id, None)
            res = self.send_message_to_user(message)
            self.check_if_exist_connection()
            return
        title = Bot.get_parameters(self.user_id)
        Bot.set_action(self.user_id, self.review_book_4, title)
        message = 'Please write down you review'
        res = self.send_message_to_user(message)
        return

    def review_book_4(self, text):
        title = Bot.get_parameters(self.user_id)
        print(title)
        funcs.review_book(self.user_id, title, text)
        message = 'Your review has been added'
        Bot.set_action(self.user_id, None)
        res = self.send_message_to_user(message)
        self.check_if_exist_connection()
        pass

    def get_book_information(self, text):
        message = '''
                Please enter the title of the book about which you want Pablo to give you information
                '''
        Bot.set_action(self.user_id, self.get_book_information_1)
        res = self.send_message_to_user(message)
        return

    def get_book_information_1(self, text):
        message = '''
        Please pick which command you want by inserting:\n
        1 To read description of book\n
        2 To get review of book\n
        3 to get links to purchase\n
        4 to get author of the book\n
        5 to exit this command\n
        '''
        title = funcs.get_book_title_from(text)
        Bot.set_action(self.user_id, self.get_book_information_handler, title)
        res = self.send_message_to_user(message)
        return

    def get_book_information_handler(self, text):
        title = Bot.get_parameters(self.user_id)
        if text == '1':
            return self.get_book_information_description(title)
        if text == '2':
            return self.get_book_information_review(title)
        if text == '3':
            return self.get_book_information_purchase_link(title)
        if text == '4':
            return self.get_book_information_author(title)
        if text == '5':
            return self.get_book_information_exit(title)
        message = '''
        I didnt understand that command.\n please try again using one of the following commands:\n
        1 To read description of book\n
        2 To get review of book\n
        3 to get links to purchase\n
        4 to get author of the book\n
        5 to exit this command\n
        '''
        res = self.send_message_to_user(message)
        return

    def get_book_information_description(self, title):
        description = funcs.get_description(title)
        message = description +'\n\n\n'
        res = self.send_message_to_user(message)
        self.get_book_information_1(title)
        # Bot.set_action(self.user_id, self.get_book_information_1, title)
        pass
    #TODO finish this func
    def get_book_information_review(self, title):
        message = '''
        Choose which kind of review you want by pressing:\n
        1 To choose a general review\n
        2 To choose a positive review\n
        3 To choose a negative review\n
        '''
        res = self.send_message_to_user(message)
        Bot.set_action(self.user_id, self.get_book_information_review_handler, title)
        pass

    def get_book_information_review_handler(self, text):
        title = Bot.get_parameters(self.user_id)
        if text == '1':
            return self.get_book_information_review_rand(title)
        if text == '2':
            return self.get_book_information_review_pos(title)
        if text == '3':
            return self.get_book_information_review_neg(title)
        message = '''
                I didnt understand that command.\n please try again using one of the following commands:\n
                1 To choose a general review\n
                2 To choose a positive review\n
                3 To choose a negative review\n
                '''
        res = self.send_message_to_user(message)
        return

    def get_book_information_review_pos(self, title):
        message = "here are your reviews:\n"
        review_list = [elem['review'] for elem in funcs.get_review_from_db(True) if elem['book_title'] == title]
        review_list = list(set(review_list))
        sampling = random.choices(review_list, k=min(len(review_list), 3))
        sampling = [elem for elem in sampling if elem is not None]
        if not sampling:
            message = "There are no positive reviews for this book"
        else:
            for i in range(1, 1 + min(len(sampling), 3)):
                message += f"{i}) {sampling[i - 1]}\n"
        res = self.send_message_to_user(message)
        return self.get_book_information_1(title)

    def get_book_information_review_neg(self, title):
        message = "here are your reviews:\n"
        review_list = [elem['review'] for elem in funcs.get_review_from_db(False) if elem['book_title'] == title]
        review_list = list(set(review_list))
        sampling = random.choices(review_list, k=min(len(review_list), 3))
        sampling = [elem for elem in sampling if elem is not None]
        if not sampling:
            message = "There are no negative reviews for this book"
        else:
            for i in range(1, 1 + min(len(sampling), 3)):
                message += f"{i}) {sampling[i - 1]}\n"
        res = self.send_message_to_user(message)
        return self.get_book_information_1(title)

    def get_book_information_review_rand(self, title):
        message = "here are your reviews:\n"
        review_list = [elem['review'] for elem in funcs.get_review_from_db() if elem['book_title'] == title]
        review_list = list(set(review_list))
        sampling = random.choices(review_list, k=min(len(review_list), 3))
        sampling = [elem for elem in sampling if elem is not None]
        if not sampling:
            message = "There are no reviews for this book"
        else:
            for i in range(1, 1 + min(len(sampling), 3)):
                message += f"{i}) {sampling[i - 1]}\n"
        res = self.send_message_to_user(message)
        return self.get_book_information_1(title)

    def get_book_information_purchase_link(self, title):
        link = funcs.get_buy_link(title)
        if link is not None:
            message = "You can buy:\n" + title + "\nby using this link:\n" + link
            # message = f"You can use this link:\n{link}\nto buy:\n{title}\n\n"
        else:
            message = f"We couldnt find a purchase link for {title}"

        message = message.replace('#', '')
        print(message)
        res = self.send_message_to_user(message)
        self.get_book_information_1(title)
        pass
    #TODO finish this func by fixing bug
    def get_book_information_author(self, title):
        authors = funcs.get_book_author(title)
        s = '' if len(authors) == 1 else 's'
        is_are = 'is' if len(authors) == 1 else 'are'
        message = f'The author{s} of this book {is_are}:\n'
        for author in authors:
            message += author
            message += '\n'
        res = self.send_message_to_user(message)
        self.get_book_information_1(title)
        pass

    def get_book_information_exit(self, title):
        message = 'command exited successfully'
        Bot.set_action(self.user_id, None)
        res = self.send_message_to_user(message)
        self.check_if_exist_connection()
        pass


    def get_recommendation(self, *args):
        message = '''
                Pablo can recommend you books based on you profile or based on a specific book.\n
                So that Pablo can recommend you the book you want. Please insert\n:
                1 To get a recommendation based on your profile\n
                2 To get a recommendation similar to a specific book\n
                3 To get a recommendation based on the author of a specific book\n
                '''
        Bot.set_action(self.user_id, self.get_recommendation_1)
        res = self.send_message_to_user(message)
        return

    def get_recommendation_1(self, text):
        if text == '1':
            return self.get_recommendation_personal(text)
            pass
        if text == '2':
            return self.get_recommendation_similar_to_book(text)
            pass
        if text == '3':
            return self.get_recommendation_similar_to_author(text)
            pass
        message = '''
        I didnt understand that command.\n please try again using one of the following commands:\n
        1 To get a recommendation based on your profile\n
        2 To get a recommendation similar to a specific book\n
        3 To get a recommendation based on the author of a specific book\n
        '''
        res = self.send_message_to_user(message)
        return

    def get_recommendation_personal(self, text):
        title = funcs.get_recomndition_book(self.user_id)
        message = f"We hope you will enjoy reading\n{title}"
        res = self.send_message_to_user(message)
        Bot.set_action(self.user_id, None)
        self.check_if_exist_connection()

    def get_recommendation_similar_to_book(self, text):
        message = "Please enter the name of the book"
        res = self.send_message_to_user(message)
        Bot.set_action(self.user_id, self.get_recommendation_similar_to_book1)
        pass

    def get_recommendation_similar_to_author(self, text):
        message = "Please enter the name of the book"
        res = self.send_message_to_user(message)
        Bot.set_action(self.user_id, self.get_recommendation_similar_to_author1)
        pass

    #TODO finish this func
    def get_recommendation_similar_to_book1(self, text):
        title = funcs.get_book_title_from(text)
        message = 'this feature is still to be implemented'
        res = self.send_message_to_user(message)
        Bot.set_action(self.user_id, None)
        self.check_if_exist_connection()
        pass
    #TODO finish this func
    def get_recommendation_similar_to_author1(self, text):
        title = funcs.get_book_title_from(text)
        message = 'this feature is still to be implemented'
        res = self.send_message_to_user(message)
        Bot.set_action(self.user_id, None)
        self.check_if_exist_connection()
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

    def connect_to_user(self, text):
        message = '''
        Pablo connects you with the users who have similar literary taste as you, provided that they accept your 
        invitation. Please enter the amount of people you would like to connect to
        '''
        res = self.send_message_to_user(message)
        Bot.set_action(self.user_id, self.connect_to_user1)
        pass

    def connect_to_user1(self, text):
        try:
            num_of_people = int(text)
        except:
            message = "Invalid input. Please enter a number resembling the amount of people you would like to connect to"
            res = self.send_message_to_user(message)
            return
        all_user_ids = [1442293094]

        #TODO receive a function which returns the top user ids and put it in all_user_ids
        print(Bot.action_dict)
        for user_id in all_user_ids:
            other_bot = Bot.bot_dict.get(user_id)
            if other_bot is None:
                return
            if Bot.get_action(user_id) is None:
            # if Bot.action_dict[user_id] is None:
                message = '''
                A user with similar literary taste to yours would like to connect with you\n
                Please insert:\ny to agree to connect\nn to deny the request
                '''
                Bot.set_action(user_id, other_bot.connect_to_user_recieve, self.user_id)
                res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                   .format(config.TOKEN, user_id, message))

            else:
                Bot.connection_dict[user_id] = {"func" : other_bot.connect_to_user_recieve_late, "text" : self.user_id}
        message = '''
        Your connection request has been sent to the most suitable users. In case they would agree to 
        connect with you, you would receive their username and password
        '''
        res = self.send_message_to_user(message)



    def connect_to_user_recieve(self, text):
        user_id = Bot.get_parameters(self.user_id)
        Bot.connection_dict[self.user_id] = None
        if text == 'y':
            message = f"User {self.first_name} {self.last_name} agreed to connect with you!"
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                               .format(config.TOKEN, user_id, message))
            message = "You have accepted the request!"
            self.send_message_to_user(message)
            Bot.set_action(self.user_id, None)
            return
        if text == 'n':
            message = "You have denied the request!"
            self.send_message_to_user(message)
            Bot.set_action(self.user_id, None)
            return
        message = "Pablo couldn't understand your command. Please insert:\ny to agree to connect\nn to deny the request"
        self.send_message_to_user(message)
        pass

    def connect_to_user_recieve_late(self, user_id):
        message = '''A user with similar literary taste to yours would like to connect with you\n
                Please insert:\ny to agree to connect\nn to deny the request'''
        Bot.set_action(self.user_id, self.connect_to_user_recieve, user_id)
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(config.TOKEN, self.user_id, message))
        Bot.connection_dict[self.user_id] = None
        #TODO check the option to make connection dict a list instead of a single value incase many people connecting
        pass

    def send_message_to_user(self, message):
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(config.TOKEN, self.user_id, message))
        return res

    def check_if_exist_connection(self):
        if Bot.connection_dict[self.user_id] is not None:
            return self.connect_to_user_recieve_late(Bot.connection_dict[self.user_id]["text"])
