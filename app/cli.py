import argparse
import sys
from app.core.database import SessionLocal
from app.repositories.user_repo import user_repo
from app.schemas.user import UserCreate
from app.models.user import User  # Required for mapper initialization
from app.models.post import Post  # Required for mapper initialization

def create_admin(email, password, full_name):
    db = SessionLocal()
    try:
        user = user_repo.get_by_email(db, email=email)
        if user:
            print(f"Erro: Usuário com email {email} já existe.")
            sys.exit(1)

        user_in = UserCreate(
            email=email,
            password=password,
            full_name=full_name
        )
        user = user_repo.create(db, obj_in=user_in)
        user.role = "admin"
        db.commit()
        db.refresh(user)
        print(f"Sucesso! Admin '{full_name}' ({email}) criado com sucesso.")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utilitário de CLI para o Mini Blog")
    subparsers = parser.add_subparsers(dest="command")

    # create-admin command
    admin_parser = subparsers.add_parser("create-admin", help="Cria um novo usuário administrador")
    admin_parser.add_argument("--email", required=True, help="Email do admin")
    admin_parser.add_argument("--password", required=True, help="Senha do admin")
    admin_parser.add_argument("--name", required=True, help="Nome completo do admin")

    args = parser.parse_args()

    if args.command == "create-admin":
        create_admin(args.email, args.password, args.name)
    else:
        parser.print_help()
