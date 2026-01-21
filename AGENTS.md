# AGENTS.md

## Project Context
**Project Name:** Mini Blog API (Retro Tech Archive)
**Tech Stack:** FastAPI, SQLAlchemy 2.0 (DeclarativeBase), Pydantic 2, Alembic, Jinja2, HTMX, Tailwind/Custom CSS.
**Aesthetic:** Retro Modern (Off-white `#F5F1EA`, Moss Green `#4A5D4E`, Petroleum Blue `#2F4F4F`).

## Architectural Rules
1. **Layer Separation:** Strictly follow the pattern: `Routes -> Services -> Repositories -> Models`.
   - **Routes:** Handle HTTP concerns, schema validation, and dependency injection.
   - **Services:** Orchestrate business logic and domain rules.
   - **Repositories:** Encapsulate database access via SQLAlchemy ORM.
   - **Models:** Declarative database entities.
2. **Database Access:** Routes and Services MUST NOT use the SQLAlchemy `Session` directly to perform queries. All persistence logic must reside in Repositories.
3. **Admin Creation:** Administrators must only be created through the CLI (`app/cli.py`) to prevent privilege escalation via registration endpoints.
4. **Content Rendering:** All user-generated content (Markdown) must be sanitized using the `markdown` filter in `app/web/routes.py` (which uses `bleach` and `CSSSanitizer`).

## Reasoning Requirements
Before acting, agents must:
1. **Trace the Flow:** Identify the affected layers (Schema -> Route -> Service -> Repository).
2. **Check Security:** Verify if the change affects RBAC or sensitive data exposure.
3. **Design Alignment:** Ensure any UI changes adhere to the "Retro Modern" design system and color palette.
4. **Migration Audit:** If the schema changes, ensure a corresponding Alembic migration is planned.

## Forbidden Actions
- **No Direct DB in Routes:** Do not use `db.query()` or `db.add()` inside route handlers.
- **No Manual SQL:** Always use SQLAlchemy ORM expressions in repositories.
- **No Insecure Markdown:** Never render user content using `| safe` without passing it through the `markdown` filter first.
- **No Privilege Escalation:** Do not add `role` fields to `UserCreate` schemas.

## Proposal & Validation
- **Tests:** All backend changes must be verified with `pytest`. Run `export PYTHONPATH=$PYTHONPATH:. && python -m pytest`.
- **UI Verification:** Frontend changes must be captured via Playwright screenshots and visually inspected.
- **Migrations:** Run `alembic upgrade head` after schema modifications to verify migration integrity.
