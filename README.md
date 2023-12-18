# Project README

## Developer Information

- **Name:** Mahesh Swaminathan
- **Stevens Login:** mswamina@stevens.edu

- **Name:** Sadam Mohamed Usman
- **Stevens Login:** smohamed1@stevens.edu 

- **Name:** Sathya Kalyan Paladugu
- **Stevens Login:** spaladu3@stevens.edu

## GitHub Repository

- **URL:** https://github.com/maheshs85/Web-Forum

## Project Overview

In this project we have built a web forum using Flask. It includes several features such as user creation, post creation, post deletion, post replies, date- and time-based range queries, and user-based range queries.

## Project Statistics

- **Estimated Hours Spent:** We estimate that we have spent 20 hours in the project.

## Testing Approach

I tested the code using postman and newman for the base functionality and automated testing with the pytest framework for the extensions. The test scripts cover various scenarios to ensure the functionality of each endpoint.

## Known Bugs or Issues

When submitting to gradescope, the version of node is not compatible with newman that we are using. So it fails the autograder tests but works fine in my local machine.

## Difficult Issue or Bug Example

When implementing get threads for a post extension, we were stuck in the correct approach in either iteratively or recursively  traversing through posts and which would give a better runtime performance. We chose the recursive approach as it gives a more readable code.

## Implemented Extensions

### 1. Users and user keys

#### Endpoints:

- **Create User:** `POST /user`
- **Delete post by User key:** `DELETE /post/{id}/delete/{user:key}`
- **Create post with User key:** `POST /post/{id}/`

### 2. Post Replies

#### Endpoints:

- **Create post with Reply:** `POST /post/{id}/`

### 3. Date- and Time-Based Range Queries

#### Endpoint:

- **Search Posts by Timestamp:** `GET /posts/search`

### 4. User-Based Range Queries

#### Endpoint:

- **Search Posts by User:** `GET /posts/user/{user_id}`

### 5. Thread Retrieval

#### Endpoint:

- **Retrieve Thread for Post:** `GET /posts/thread/{post_id}`

## Test Summaries

### 1. User keys Tests

function test_user_create_and_delete_post tests the user and post creation extension.

### 2. Post Replies and thread Tests

function test_get_thread_for_post tests the post replies and threads extensions. 

### 3. Search post by user Tests 
function test_search_posts_by_user tests the search posts by user extension.

### 4. Search post by timestamp
function test_search_posts_by_timestamp tests the search posts by start and end timestamp.

