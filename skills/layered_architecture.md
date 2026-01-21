# Layered Architecture Enforcement

## Purpose
Ensure that all features follow the `Route -> Service -> Repository -> Model` pattern to maintain separation of concerns and testability.

## When to Use
- When adding a new endpoint or feature.
- When refactoring existing logic.
- When modifying data access patterns.

## Rules
1. **Repository Layer:** Create or update a class in `app/repositories/` for all database interactions. Use SQLAlchemy 2.0 style.
2. **Service Layer:** Implement business logic in `app/services/`. Services should be the only ones calling repositories.
3. **Route Layer:** In `app/api/routes/` or `app/web/routes.py`, validate input with Pydantic and call the appropriate service.
4. **Dependency Injection:** Use `app.api.deps.get_db` to provide the session to services and repositories.

## Constraints
- Never perform database operations (query/add/delete) directly in a Route.
- Repositories should return Models or Schemas, not Raw SQL results.

## Expected Output
A set of changes across at least three files (Schema, Route, Service, and Repository) that implements the feature following the defined layers.
