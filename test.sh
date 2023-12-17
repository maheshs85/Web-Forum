#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

./run.sh &
PID=$! # record the PID

newman run tests/forum_multiple_posts.postman_collection.json -e tests/env.json # use the env file
newman run tests/forum_post_read_delete.postman_collection.json -n 50 # 50 iterations