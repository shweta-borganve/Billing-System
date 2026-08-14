# Backend Improvement TODO

## Phase 1: Core Backend Improvements

### 1. Refactor project structure and clean modules
Definition of Done:
- Split responsibilities into clear modules such as `auth`, `billing`, `products`, `database`, and `services`.
- Remove duplication, keep naming consistent, and ensure each file has a single clear responsibility.

### 2. Add config, env management and secrets handling
Definition of Done:
- Move hardcoded values into environment variables and a central config loader.
- Add sample `.env.example` and secure handling for secret keys, DB credentials, and API settings.

### 3. Improve validation, logging and error handling
Definition of Done:
- Add strict input validation for all billing and product actions with clear error messages.
- Replace ad-hoc `print` usage with structured logging and consistent error handling across the app.

### 4. Add authentication, roles and secure access rules
Definition of Done:
- Add login/session or token-based authentication and define access roles for admin and staff users.
- Protect sensitive endpoints and enforce permission checks before any billing or product mutation.

### 5. Add tests, migrations and CI validation
Definition of Done:
- Add a proper test framework such as `pytest` with unit and integration coverage for billing logic and auth flows.
- Add database migration scripts and CI pipelines to run linting, tests, and validation automatically on every push.

---

## Phase 2: Testing & Pipeline Infrastructure

### 6. Add quick linting pipelines (black, ruff, isort)
Definition of Done:
- Add black, ruff, and isort to requirements.txt
- Create configuration for each tool in pyproject.toml

### 7. Add mypy static type checking
Definition of Done:
- Add mypy to requirements.txt with pyproject.toml configuration
- Run mypy to identify and fix type issues across codebase

### 8. Add bandit security scanning
Definition of Done:
- Add bandit to requirements.txt
- Configure bandit to scan auth, database, and file operations for vulnerabilities

### 9. Add safety/pip-audit dependency scanning
Definition of Done:
- Add safety or pip-audit for dependency vulnerability detection
- Configure to run on requirements.txt

### 10. Add pre-commit git hooks setup
Definition of Done:
- Configure pre-commit framework
- Add hooks for black, ruff, mypy, and bandit to run automatically before commits

### 11. Create tests/ directory structure
Definition of Done:
- Create `tests/` directory at project root
- Organize tests with clear naming convention (test_*.py)

### 12. Move test_main.py into tests/ directory
Definition of Done:
- Move existing test_main.py from root to tests/
- Ensure imports and paths still work correctly

### 13. Add pyproject.toml with pytest config
Definition of Done:
- Configure pytest in pyproject.toml with:
  - `testpaths = ["tests"]` to specify test location
  - `python_files = ["test_*.py"]` for test discovery
  - Coverage settings and output options

### 14. Add conftest.py for shared test fixtures
Definition of Done:
- Create conftest.py in tests/ directory
- Add shared fixtures for database mocking, authentication mocks, and common test setup
