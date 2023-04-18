import utils.api_key as api_key
import requests
import utils.instagrampy


class InstagramApi:
    """
    A class to represent all media from desired instagram user via instagram grapi API
    """

    namespace = 'time_to_post'
    api_entry = 'API'
    ig_entry = 'IG_ID'
    user_id = api_key.get_entry(entry=ig_entry, namespace=namespace)
    access_token = api_key.get_entry(entry=api_entry, namespace=namespace)
    graphi_url = f'https://graph.facebook.com/v15.0/{user_id}'

    def get_users_media(self, username: str):
        """
        Function to extract data about all users public posts (media) on his/her instagram profile

        :param username: instagram username whose media we want to get data about
        :return: list of posts (media)
        """
        media = []
        fields_user = f'business_discovery.username({username})'
        fields_data = '''{followers_count,media.limit(100){
                                    media_type, 
                                    media_product_type, 
                                    timestamp, 
                                    comments_count, 
                                    like_count, 
                                    permalink
                                    }}'''
        fields = fields_user + fields_data

        media_res = self.instagram_grapi_call(fields=fields)

        # parse response
        media = media + self.parse_media_response(media_res.json(), username)

        after_token = self.get_after_token(media_res.json())
        # parse response to get after
        while after_token:
            fields_data = '''{followers_count,media.after(''' + after_token + ''').limit(100){
                                                media_type, 
                                                media_product_type, 
                                                timestamp, 
                                                comments_count, 
                                                like_count, 
                                                permalink
                                                }}'''

            fields = fields_user + fields_data
            media_res = self.instagram_grapi_call(fields=fields)
            # parse response
            media = media + self.parse_media_response(media_res.json(), username)

            after_token = self.get_after_token(media_res.json())

        return media

    def instagram_grapi_call(self, fields):
        """
        Request IG grapi API
        :param fields: required field about users posts
        :return: grapi response
        """
        parameters = {
            'access_token': self.access_token,
            'fields': fields
        }
        res = requests.get(url=self.graphi_url, params=parameters)

        return res

    @staticmethod
    def get_after_token(res_json):
        """
        Function to parse after token from IG API response
        :param res_json: API response
        :return: after token
        """
        if 'paging' in res_json['business_discovery']['media']:
            if 'after' in res_json['business_discovery']['media']['paging']['cursors']:
                after = res_json['business_discovery']['media']['paging']['cursors']['after']
            else:
                after = None
        else:
            after = None

        return after

    @staticmethod
    def parse_media_response(response, username):
        """
        Parse API response to desired format for SQlite DB
        :param response: API response
        :param username: IG username who posted the posts in response
        :return: list of media
        """
        media = []
        for medium in response['business_discovery']['media']['data']:
            likes_count = 0
            if 'like_count' in medium:
                likes_count = medium['like_count']

            reel_length = 0
            # if medium['media_product_type'] == 'REELS':
            #     reel_length = instagrampy.get_reel_lenght(medium['permalink'])

            medium_tuple = (response['business_discovery']['id'],
                            username,
                            response['business_discovery']['followers_count'],
                            medium['id'],
                            medium['media_type'],
                            medium['media_product_type'],
                            medium['comments_count'],
                            likes_count,
                            medium['timestamp'],
                            medium['permalink'],
                            reel_length)
            media.append(medium_tuple)
        return media

