import requests
import json

# Replace with the actual URL of your Flask application
BASE_URL = "http://localhost:8000"

def create_user():
    response = requests.post(f"{BASE_URL}/user")
    if response.status_code == 200:
        user_data = json.loads(response.text)
        return user_data
    else:
        print(f"Error creating user: {response.text}")
        return None

def create_post(msg, user_id, user_key, reply_to=None):
    data = {
        "msg": msg,
        "user_id": user_id,
        "user_key": user_key,
        "reply_to": reply_to
    }

    response = requests.post(f"{BASE_URL}/post", json=data)
    if response.status_code == 200:
        post_data = json.loads(response.text)
        return post_data
    else:
        print(f"Error creating post: {response.text}")
        return None

if __name__ == "__main__":
    # Create a user
    user_data = create_user()
    if user_data:
        user_id = user_data["id"]
        user_key = user_data["key"]

        # Create posts
        post1 = create_post("Hello World!", user_id, user_key)
        post2 = create_post("How are you?", user_id, user_key, reply_to=post1["id"])
        post3 = create_post("I'm doing well, thanks!", user_id, user_key, reply_to=post2["id"])

        # Display created posts
        print("User ID:", user_id)
        print("User Key:", user_key)
        print("Post 1:", post1)
        print("Post 2:", post2)
        print("Post 3:", post3)
        
        user2_data = create_user()
        if user2_data:
            user2_id = user2_data["id"]
            user2_key = user2_data["key"]

            # Create a post for the second user replying to the first user's post
            post4 = create_post("Test Post 4 by User 2 (Reply to User 1)", user2_id, user2_key, reply_to=post1["id"])

            # Display created posts for the second user
            print("\nUser 2 ID:", user2_id)
            print("User 2 Key:", user2_key)
            print("Test Post 4 by User 2 (Reply to User 1):", post4)
