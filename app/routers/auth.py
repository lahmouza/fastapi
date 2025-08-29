from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import model,schemas,utils,oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
def login(user:schemas.UserLogin,db:Session=Depends(get_db)):
    db_user=db.query(model.User).filter(model.User.email==user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not utils.verify(user.password,db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    access_token=oauth2.create_access_token(data={"user_id":db_user.id})
    
    
    return {"access_token":access_token,"token_type":"bearer"}


