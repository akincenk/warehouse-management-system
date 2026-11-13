# Roadmap

Work I plan to do next, roughly in this order. Each item has an issue in the tracker.
Estimates are rough and include tests and docs.

## 1. Database migrations (about 3 h)

- Add Alembic, generate the initial migration from the current models.
- Stop calling `create_all` on startup; run migrations in Docker and CI instead.

## 2. Richer products (about 5 h)

- Add SKU code (unique), description, location (aisle / bin) and a reorder point.
- Search and filter products by name, SKU and location; pagination on the list.

## 3. Stock movements and audit history (about 6 h)

- Quantity changes go through stock-in / stock-out / adjustment endpoints instead of a plain edit.
- Every change records who did it, when and why; history view per product.

## 4. Auth hardening (about 5 h)

- Login rate limiting per username and IP.
- Refresh tokens with revocation on logout and on role change.
- Move the frontend token out of `localStorage`.

## 5. Frontend (about 8 h)

- Product list with search, create/edit forms for managers, user role screen for admins.
- Show and hide actions by role.
- Component tests with Vitest and React Testing Library, run in CI.

## 6. Housekeeping (about 2 h)

- Docker Compose for backend + frontend together.
- Seed script with made-up sample data for demos.
- Tag a first release (`v0.1.0`) with a changelog.
