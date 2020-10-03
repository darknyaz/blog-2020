from src.db.db import DB


class MessageHelper:
    def __init__(self):
        self.messages = DB.execute_select_query(
            'SELECT Message.id, User.id, name, timestamp, text '
            'FROM Message JOIN User ON author = User.id')


MH = MessageHelper()
