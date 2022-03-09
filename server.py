import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from post import Post




app = Flask(__name__)
CORS(app)
logging.getLogger('flask_cors').level = logging.DEBUG

post = Post()


@app.route('/add_post', methods=['POST'])
def add_post():
    try:
        user_id = request.args.get("user_id")
        title = request.get_json()["title"]
        body = request.get_json()["body"]
        if post.create_post(
                user_id=user_id,
                title=title,
                body=body
        ) == 1:
            return "Post added successfully"
        else:
            return f"Post not added user |>{user_id}<| not exist"

    except:
        return "Error: Possible error in the request body"


@app.route('/change_post', methods=['PUT'])
def change_post():
    try:
        post_id = request.args.get("post_id")
        title = request.get_json()["title"]
        body = request.get_json()["body"]
        if post_id != None:
            if post.change_post(
                    postId=post_id,
                    title=title,
                    body=body
            ) == 1:
                return "Post change successfully "
            else:
                return f"Post {post_id} not change. It probably doesn't exist in the database."
        else:
            return "Not exist argument |>post_id<|"
    except:
        return "Error: Possible error in the request body"


@app.route('/get_post', methods=['GET'])
def get_post():
    try:
        post_id = request.args.get("post_id")
        if post_id != None:
            return jsonify(post.get_post(post_id))
        else:
            return "Not exist argument |>post_id<|"
    except:
        return "Error"


@app.route('/get_posts', methods=['GET'])
def get_posts():
    # try:
    user_id = request.args.get("user_id")
    if user_id != None:
        return jsonify(post.get_posts(user_id))
    else:
        return "Not exist argument |>user_id<|"
    pass
    # except:
    #     return "Error"


@app.route('/delete_post', methods=['DELETE'])
def delete_post():
    try:
        post_id = request.args.get("post_id")
        if post_id != None:
            return jsonify(post.delete_post(post_id))
        else:
            return "Not exist argument |>post_Id<|"
    except:
        return "Error"


if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=5000
    )



