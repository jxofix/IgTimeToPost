from utils import api_IG
from utils import sqlite_db


def get_and_safe_all_media(username):
    """
    Function to store post data to sqlite database

    :param username: instagram username which post will be saved
    """
    ig_api = api_IG.InstagramApi()
    media = ig_api.get_users_media(username)

    db = sqlite_db.MediaDB()
    db.insert_media('media', media)


if __name__ == '__main__':
    get_and_safe_all_media('travelingwithstephy')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
