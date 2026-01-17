from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=20)
    published: Optional[bool] = False

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    content: Optional[str] = Field(None, min_length=20)

class PostInDBBase(PostBase):
    id: int
    created_at: datetime
    author_id: int

    model_config = ConfigDict(from_attributes=True)

class Post(PostInDBBase):
    pass
