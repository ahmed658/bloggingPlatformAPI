from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    posts_retrieved_from_get_request = res.json()
    posts_added_by_post_request = test_posts
    
    def validate(post):
        return schemas.PostReturn(**post)
    
    for post in posts_added_by_post_request:
        validate(post)
        
    for post in posts_retrieved_from_get_request:
        validate(post)
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_added_by_post_request[0]['post_id'] == posts_retrieved_from_get_request[0]['post_id']
    
def test_create_post(authorized_client, test_user):
    post_data = {
        "title": "New Post Title",
        "content": "This is the content of the new post."
    }
    res = authorized_client.post("/posts/", json=post_data)
    created_post = schemas.PostReturn(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == post_data["title"]
    assert created_post.content == post_data["content"]
    assert created_post.author.username == test_user["username"]

def test_get_single_post(authorized_client, test_posts):
    post_id = test_posts[0]["post_id"]
    res = authorized_client.get(f"/posts/{post_id}")
    retrieved_post = schemas.PostReturn(**res.json())
    
    assert res.status_code == 200
    assert retrieved_post.post_id == post_id
    assert retrieved_post.title == test_posts[0]["title"]

def test_get_nonexistent_post(authorized_client):
    res = authorized_client.get("/posts/9999")
    assert res.status_code == 404
    assert res.json().get("detail") == "post with ID 9999 was not found."

def test_update_post(authorized_client, test_posts):
    post_id = test_posts[0]["post_id"]
    update_data = {
        "title": "Updated Title",
        "content": "Updated Content"
    }
    res = authorized_client.put(f"/posts/{post_id}", json=update_data)
    updated_post = schemas.PostReturn(**res.json())
    
    assert res.status_code == 200
    assert updated_post.title == update_data["title"]
    assert updated_post.content == update_data["content"]


def test_delete_post(authorized_client, test_posts):
    post_id = test_posts[0]["post_id"]
    res = authorized_client.delete(f"/posts/{post_id}")
    
    assert res.status_code == 204
    
    # Verify post is deleted
    res = authorized_client.get(f"/posts/{post_id}")
    assert res.status_code == 404


def test_search_posts(authorized_client, test_posts):
    search_query = "Post 1"
    res = authorized_client.get(f"/posts?search={search_query}")
    search_results = res.json()
    
    assert res.status_code == 200
    assert len(search_results) == 1
    assert search_query in search_results[0]["title"]

def test_pagination(authorized_client, test_posts):
    limit = 2
    skip = 1
    res = authorized_client.get(f"/posts?limit={limit}&skip={skip}")
    paginated_posts = res.json()
    
    assert res.status_code == 200
    assert len(paginated_posts) == limit
    assert paginated_posts[0]["post_id"] == test_posts[skip]["post_id"]
