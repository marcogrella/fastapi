from typing import List
from app import schemas


# authorized_client já possui um token válido. 
# test_posts é um fixture que salva 3 posts com um usuário 

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
  
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    print(posts_list)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

    