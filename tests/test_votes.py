import pytest
from app import models


@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user['id']) 
    session.add(new_vote)
    session.commit()

# dir no caso é para adicionar um voto no post

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1}) 
    assert res.status_code == 201

# para esse test um voto já deve ter sito feito em um post. Por isso foi criado o fixture test_vote para isso

def test_vote_twice_in_vote_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id":test_posts[3].id, "dir": 1}) # voto repetido (não permitido)
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_vote, test_posts):
    res = authorized_client.post("/vote/", json={"post_id":test_posts[3].id, "dir": 0}) # dir 0 deletar um voto
    assert res.status_code == 201

# testa a tentativa de excluir um voto que não existe
def test_delete_vote_that_not_exists(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id":test_posts[3].id, "dir": 0}) # voto não existe.
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id":800000, "dir": 1}) # voto não existe.
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id":test_posts[3].id, "dir": 0}) # voto não existe.
    assert res.status_code == 401

