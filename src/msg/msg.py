from src.db.db import DB


class MessageHelper:
    def __init__(self):
        self.messages = None
        self.update_messages()
        
    def update_messages(self):
        self.messages = DB.execute_select_query(
            'SELECT Message.id, User.id, name, timestamp, text '
            'FROM Message JOIN User ON author = User.id')

    def delete_message(self, id):
        DB.execute_dml_query(f'DELETE FROM Message WHERE id = {id}')


MH = MessageHelper()
