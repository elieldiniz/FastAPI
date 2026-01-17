from sqlalchemy.orm import Session
from app.repositories.post_repo import post_repo
from app.schemas.post import PostCreate, PostUpdate
from app.models.post import Post
from typing import List, Optional

class PostService:
    def create_post(self, db: Session, obj_in: PostCreate, author_id: int) -> Post:
        return post_repo.create_with_author(db, obj_in=obj_in, author_id=author_id)

    def get_post(self, db: Session, post_id: int) -> Optional[Post]:
        return post_repo.get_by_id(db, post_id=post_id)

    def get_posts(self, db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
        return post_repo.get_multi(db, skip=skip, limit=limit)

    def get_published_posts(self, db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
        return post_repo.get_published(db, skip=skip, limit=limit)

    def update_post(self, db: Session, db_obj: Post, obj_in: PostUpdate) -> Post:
        return post_repo.update(db, db_obj=db_obj, obj_in=obj_in)

    def delete_post(self, db: Session, post_id: int) -> Post:
        return post_repo.remove(db, id=post_id)

post_service = PostService()
