from flask import Flask, request, jsonify
import secrets
import datetime
from threading import Lock

app = Flask(__name__)
lock = Lock()
posts = {}  # Global state to store posts
post_id_counter = 1

# Endpoint #1: Create a post
@app.route('/post', methods=['POST'])
def create_post():
    with lock:
        try:
            data = request.get_json()
            if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str):
                return jsonify({'err': 'Bad request'}), 400

            post_id = generate_unique_id()
            key = generate_random_key()
            timestamp = get_current_timestamp()

            post = {'id': post_id, 'key': key, 'timestamp': timestamp, 'msg': data['msg']}
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
        return jsonify({'id': post['id'], 'timestamp': post['timestamp'], 'msg': post['msg']})

# Endpoint #3: Delete a post
@app.route('/post/<int:post_id>/delete/<string:key>', methods=['DELETE'])
def delete_post(post_id, key):
    with lock:
        if post_id not in posts:
            return jsonify({'err': 'Not found'}), 404

        post = posts[post_id]
        if post['key'] != key:
            return jsonify({'err': 'Forbidden'}), 403

        del posts[post_id]
        return jsonify({'id': post['id'], 'key': post['key'], 'timestamp': post['timestamp']})

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
    app.run(debug=True)
