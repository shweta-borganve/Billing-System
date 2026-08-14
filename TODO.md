# Backend Improvement TODO

## 1. Refactor project structure and clean modules
Definition of Done:
- Split responsibilities into clear modules such as `auth`, `billing`, `products`, `database`, and `services`.
- Remove duplication, keep naming consistent, and ensure each file has a single clear responsibility.

## 2. Add config, env management and secrets handling
Definition of Done:
- Move hardcoded values into environment variables and a central config loader.
- Add sample `.env.example` and secure handling for secret keys, DB credentials, and API settings.

## 3. Improve validation, logging and error handling
Definition of Done:
- Add strict input validation for all billing and product actions with clear error messages.
- Replace ad-hoc `print` usage with structured logging and consistent error handling across the app.

## 4. Add authentication, roles and secure access rules
Definition of Done:
- Add login/session or token-based authentication and define access roles for admin and staff users.
- Protect sensitive endpoints and enforce permission checks before any billing or product mutation.

## 5. Add tests, migrations and CI validation
Definition of Done:
- Add a proper test framework such as `pytest` with unit and integration coverage for billing logic and auth flows.
- Add database migration scripts and CI pipelines to run linting, tests, and validation automatically on every push.
