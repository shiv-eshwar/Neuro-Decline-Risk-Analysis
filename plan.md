# NeuroWatch — Neurological Behavioral Analyst Dashboard

## Design Direction
- **Aesthetic**: Clinical yet warm — inspired by health-tech dashboards
- **Accent Color**: Teal/cyan (`#0d9488` / teal-600)
- **Surfaces**: White cards with subtle borders on slate-50 background
- **Typography**: Inter font, strong hierarchy

---

## Phase 1: Core Layout, Dashboard Overview & Data Models ✅
- [x] Define state models and dashboard UI
- [x] Populate with realistic sample data

## Phase 2: Session Detail View & Analysis Engine ✅
- [x] Session Detail page with metric panels
- [x] Implement analysis engine (baseline comparison, domain scoring)

## Phase 3: Trends, Alerts & Settings Pages ✅
- [x] Multi-line trends charts
- [x] Alerts history and settings page

## Phase 4: In-App Interactive Assessment ✅
- [x] Build `/assessment` route and Assessment Wizard Shell
- [x] Implement Typing, Reaction, Memory, and Voice Tests
- [x] Finalize assessment into session data and redirect

---

## Phase 5: Authentication System (Login & Signup) ✅
- [x] Create `AuthState` to handle user authentication logic (login, signup, logout, route protection).
- [x] Build `/login` page with clean, clinical design matching the app.
- [x] Build `/signup` page for new user registration.
- [x] Protect existing routes (`/`, `/assessment`, `/sessions`, etc.) by redirecting unauthenticated users to `/login`.
- [x] Add a logout button to the sidebar.