import peewee as pw

db = pw.SqliteDatabase('History_info.db')


class BaseModel(pw.Model):

    created_at = pw.TextField()  # Дата и время ввода команды.

    class Meta():
        database = db


class History(BaseModel):

    chat_id = pw.TextField()
    user_hotels = pw.TextField()  #  отели, которые были найдены
    user_command = pw.TextField()  # Комманда, которую вводил пользователь
