from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from typing import List, Optional

class PostRepository:
    def get_by_id(self, db: Session, post_id: int) -> Optional[Post]:
        return db.query(Post).filter(Post.id == post_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).offset(skip).limit(limit).all()

    def get_published(self, db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).filter(Post.published == True).offset(skip).limit(limit).all()

    def create_with_author(self, db: Session, obj_in: PostCreate, author_id: int) -> Post:
        db_obj = Post(
            title=obj_in.title,
            content=obj_in.content,
            published=obj_in.published,
            author_id=author_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Post, obj_in: PostUpdate) -> Post:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Post:
        obj = db.get(Post, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

post_repo = PostRepository()
