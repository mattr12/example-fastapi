from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)


###
### Pydantic schema that validates that the frontend
### sent the expected data model
###
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# try:
#     conn = psycopg2.connect(
#         host="localhost",
#         database="fastapi",
#         user="fastapi_admin",
#         password="fastapi",
#         cursor_factory=RealDictCursor,
#     )

#     cursor = conn.cursor()

#     print("Database connection was successful!")
# except Exception as error:
#     print("Connecting to database failed")
#     print("Error: ", error)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to my API"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return {"data": posts}


@app.get("/posts/{id}")
def get_post(
    id: int, db: Session = Depends(get_db)
):  # implicity validates and converts id to int
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *
    # """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    # UPDATE posts
    # SET
    # title = %s, content = %s, published = %s
    # WHERE id = %s
    # RETURNING *;
    # """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}
