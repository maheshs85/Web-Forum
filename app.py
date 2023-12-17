from flask import Flask, request, jsonify
import secrets
import datetime
from threading import Lock

app = Flask(__name__)
lock = Lock()
users = {}
posts = {}
post_id_counter = 1
    
# Endpoint #1: Create a post
@app.route('/post', methods=['POST'])
def create_post():
    with lock:
        try:
            data = request.get_json()
            if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str):
                return jsonify({'err': 'Bad request'}), 400

            user_id = None
            if 'user_id' in data and 'user_key' in data:
                user_id = data['user_id']
                user_key = data['user_key']

                if user_id not in users or users[user_id]['key'] != user_key:
                    return jsonify({'err': 'Unauthorized'}), 401
            
            post_id = generate_unique_id()
            key = generate_random_key()
            timestamp = get_current_timestamp()

            post = {'id': post_id, 'key': key, 'user_id': user_id, 'timestamp': timestamp, 'msg': data['msg']}
            posts[post_id] = post

            return jsonify(post)
        except Exception as e:
            return jsonify({'err': str(e)}), 500

# Endpoint #2: Read a post
@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    with lock:
        if post_id not in posts:
            return jsonify({'err': 'Not found'}), 404

        post = posts[post_id]

        user_id = None
        if 'user_id' in post:
            user_id = post['user_id']
        return jsonify({'id': post['id'], 'user_id': user_id, 'timestamp': post['timestamp'], 'msg': post['msg']})

# Endpoint #3: Delete a post
@app.route('/post/<int:post_id>/delete/<string:key>', methods=['DELETE'])
def delete_post(post_id, key):
    with lock:
        if post_id not in posts:
            return jsonify({'err': 'Not found'}), 404

        post = posts[post_id]
        posts_key = post['key']

        user_id = post['user_id']
        if user_id != None:
            user = users[user_id]
            user_key = user['key']
        else:
            user_key = None
            
        if posts_key != key and user_key != key:
            return jsonify({'err': 'Forbidden'}), 403

        del posts[post_id]
        return jsonify({'id': post_id, 'user_id': user_id, 'timestamp': post['timestamp']})

@app.route('/user', methods=['POST'])
def create_user():
    with lock:
        user_id = generate_unique_id()
        user_key = generate_random_key()
        users[user_id] = {'id': user_id, 'key': user_key}
        return jsonify(users[user_id])
    
def generate_unique_id():
    global post_id_counter
    post_id = post_id_counter
    post_id_counter += 1
    return post_id

def generate_random_key():
    return secrets.token_urlsafe(32)

def get_current_timestamp():
    return datetime.datetime.utcnow().isoformat()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
