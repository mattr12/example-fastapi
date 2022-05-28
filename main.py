from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

###
### Pydantic schema that validates that the frontend
### sent the expected data model
###
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to my API"}


@app.get("/posts")
def get_posts():
    return {"data": "Here are your posts!"}


@app.post("/createposts")
def create_posts(post: Post):
    print(post.title)
    print(post.published)

    return {"data": "new post"}
