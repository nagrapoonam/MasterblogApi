# using Flask to handle HTTP requests, create JSON responses, and access data from incoming requests.
from flask import Flask, jsonify, request
# allowing cross-origin requests from any domain to access API endpoints.
from flask_cors import CORS

app = Flask(__name__)  # Initializing a Flask application instance
CORS(app)  # This will enable CORS for all routes

# a list of dictionaries representing blog posts
POSTS = [
    {"id": 1, "title": "7First post", "content": "1This is the first post."},
    {"id": 2, "title": "6Second post", "content": "2This is the second post."},
    {"id": 3, "title": "5Third post", "content": "3This is the third post."},
    {"id": 4, "title": "4First post", "content": "4This is the tenth post."},
    {"id": 5, "title": "3Fifth post", "content": "5This is the fifth post."},
    {"id": 6, "title": "2Sixth post", "content": "6This is the sixth post."},
    {"id": 7, "title": "1First post", "content": "7This is the aseventh post."},

]


# handles GET requests to the /api/posts endpoint for retrieving a list of blog posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Get the sort and direction query parameters
    sort_field = request.args.get('sort')
    direction = request.args.get('direction')

    # Check if sort_field and direction are provided
    if sort_field and direction:
        # Check if sort_field is valid
        if sort_field not in ['title', 'content']:
            response = {
                'error': 'Invalid sort field.',
                'valid_fields': ['title', 'content']
            }
            return jsonify(response), 400

        # Check if direction is valid
        if direction not in ['asc', 'desc']:
            response = {
                'error': 'Invalid sort direction.',
                'valid_directions': ['asc', 'desc']
            }
            return jsonify(response), 400

        # Sort the posts based on the provided parameters
        sorted_posts = sorted(POSTS, key=lambda post: post.get(sort_field, ''),
                              reverse=(direction == 'desc'))

        return jsonify(sorted_posts)
    else:
        # No sort parameters provided, return the original order of posts
        return jsonify(POSTS)


# handles HTTP POST requests to the /api/posts endpoint for creating new blog posts
@app.route('/api/posts', methods=['POST'])
def create_post():
    """function handles the creation of new blog posts by extracting the title and content from the request JSON,
    validating the data, generating a unique ID, adding the new post to the POSTS list,
    and returning the created post as a JSON response"""
    data = request.get_json()  # extract the JSON data
    title = data.get('title')  # retrieve the value of the 'title'
    content = data.get('content')  # retrieve the value of the 'content'

    # checks if both the title and content are missing
    if not title and not content:
        response = {
            'error': 'Both title and content are missing.',
            'missing_fields': ['title', 'content']
        }
        return jsonify(response), 400
    elif not title:  # check if title is missing
        response = {
            'error': 'Title is missing.',
            'missing_fields': ['title']
        }
        return jsonify(response), 400
    elif not content:  # check if content is missing
        response = {
            'error': 'Content is missing.',
            'missing_fields': ['content']
        }
        return jsonify(response), 400

    # creates a new dictionary new_post with an ID, title, and content based on the provided title and content variables.
    new_post = {
        'id': len(POSTS) + 1,  # Generate a new unique ID
        'title': title,
        'content': content
    }
    POSTS.append(new_post)  # adding a new blog post to the list

    # returns the new_post dictionary as a JSON response with a status code of 201 Created
    return jsonify(new_post), 201


# handles HTTP DELETE requests to the /api/posts/<id> endpoint for deleting a specific blog post based on its ID
@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """ function handles the deletion of a specific blog post based on its ID by searching for the post in the POSTS list,
    removing it if found, and returning a JSON response indicating the success or failure of the deletion operation"""
    post_index = None
    for index, post in enumerate(POSTS):
        if post['id'] == id:
            post_index = index
            break

    if post_index is None:
        response = {
            'error': 'Post not found.'
        }
        return jsonify(response), 404

    deleted_post = POSTS.pop(post_index)
    response = {
        'message': f"Post with id {id} has been deleted successfully."
    }
    return jsonify(response), 200


# handles HTTP PUT requests to the /api/posts/<id> endpoint for updating a specific blog post based on its ID
@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """ function handles the update of a specific blog post based on its ID by retrieving the new title and content from the request JSON,
     finding the post in the POSTS list,
     updating its fields if found, and
     returning the updated post as a JSON response"""
    data = request.get_json()
    new_title = data.get('title')
    new_content = data.get('content')

    post = None
    for p in POSTS:
        if p['id'] == id:
            post = p
            break

    if not post:
        response = {
            'error': 'Post not found.'
        }
        return jsonify(response), 404

    if new_title:
        post['title'] = new_title
    if new_content:
        post['content'] = new_content

    updated_post = {
        'id': post['id'],
        'title': post['title'],
        'content': post['content']
    }
    return jsonify(updated_post), 200


# handles HTTP GET requests to the /api/posts/search endpoint for searching blog posts based on specified search criteria
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """function handles the search for blog posts based on the provided title and/or content search criteria,
    returning a JSON response containing the matched posts.
    If no search criteria are provided, an empty response is returned"""
    title = request.args.get('title')
    content = request.args.get('content')

    if not title and not content:
        return jsonify([])

    matched_posts = []
    for post in POSTS:
        if title and title.lower() in post['title'].lower():
            matched_posts.append(post)
        elif content and content.lower() in post['content'].lower():
            matched_posts.append(post)

    return jsonify(matched_posts)


# runs the Flask application when the Python script is executed directly,
# starting the server on host="0.0.0.0" and port=5002 with debug mode enabled.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
