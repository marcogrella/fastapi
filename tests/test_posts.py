from typing import List
from app import schemas
import pytest

from routers.post import update_post


# authorized_client já possui um token válido. 
# test_posts é um fixture que salva 3 posts com um usuário 

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
  
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json()) # chama a função acima e retorna os valores já convertidos para o tipo PostOut
    posts_list = list(posts_map) # converte de map para lista

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
     
# testar get_all posts com o usuário não autenticado 
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

# testar get_post by id  com o usuário não autenticado 
def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts): 
    res = authorized_client.get(f"/posts/888888")
    assert res.status_code == 404



def test_get_one_post(authorized_client, test_posts): 
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = schemas.PostOut(**res.json()) # desempacota a resposta em um postOut
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome content", True),
    ("favorite another new title", "favorite another new content", True),
    ("Another new brand new title", "another new brand new conent", False),
    ])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(f"/posts/", json={"title": title, "content": content, "published": published})

    # convertendo para o modelo de saída (response)
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']



def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(f"/posts/", json={"title": "título de teste", "content": "conteúdo qualquer"})

    # convertendo para o modelo de saída (response)
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == "título de teste"
    assert created_post.content ==  "conteúdo qualquer"
    assert created_post.published == True # deve ser true porque é um valor default.
    assert created_post.user_id == test_user['id']


def test_unauthorized_user_create_posts(client, test_posts):
    res = client.post(f"/posts/", json={"title": "título de teste", "content": "conteúdo qualquer"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8000000")
    assert res.status_code == 404


def test_deleting_post_that_belongs_to_another_user(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}") # id do post não pertence ao id do usuario. 
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    update_post = schemas.Post(**res.json()) # converte o retorno para o response model. 
    assert res.status_code == 200
    assert update_post.title == data['title']
    assert update_post.content == data['content']


def test_update_others_user_post(authorized_client, test_user, test_posts, test_user_2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id    # pertencente ao test_user_2
    }

    # como se o usuário test_user estivesse tentando alterar um post que não pertence a ele. 
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403



def test_update_postn_non_exists(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id    # pertencente ao test_user_2
    }
    
    res = authorized_client.put(f"/posts/10000000000000", json=data)
    assert res.status_code == 404