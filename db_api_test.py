import paplo_db_api as db


def show_table(table_name):
    with db.connection.cursor() as cursor:
        query = "SELECT * FROM {}".format(table_name)
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)

if __name__ == '__main__':
    # db.create_user("ea12335", "Mohammad", "Abid")
    # show_table('users')
    # db.create_user(None, "Mohammad", "Abid")
    # db.add_book("My Book", "Action Book", "No-link", "No-link", "Actions")
    # show_table('books')
    print(db.get_all_users_id())

