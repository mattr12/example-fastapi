from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .. import models, schemas, oauth2, database

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_vote(
    vote: schemas.VoteCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    if vote.dir != 1 and vote.dir != 0:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail="Value vote.dir not in range: [0, 1]",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already voted on post.",
            )
        else:
            try:
                new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)

                db.add(new_vote)
                db.commit()

                return {"message": "Successfully added vote."}
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id: {vote.post_id} not found.",
                )

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote not found.",
            )
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message": "Successfully deleted vote."}
