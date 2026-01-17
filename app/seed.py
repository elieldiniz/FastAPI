from app.core.database import SessionLocal
from app.repositories.user_repo import user_repo
from app.repositories.post_repo import post_repo
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate
from app.core import security

def seed():
    db = SessionLocal()

    # Create admin user
    admin_user = user_repo.get_by_email(db, email="admin@blog.com")
    if not admin_user:
        admin_in = UserCreate(
            email="admin@blog.com",
            password="adminpassword",
            full_name="Alex Rivera"
        )
        admin_user = user_repo.create(db, obj_in=admin_in)
        admin_user.role = "admin"
        db.commit()
        db.refresh(admin_user)
        print("Admin user created.")

    # Create common user
    common_user = user_repo.get_by_email(db, email="reader@blog.com")
    if not common_user:
        user_in = UserCreate(
            email="reader@blog.com",
            password="readerpassword",
            full_name="Leitor Atento"
        )
        common_user = user_repo.create(db, obj_in=user_in)
        print("Common user created.")

    # Create some posts based on the images
    if post_repo.get_multi(db, limit=1) == []:
        post1 = PostCreate(
            title="The Resurgence of Mechanical Keyboards in the 21st Century",
            content="""For decades, the humble membrane keyboard reigned supreme in offices and homes...
            The shift wasn't just about nostalgia. As professional typing time increased and gaming became a global phenomenon...
            """,
            published=True
        )
        post_repo.create_with_author(db, obj_in=post1, author_id=admin_user.id)

        post2 = PostCreate(
            title="The Aesthetics of CRT Monitors",
            content="In the era of sleek LCDs and ultra-thin OLEDs, there's a growing movement rediscovering the warm glow of cathode ray tubes...",
            published=True
        )
        post_repo.create_with_author(db, obj_in=post2, author_id=admin_user.id)

        post3 = PostCreate(
            title="Draft: Future of Decentralized Web",
            content="This is a draft about Web3 and decentralization.",
            published=False
        )
        post_repo.create_with_author(db, obj_in=post3, author_id=admin_user.id)
        print("Initial posts created.")

    db.close()

if __name__ == "__main__":
    seed()
