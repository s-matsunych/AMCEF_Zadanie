import requests

ERROR_MSG = "Error EPosts"

class EPosts:
    link = 'https://jsonplaceholder.typicode.com/posts/'

    def get_post(self, post_id):
        try:
            response = requests.get(url=f"{self.link}{post_id}").json()

            if (len(response) > 0) and (response["id"] == int(post_id)):
                return response
            else:
                return None

        except:
            return ERROR_MSG


    def get_posts(self, user_id):
        try:
            response = requests.get(
                url=self.link,
                params={
                    "userId": user_id
                }
            ).json()

            if len(response) > 0:
                return response
            else:
                return None
        except:
            return ERROR_MSG


    def get_last_id(self):
        try:
            response = requests.get(
                url=self.link
            ).json()
            return response[-1]['id']
        except:
            return ERROR_MSG


class EUsers:
    link = 'https://jsonplaceholder.typicode.com/users/'

    def exist(self, user_id):
        try:
            response = requests.get(url=f"{self.link}{user_id}").json()
            if (len(response) > 0) and (response["id"] == int(user_id)):
                return True
            else:
                return False
        except:
            return "Error EUsers"
