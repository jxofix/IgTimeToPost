import sqlite3


class MediaDB:
    """
    Class representing SQlite database containing all media data for required instagram users
    """

    def __init__(self, db_name='InstaMedia'):
        self.db_name = db_name
        self.db = sqlite3.connect(self.db_name)

    def create_table(self, table_name):
        """
        Creating structure of SQlite DB
        :param table_name: name of SQLite table
        """
        self.db.execute("""
                        CREATE TABLE {table_name}  (
                            user_id TEXT NOT NULL,
                            username TEXT,
                            followers_count INTEGER,
                            media_id TEXT,
                            media_type TEXT,
                            media_product TEXT,
                            comments_count INTEGER,
                            likes_count INTEGER,
                            time_posted TEXT,
                            permalink TEXT,
                            duration LONG
                        );                       
        """.format(table_name=table_name))

    def insert_media(self, table_name, data):
        """
        Function inserting data about media into SQlite DB
        :param table_name: name of the table we want to insert data to
        :param data: list of media we want to insert
        """
        sql = 'INSERT INTO {table_name} (user_id, ' \
              'username, ' \
              'followers_count, ' \
              'media_id, ' \
              'media_type, ' \
              'media_product, ' \
              'comments_count, ' \
              'likes_count, ' \
              'time_posted,' \
              'permalink,' \
              'duration' \
              ') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(table_name=table_name)
        with self.db:
            self.db.executemany(sql, data)

