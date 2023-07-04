from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This is the third post."},
    {"id": 4, "title": "First post", "content": "This is the tenth post."},
    {"id": 5, "title": "Fifth post", "content": "This is the fifth post."},
    {"id": 6, "title": "Sixth post", "content": "This is the sixth post."},
    {"id": 7, "title": "First post", "content": "This is the aseventh post."},

]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title and not content:
        response = {
            'error': 'Both title and content are missing.',
            'missing_fields': ['title', 'content']
        }
        return jsonify(response), 400
    elif not title:
        response = {
            'error': 'Title is missing.',
            'missing_fields': ['title']
        }
        return jsonify(response), 400
    elif not content:
        response = {
            'error': 'Content is missing.',
            'missing_fields': ['content']
        }
        return jsonify(response), 400

    new_post = {
        'id': len(POSTS) + 1,  # Generate a new unique ID
        'title': title,
        'content': content
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
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


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
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


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
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



@app.route('/api/posts', methods=['GET'])
def sorted_posts():
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    # Sorting logic
    if sort not in ['title', 'content']:
        return jsonify({'error': 'Invalid sort field'}), 400

    if direction not in ['asc', 'desc']:
        return jsonify({'error': 'Invalid sort direction'}), 400

    sorted_posts = sorted(POSTS, key=lambda p: p[sort].lower(),
                          reverse=(direction == 'desc'))

    # Return the sorted posts
    return jsonify({'posts': sorted_posts})


# @app.route('/api/posts/print', methods=['GET'])
# def sorted_posts():
#
#     search_content = request.args.get('search_content')
#     order = request.args.get('order')
#
#     # Filter the posts based on the search content
#     filtered_posts = [post for post in POSTS if search_content.lower() in post['title'].lower() or search_content.lower() in post['content'].lower()]
#
#     # Sort the filtered posts by ID
#     sorted_posts = sorted(filtered_posts, key=lambda x: x['id'], reverse=(order == "descending"))
#
#     # Prepare the response
#     response = []
#     for post in sorted_posts:
#         response.append({
#             "id": post['id'],
#             "title": post['title'],
#             "content": post['content']
#         })
#
#     return jsonify(response)




# @app.route('/api/posts', methods=['GET'])
# def sorted_posts():
#     sort_param = request.args.get('sort')
#     direction_param = request.args.get('direction')
#
#     if sort_param == 'title':
#         posts = sorted(POSTS, key=lambda p: p['title'])
#     elif sort_param == 'content':
#         posts = sorted(POSTS, key=lambda p: p['content'])
#     else:
#         posts = POSTS
#
#     if direction_param == 'desc':
#         posts.reverse()
#
#     return {'posts': posts}



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
