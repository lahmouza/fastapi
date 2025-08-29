from typing import Optional

from sqlalchemy import func
from .. import model,schemas,utils


from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from sqlalchemy.orm import Session 
from .. import main ,oauth2



router = APIRouter(
    prefix="/posts" ,
    tags=["Posts"]
)



@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search: Optional[str]=""):
    # This function would typically retrieve posts from a database
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    

    results=db.query(model.Post).join(model.Vote, model.Vote.post_id==model.Post.id, isouter=True).group_by(model.Post.id).add_columns(func.count(model.Vote.post_id).label("votes")).filter(model.Post.title.contains(search)).limit(limit).offset(offset=skip).all()
    

    
    
    return results 


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(new_post:schemas.PostCreate,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning * """,(new_post.title, new_post.content, new_post.published))
    # post = cur.fetchone()
    # conn.commit()
    print(user_id)
    owner=user_id.id
    post=model.Post(owner_id=owner,**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post




@router.get("/{post_id}",response_model=schemas.PostOut)
def get_one_post(post_id: int,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id),))
    # post = cur.fetchone()
    # post=db.query(model.Post).filter(model.Post.id==post_id).first()
    post=db.query(model.Post).join(model.Vote, model.Vote.post_id==model.Post.id, isouter=True).group_by(model.Post.id).add_columns(func.count(model.Vote.post_id).label("votes")).filter(model.Post.id==post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {post_id} not found")

    print(post_id)
    return  post





@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), user_data: schemas.TokenData = Depends(oauth2.get_current_user)):
    #find the index of the post to delete
    #posts.pop(post_id)

    # cur.execute("""DELETE FROM posts WHERE id = %s""", (str(post_id),))
    # deleted_post = cur.fetchone()
    # conn.commit()
    deleted_post=db.query(model.Post).filter(model.Post.id==post_id).first()
    

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {post_id} not found")
    if deleted_post.owner_id != int(user_data.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{post_id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_data: schemas.TokenData = Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""",
    #             (updated_post.title, updated_post.content, updated_post.published, str(post_id)))
    # post = cur.fetchone()
    # conn.commit()

    post_query = db.query(model.Post).filter(model.Post.id == post_id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {post_id} not found")
    
    if post.owner_id != int(user_data.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post_query.first()) 
    return post_query.first()

