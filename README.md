# TrustFlow KYC — Merchant Onboarding & Compliance System

A decoupled full-stack KYC compliance pipeline for onboarding merchants and managing document verification — with a database-enforced state machine, role-based access control, and SLA tracking.

🔗 **Live:** [trustflow-kyc.vercel.app/login](https://trustflow-kyc.vercel.app/login)

---

## The Problem

KYC compliance systems need to enforce strict business logic at every stage. The challenge isn't collecting data — it's preventing:

- Illegal state jumps (e.g. draft → approved, bypassing review)
- Horizontal privilege escalation (one merchant accessing another's data)
- SLA breaches going unnoticed in the reviewer queue

TrustFlow solves all three.

---

## Key Features

### Database-Enforced State Machine

States: `draft → submitted → under_review → approved / rejected / more_info_requested`

State transitions are validated at the **database/backend layer** — not the frontend. A malicious API call attempting an illegal jump (e.g. `rejected → approved`) is blocked at the model level, regardless of client behavior.

```
draft
  └→ submitted
       └→ under_review
            ├→ approved
            ├→ rejected
            └→ more_info_requested
                 └→ submitted (merchant can re-submit)
```

### Role-Based Access Control

| Role     | Capabilities                                           |
| -------- | ------------------------------------------------------ |
| Merchant | Register, create/edit drafts, submit, view own history |
| Reviewer | Access FIFO queue, transition states, view documents   |

Query-level data isolation — every merchant query filters by `authenticated user`. Horizontal privilege escalation is impossible by design.

### FIFO Reviewer Queue

- Sorts submissions chronologically (oldest first)
- Uses database aggregation to surface **only the latest submission per merchant** — prevents queue clutter from re-submissions
- Merchants with multiple attempts show only their current active submission

### SLA Tracking

- Client-side calculation against submission timestamp
- Applications exceeding **24-hour turnaround** are flagged **"At Risk"** in the reviewer dashboard
- Zero database polling — pure frontend logic

### Submission Version History

Merchants can view a full audit log of all their past submissions (drafts, approved, rejected) at the bottom of their dashboard.

### Document Validation

- Accepted formats: `.pdf`, `.jpg`, `.png`
- Max file size: **5MB** — enforced at serializer layer before touching server memory

---

## Tech Stack

| Layer      | Technology                                         |
| ---------- | -------------------------------------------------- |
| Frontend   | React 18 · Vite · React Router · Vanilla CSS       |
| Backend    | REST API (decoupled)                               |
| Database   | PostgreSQL                                         |
| Auth       | JWT Token Authentication · PBKDF2 password hashing |
| Deployment | Vercel (Frontend) · Render (Backend)               |

### PostgreSQL Configuration

- Adaptive SSL: `sslmode=require` on Render, bypassed for localhost
- Strict PostgreSQL enforcement — no SQLite fallback (prevents state mismatches under multi-worker deployment)

---

## Architecture

```
React Frontend (Vercel)
    ↕ HTTP/JSON + JWT
REST API Backend (Render — Gunicorn multi-worker)
    ↕ ORM
PostgreSQL Database (Render)
```

---

## API Endpoints

| Method | Endpoint                                           | Description                 |
| ------ | -------------------------------------------------- | --------------------------- |
| POST   | `/api/v1/auth/register/`                           | Register new merchant       |
| POST   | `/api/v1/auth/token/`                              | Issue auth token            |
| GET    | `/api/v1/kyc/submissions/`                         | List merchant's submissions |
| POST   | `/api/v1/kyc/submissions/`                         | Create new draft            |
| PATCH  | `/api/v1/kyc/submissions/<id>/`                    | Update draft                |
| POST   | `/api/v1/kyc/submissions/<id>/submit_application/` | Submit for review           |
| GET    | `/api/v1/kyc/reviewer-queue/`                      | FIFO queue for reviewers    |
| POST   | `/api/v1/kyc/reviewer-queue/<id>/change_state/`    | Transition submission state |

---

## Getting Started

```bash
# Clone
git clone https://github.com/AbhiEE03/TrustFlow_KYC.git

# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
pip install -r requirements.txt
# Add .env: DATABASE_URL, SECRET_KEY, ALLOWED_HOSTS
python manage.py migrate
python manage.py runserver
```

**Test credentials (demo):**

- Merchant: Register via Sign Up
- Reviewer: Contact for demo reviewer access

---

## Screenshots

> Login · Merchant Dashboard · Onboarding Form · Draft State · Submitted State · Reviewer Queue

_(See screenshots in /docs or live demo above)_

---

## What I Learned

- Designing state machines that enforce business logic at the right layer
- Building systems resilient to API bypass and UI tampering
- PostgreSQL SSL configuration for multi-environment deployment
- Efficient queue design using aggregation instead of polling
