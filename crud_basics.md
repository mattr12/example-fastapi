### CRUD

Create              POST               /posts
Read                GET                /posts
Read (singular)     GET                /posts/:id
Update              PUT/PATCH          /posts/:id 
Delete              DELETE             /posts/:id

### CRUD in FastAPI

```python
# creates a post
@app.post("/posts")

# gets all posts
@app.get("/posts")

# gets specific post with {id}
@app.get("/posts/{id}")

# updates specific post with {id}
@app.put("/posts/{id}")

# deletes speciic post with {id}
@app.delete("/posts/{id}")
```

# Note on naming

Use the plural form of the noun, ie: posts not post; users not user.

# Note on updating

A PUT request provides ALL the information, whereas a PATCH operation provides SOME of what is updated.