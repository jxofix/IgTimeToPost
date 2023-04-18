from instagrapi import Client

def get_reel_lenght(reel_url):
    """
    Function to get specific REEL video duration using unofficial library instagrapi (based on web scrapping)
    :param reel_url: url to the specific REEL video
    :return: duration of the REEL video
    """
    cl = Client()
    media_pk = cl.media_pk_from_url(reel_url)
    media_info = cl.media_info_gql(media_pk=media_pk)

    return media_info.dict()['video_duration']
