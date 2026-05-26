# TrustFlow KYC Onboarding: Architectural Decisions

This is a breakdown of the key logic, database, and structural decisions made for the **TrustFlow KYC** onboarding platform.

## 1. Preventing Illegal State Transitions
The status workflow is enforced strictly at the model layer (`backend/kyc/models.py`) using a state transition dictionary:
*   Transitions must match specific paths (e.g. `draft` -> `submitted` -> `under_review`).
*   Validation is executed inside the model's `clean()` and `save()` logic rather than views, ensuring that illegal bypasses are blocked regardless of UI state or direct API requests.

## 2. PostgreSQL Migration & Concurrency
To handle concurrent server requests and prevent race conditions in multi-worker production configurations, the persistence layer was moved completely to PostgreSQL:
*   Django settings strictly require a PostgreSQL engine.
*   Connection settings dynamically use `sslmode='require'` for remote databases (e.g. Render deployments) while bypassing SSL for local connections (`localhost`) to make development seamless.
*   Handles URL-encoded passwords with special characters (like `@` to `%40`) securely within `DATABASE_URL`.

## 3. Merchant Submission History (One-to-Many Relation)
Originally, a merchant could only have a single onboarding application. To support iterative updates (e.g., when a reviewer requests updates or rejects a draft):
*   Shifted from a `OneToOneField` to a `ForeignKey` relationship.
*   Merchants can now build a historical log of their submissions.
*   The Reviewer Queue remains efficient by fetching only the latest submission (`Max('id')`) per merchant, avoiding queue clutter.

## 4. Document Security & Size Limits
File uploads in the onboarding flow are vetted inside the serializer layer:
*   Type check: Limits uploads to safe, readable formats (`.pdf`, `.jpg`, `.png`).
*   Size check: Enforces a strict 5MB file ceiling at the serializer level before database insertion, protecting server storage.

## 5. Session and Token Hardening
*   Dynamic CORS mapping allows Vercel frontend communication while keeping backend host lists secure.
*   Stale authentication tokens are cleared on the login page mount, resolving credential collisions across browser tabs.
