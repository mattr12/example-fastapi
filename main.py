from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

###
### Pydantic schema that validates that the frontend
### sent the expected data model
###
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
    {"title": "title of post 3", "content": "content of post 3", "id": 3},
]


def _find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def _find_post_index(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to my API"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):  # implicity validates and converts id to int
    post = _find_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()

    post_dict["id"] = randrange(0, 1e9)

    my_posts.append(post_dict)

    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = _find_post_index(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = _find_post_index(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )

    post_dict = post.dict()

    post_dict["id"] = id

    my_posts[index] = post_dict

    return {"data": post_dict}
