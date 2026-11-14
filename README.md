# My Statement – Full-Stack Financial Dashboard

A professional full-stack personal financial dashboard that allows authenticated users to view their account balance, browse financial statements, navigate transaction history, and manage account information.

## Tech Stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, React Router, Axios
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite (Development)
- **Authentication:** JWT (JSON Web Tokens), Passlib (bcrypt)
- **Testing:** Pytest (Backend), Vitest + React Testing Library (Frontend), Playwright (E2E)

## Project Structure

```text
my-statement-dashboard/
├── backend/            # FastAPI application, SQLite DB, and Pytest suite
│   ├── app/            # Main application code (API routes, models, schemas, crud)
│   ├── tests/          # Pytest automated tests
│   ├── seed.py         # Database seeding script
│   └── requirements.txt
├── frontend/           # React + Vite application
│   ├── src/            # Components, pages, contexts, API clients
│   ├── e2e/            # Playwright End-to-End tests
│   ├── playwright.config.ts
│   ├── package.json
│   └── vite.config.ts
└── README.md