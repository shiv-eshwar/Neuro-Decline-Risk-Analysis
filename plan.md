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

---

## Phase 4: In-App Interactive Assessment (New) ✅
- [x] Build `/assessment` route and Assessment Wizard Shell
  - Step-by-step UI (Typing → Reaction → Memory → Voice)
  - Replace/Update "New Session" button to navigate to `/assessment`
- [x] Implement **Typing Test**:
  - UI: Prompted text paragraph and a `text_area` for user input
  - Logic: Track start time, end time, keystrokes, and errors to calculate WPM, error rate, and interval variance.
- [x] Implement **Reaction Test**:
  - UI: Interactive target area that turns green at random intervals.
  - Logic: Record reaction times across 3-5 trials, detecting anticipation errors and calculating mean RT and variance.
- [x] Implement **Memory Test**:
  - UI: Display a sequence of items (numbers/words) for 3 seconds, hide them, and prompt user to recall.
  - Logic: Calculate recall accuracy, false positives, and sequence memory score.
- [x] Implement **Voice Test & Integration**:
  - UI: Reading prompt with a "Start/Stop Recording" simulated interaction.
  - Logic: Generate voice metrics based on duration and expected reading speed.
  - Finalization: Compile all 4 domain metrics into a `SessionData` object, run the analysis engine, append to history, and redirect to the new session detail page.