#!usr/bin/sh

python3.13 compile-post-pipeline/make-posts-json.py

if [ $? -ne 0 ]; then
    echo "Failed to make posts.json"
    exit 1
fi

python3.13 compile-post-pipeline/compile-posts.py

if [ $? -ne 0 ]; then
    echo "Failed to compile posts"
    exit 1
fi

exit 0
