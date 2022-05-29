from pydantic import BaseModel


###
### Pydantic schema that validates that the frontend
### sent the expected data model
###
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
