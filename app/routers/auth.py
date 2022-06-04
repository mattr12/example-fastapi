from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session


from .. import models, utils, database, schemas

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials."
        )

    is_verified = utils.verify(credentials.password, user.password)

    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials."
        )

    return {"token": "example token"}
