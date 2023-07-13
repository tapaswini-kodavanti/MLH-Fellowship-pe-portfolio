#!/bin/bash

# Base URL of the API
base_url="http://localhost:5000"

# Function to generate a random string
generate_random_string() {
    local random_string=$(cat /dev/urandom | tr -dc 'a-zA-Z' | fold -w 10 | head -n 1)
    echo "$random_string"
}

# Test POST endpoint
test_post_endpoint() {
    local url="$base_url/api/timeline_post"

    # Generate random data
    local name=$(generate_random_string)
    local email="${name}@example.com"
    local content=$(generate_random_string)

    # Make the POST request
    local response=$(curl --request POST "$url" -d "name=$name&email=$email&content=$content")

    echo "POST Response:"
    echo "$response"
}

# Test GET endpoint
test_get_endpoint() {
    local url="$base_url/api/timeline_post"

    # Make the GET request
    local response=$(curl "$url")

    echo "GET Response:"
    echo "$response"
}

# Test DELETE endpoint
test_delete_endpoint() {
    local url="$base_url/api/timeline_post"

    # Make the DELETE request
    local response=$(curl -s -X DELETE "$url")

    echo "DELETE Response:"
    echo "$response"
}

# Call the functions to test the endpoints
test_post_endpoint
echo "---------------------------"
test_get_endpoint
echo "---------------------------"
test_delete_endpoint
