from flask import Flask, request, jsonify
import secrets
import datetime
from threading import Lock

app = Flask(__name__)
lock = Lock()
users = {}
posts = {}
replies = {}
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

            if 'reply_to' in data:
                reply_to = data.get('reply_to')
            else:
                reply_to = None

            if reply_to:
                if reply_to not in replies:
                    replies[reply_to] = []
                replies[reply_to].append(post_id)

            post = {'id': post_id, 'key': key, 'user_id': user_id, 'timestamp': timestamp, 'msg': data['msg'], 'reply_to': reply_to}
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

        reply_to = post.get('reply_to')
        replies_list = replies.get(post_id, [])
        
        user_id = None
        if 'user_id' in post:
            user_id = post['user_id']
        return jsonify({'id': post['id'], 'user_id': user_id, 'timestamp': post['timestamp'], 'msg': post['msg'], 'reply_to': reply_to, 'replies': replies_list})

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

@app.route('/posts/search', methods=['GET'])
def search_posts_by_timestamp():
    with lock:
        try:
            start_timestamp_str = request.args.get('start_timestamp')
            end_timestamp_str = request.args.get('end_timestamp')

            if not start_timestamp_str and not end_timestamp_str:
                return jsonify({'err': 'Provide at least one of start_timestamp or end_timestamp'}), 400

            start_timestamp = datetime.datetime.fromisoformat(start_timestamp_str) if start_timestamp_str else None
            end_timestamp = datetime.datetime.fromisoformat(end_timestamp_str) if end_timestamp_str else None

            matching_posts = []
            for post_id, post in posts.items():
                post_timestamp = datetime.datetime.fromisoformat(post['timestamp'])
                if (not start_timestamp or start_timestamp <= post_timestamp) and \
                        (not end_timestamp or post_timestamp <= end_timestamp):
                    matching_posts.append({
                        'id': post['id'],
                        'timestamp': post['timestamp'],
                        'msg': post['msg'],
                        'reply_to': post.get('reply_to'),
                        'replies': replies.get(post['id'], [])
                    })

            return jsonify(matching_posts)
        except ValueError:
            return jsonify({'err': 'Invalid timestamp format'}), 400
        
@app.route('/user', methods=['POST'])
def create_user():
    with lock:
        user_id = generate_unique_id()
        user_key = generate_random_key()
        users[user_id] = {'id': user_id, 'key': user_key}
        return jsonify(users[user_id])

@app.route('/posts/user/<int:user_id>', methods=['GET'])
def search_posts_by_user(user_id):
    with lock:
        if user_id not in users:
            return jsonify({'err': 'User not found'}), 404

        user_posts = []
        for post_id, post in posts.items():
            if post['user_id'] == user_id:
                user_posts.append({
                    'id': post['id'],
                    'timestamp': post['timestamp'],
                    'msg': post['msg'],
                    'reply_to': post.get('reply_to'),
                    'replies': replies.get(post['id'], [])
                })

        return jsonify(user_posts)

@app.route('/posts/thread/<int:post_id>', methods=['GET'])
def get_thread_for_post(post_id):
    with lock:
        if post_id not in posts:
            return jsonify({'err': 'Post not found'}), 404

        thread_posts = []

        def traverse_thread(current_post_id):
            # Add the current post to the thread
            current_post = posts[current_post_id]
            thread_posts.append({
                'id': current_post['id'],
                'timestamp': current_post['timestamp'],
                'msg': current_post['msg'],
                'reply_to': current_post.get('reply_to'),
                'replies': replies.get(current_post['id'], [])
            })

            # Recursively traverse replies
            for reply_id in replies.get(current_post_id, []):
                traverse_thread(reply_id)

        traverse_thread(post_id)
        return jsonify(thread_posts)
    
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
