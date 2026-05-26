# TrustFlow KYC - Merchant Onboarding Pipeline

A high-integrity KYC (Know Your Customer) compliance pipeline featuring a decoupled full-stack architecture, database-enforced state transitions, secure merchant registration, and a reviewer queue with live SLA monitoring.

## 🏗️ Tech Stack

- **Frontend**: React + Vite
- **Backend**: Django + Django REST Framework
- **Database**: PostgreSQL (Strictly enforced)

## 🚀 Key Features

- **State Machine Integrity**: Model-level state transition checks to prevent illegal status bypasses.
- **Merchant Audits & History**: Submissions use a `ForeignKey` relationship instead of `OneToOneField` to let merchants maintain and view an iterative application history.
- **FIFO Reviewer Queue**: Chronological prioritization queue with a frontend SLA badge flagging applications unresolved for over 24 hours as "At Risk".
- **Dynamic CORS & SSL**: Dynamic allowed host mapping for Render deployments, and custom SSL checks tailored for remote vs. local connections.

## 🛠️ Local Development

### Backend Setup

1. `cd backend`
2. `pip install -r requirements.txt`
3. Configure your local settings in a `.env` file (see `.env.example`).
4. `python manage.py migrate`
5. `python manage.py runserver`

### Frontend Setup

1. `cd frontend`
2. `npm install`
3. `npm run dev`

---

For details on database migrations, security choices, and state design decisions, see the [EXPLAINER.md](./EXPLAINER.md).
