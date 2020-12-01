import pymysql

API_KEYS = {
    "key": "q5QJR1BpwdBHs7SLjH0mw",
    "secret": "AVn3klr2VsZk5l8e4ia9hf55lTez5BSIankd7G9a94"
}

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="paplo",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)