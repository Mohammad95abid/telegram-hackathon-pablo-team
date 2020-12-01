import paplo_db_api as db



if __name__ == '__main__':
    # create users raws
    print(db.create_user("ea12335", "Mohammad", "Abid"))
    print(db.create_user("esv12335", "Mohammad", "Abo Ali"))
    print(db.create_user("eut12335", "Qasim", "Habib"))
    print(db.create_user("15egT4", "Hanin", "Saeed"))
    # create books raws
    print(db.add_book("My Book", "Action Book", "No-link", "No-link", "Actions"))
    # create reviews raws
    print(db.update_review("My Book", "esv12335", False))
    print(print(db.update_review("My Book","15egT4", True, "Wow!")))
    print(db.update_review("My Book", "eut12335", True))
    #   to update a review description of exist review
    # print(db.update_review("My Book", "esv12335", None, "Wow!1222"))