from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User as UserModel
from app.schemas.post import Post, PostCreate, PostUpdate
from app.services.post_service import post_service

router = APIRouter()

@router.get("/", response_model=List[Post])
def read_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[UserModel] = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve posts. Admins see all, others see published only.
    """
    if current_user and current_user.role == "admin":
        posts = post_service.get_posts(db, skip=skip, limit=limit)
    else:
        posts = post_service.get_published_posts(db, skip=skip, limit=limit)
    return posts

@router.post("/", response_model=Post)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: PostCreate,
    current_user: UserModel = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Create new post. Only for admins.
    """
    return post_service.create_post(db, obj_in=post_in, author_id=current_user.id)

@router.put("/{id}", response_model=Post)
def update_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    post_in: PostUpdate,
    current_user: UserModel = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Update a post. Only for admins.
    """
    post = post_service.get_post(db, post_id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_service.update_post(db, db_obj=post, obj_in=post_in)

@router.get("/{id}", response_model=Post)
def read_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Get post by ID.
    """
    post = post_service.get_post(db, post_id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{id}", response_model=Post)
def delete_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: UserModel = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Delete a post. Only for admins.
    """
    post = post_service.get_post(db, post_id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_service.delete_post(db, post_id=id)
