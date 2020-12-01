from flask import request

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
    @staticmethod
    def fill_empty_action_dict(empty_dict):
        empty_dict["start"] = 0
        empty_dict["rate_book"] = 0
        empty_dict["get_recommendation"] = 0
        empty_dict["get_library"] = 0
        empty_dict["review_book"] = 0
        empty_dict["get_review"] = 0
        empty_dict["get_recommendation_by_genre"] = 0
        empty_dict["get_recommendation_by_author"] = 0
        empty_dict["get_purchase_link"] = 0
        empty_dict["get_audio_link"] = 0
        empty_dict["connect_to_user"] = 0

    @staticmethod
    def get_action_dict(user_id):
        if Bot.actionDict.get(user_id, None) is None:
            Bot.actionDict[user_id] = dict()
            Bot.fill_empty_action_dict(Bot.actionDict[user_id])
        return Bot.actionDict

    def __init__(self, myrequest):
        self.first_name = None
        self.last_name = None
        self.user_id = None
        self.handler = dict()
        self.fill_bot_data(myrequest)

    def fill_bot_data(self, my_request:request):
        request_json = my_request.get_json()['message']
        personal_data = request_json['from']
        self.first_name = personal_data['first_name']
        self.last_name = personal_data['last_name']
        self.user_id = personal_data['id']

    def create_handler_of_bot(self):
        self.handler["/start"] = self.start
        self.handler["/description"] = self.get_description_of_bot
        self.handler["/rate_book"] = self.rate_book
        self.handler["/get_recommendation"] = self.get_recommendation
        self.handler["/get_library"] = self.get_library
        self.handler["/review_book"] = self.review_book
        self.handler["/get_review"] = self.get_review
        self.handler["/get_recommendation_by_genre"] = self.get_recommendation_by_genre
        self.handler["/get_recommendation_by_author"] = self.get_recommendation_by_author
        self.handler["/get_purchase_link"] = self.get_purchase_link
        self.handler["/get_audio_link"] = self.get_audio_link
        self.handler["/connect_to_user"] = self.connect_to_user

    def check_uncompleted_actions(self):
        pass

    def function_handler(self, message, *args):
        pass

    def start(self, *args):
        pass

    def get_description_of_bot(self, *args):
        pass

    def rate_book(self, *args):
        pass

    def get_recommendation(self, *args):
        pass

    def get_library(self, *args):
        pass

    def review_book(self, *args):
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

