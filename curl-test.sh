#!/bin/bash
curl --request POST http://localhost:5000/api/timeline_post -d 'name=tester&email=tester@gmail.com&content=testing'
info=$(curl -s -X GET http://localhost:5000/api/timeline_post)
timeline_post=$(echo $info | jq '.timeline_posts')
post=$(echo $timeline_post | jq '.[0]')

name=$(echo "$post" | jq -r '.name')
email=$(echo "$post" | jq -r '.email')
content=$(echo "$post" | jq -r '.content')


if [ "$name" != "tester" ] || [ "$email" != "tester@gmail.com" ] || [ "$content" != "testing" ]; then
    echo "Error: GET or POST endpoint failed" >&2
    exit 1
else
    echo "GET and POST working correctly"
fi

id=$(echo $post | jq '.id')
curl --request DELETE http://localhost:5000/api/timeline_post/$id
