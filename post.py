from sqlalchemy import Column, String, Integer, func, exc

from base import Base, Session, external_user, external_posts

session = Session()


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    body = Column(String)

    def __init__(self):
        pass


    def create_post(self, user_id, title, body, postId=None):

        post = Post()
        if postId is None:
            post.id = self.create_new_id()
        else:
            post.id = postId

        post.user_id = user_id
        post.title = title
        post.body = body

        if external_user.exist(user_id):
            session.add(post)
            session.commit()
            return 1
        else:
            return 0

    def get_post(self, post_id):

        if self.check_numeric(post_id):

            response_db = session.query(Post).get(post_id)
            if response_db is None:
                response_api = external_posts.get_post(post_id)
                if response_api is None:
                    return None
                else:
                    self.create_post(
                        postId=response_api["id"],
                        user_id=response_api["userId"],
                        title=response_api["title"],
                        body=response_api["body"]
                    )
                    return self.serialize(response_api)
            else:
                return self.serialize(response_db)

        else:
            return "Argument error, integer data expected."


    def get_posts(self, user_id):

        if self.check_numeric(user_id):
            response_db = session.query(Post).filter(Post.user_id == user_id).all()
            print(response_db)
            if len(response_db) > 0:
                return self.serialize(response_db)
            else:
                return None
        else:
            return "Argument error, integer data expected."


    def delete_post(self, postId):
        """
        :param postId:
        :return: If post successful deleted return 1 else 0
        """
        if self.check_numeric(postId):
            if session.query(Post).filter(Post.id == postId).delete() == 0:
                return 0
            else:
                session.commit()
                return 1
        else:
            return "Argument error, integer data expected."


    def change_post(self, postId, title=None, body=None):
        status = 0
        if self.check_numeric(postId):
            if title is not None:
                status = self.change_field(postId=postId, field_name="title", field_value=title)

            if body is not None:
                status = self.change_field(postId=postId, field_name="body", field_value=body)

            session.commit()
            return status
        else:
            session.commit()
            return "Argument error, integer data expected."

    @staticmethod
    def change_field(postId, field_name, field_value):

        try:
            response_db = session.query(Post).filter(Post.id == postId).update(
                {
                    field_name: field_value
                }
            )

            if response_db <= 0:
                print(f"No change field: {field_name}")
                return None
            else:
                session.commit()
                return 1
        except:
            session.commit()
            return "Type error"


    def serialize(self, obj):
        if type(obj) == dict:
            return obj

        elif type(obj) == list:

            new_list = []
            for object in obj:
                new_list.append(self.serialize(object))
            return new_list

        elif type(obj) == Post:
            return {
                "id": obj.id,
                "user_id": obj.user_id,
                "title": obj.title,
                "body": obj.body,
            }
        else:
            return None



    def create_new_id(self):
        print(self.get_last_id(), external_posts.get_last_id())
        return max([self.get_last_id(), external_posts.get_last_id()]) + 1

    @staticmethod
    def get_last_id():
        try:
            response_db = session.query(func.max(Post.id)).first()
            if response_db[0] is None:
                return 0
            else:
                return response_db[0]
        except:
            return None

    @staticmethod
    def check_numeric(value):
        if type(value) == int:
            return True
        elif type(value) == str and value.isnumeric():
            return True
        else:
            return False


