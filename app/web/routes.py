from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.api import deps
from app.core.config import settings
from app.services.auth_service import auth_service
from app.services.post_service import post_service
from app.core import security
from app.models.user import User
import markdown2
import bleach

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

from bleach.css_sanitizer import CSSSanitizer

# Define Markdown filter constants for performance
ALLOWED_MARKDOWN_TAGS = bleach.ALLOWED_TAGS | {
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'pre', 'code', 'span', 'div', 'br', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td'
}
ALLOWED_MARKDOWN_ATTRS = bleach.ALLOWED_ATTRIBUTES.copy()
ALLOWED_MARKDOWN_ATTRS['*'] = ['class', 'style']
ALLOWED_MARKDOWN_ATTRS['img'] = ['src', 'alt', 'title']

css_sanitizer = CSSSanitizer(allowed_css_properties=[
    'color', 'font-weight', 'text-align', 'margin', 'padding'
])

def markdown_filter(text):
    # Convert markdown to HTML
    html = markdown2.markdown(text, extras=["fenced-code-blocks", "tables"])
    # Sanitize HTML with CSS sanitizer for security
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_MARKDOWN_TAGS,
        attributes=ALLOWED_MARKDOWN_ATTRS,
        css_sanitizer=css_sanitizer
    )
    return clean_html

templates.env.filters["markdown"] = markdown_filter

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: Optional[User] = Depends(deps.get_current_user)
):
    posts = post_service.get_published_posts(db, limit=5)
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "user": current_user}
    )

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request, current_user: Optional[User] = Depends(deps.get_current_user)):
    if current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request, "login.html", {"user": current_user})

@router.post("/login")
async def login_post(
    request: Request,
    db: Session = Depends(deps.get_db),
    username: str = Form(...),
    password: str = Form(...)
):
    user = auth_service.authenticate(db, email=username, password=password)
    if not user:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Invalid email or password", "user": None}
        )

    access_token = security.create_access_token(subject=user.id)
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

@router.get("/posts", response_class=HTMLResponse)
async def posts_list(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: Optional[User] = Depends(deps.get_current_user)
):
    posts = post_service.get_published_posts(db)
    return templates.TemplateResponse(
        request,
        "posts/list.html",
        {"posts": posts, "user": current_user}
    )

@router.get("/posts/{id}", response_class=HTMLResponse)
async def post_detail(
    id: int,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: Optional[User] = Depends(deps.get_current_user)
):
    post = post_service.get_post(db, post_id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse(
        request,
        "posts/detail.html",
        {"post": post, "user": current_user}
    )

@router.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request,
    current_user: User = Depends(deps.get_current_active_user)
):
    return templates.TemplateResponse(
        request,
        "profile.html",
        {"user": current_user}
    )

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    posts = post_service.get_posts(db)
    return templates.TemplateResponse(
        request,
        "dashboard/index.html",
        {"posts": posts, "user": current_user}
    )

@router.get("/dashboard/posts/new", response_class=HTMLResponse)
async def post_create_get(
    request: Request,
    current_user: User = Depends(deps.get_current_active_admin)
):
    return templates.TemplateResponse(
        request,
        "dashboard/post_form.html",
        {"user": current_user, "action": "Create"}
    )

@router.post("/dashboard/posts/new")
async def post_create_post(
    request: Request,
    db: Session = Depends(deps.get_db),
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(False),
    current_user: User = Depends(deps.get_current_active_admin)
):
    from app.schemas.post import PostCreate
    post_in = PostCreate(title=title, content=content, published=published)
    post_service.create_post(db, obj_in=post_in, author_id=current_user.id)
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@router.get("/dashboard/posts/{id}/edit", response_class=HTMLResponse)
async def post_edit_get(
    id: int,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    post = post_service.get_post(db, post_id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse(
        request,
        "dashboard/post_form.html",
        {"user": current_user, "post": post, "action": "Edit"}
    )

@router.post("/dashboard/posts/{id}/edit")
async def post_edit_post(
    id: int,
    request: Request,
    db: Session = Depends(deps.get_db),
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(False),
    current_user: User = Depends(deps.get_current_active_admin)
):
    from app.schemas.post import PostUpdate
    db_obj = post_service.get_post(db, post_id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Post not found")
    post_in = PostUpdate(title=title, content=content, published=published)
    post_service.update_post(db, db_obj=db_obj, obj_in=post_in)
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@router.delete("/dashboard/posts/{id}")
async def post_delete(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    post_service.delete_post(db, post_id=id)
    return HTMLResponse(content="") # HTMX will remove the row
