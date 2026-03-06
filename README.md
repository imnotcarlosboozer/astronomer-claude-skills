# Astronomer Claude Code Skills

Claude Code skills for Astronomer sales intelligence. Research companies for Apache Airflow fit, score pipeline opportunities, and generate AE briefs — all from within Claude Code.

Built for the Astronomer sales team. Works out of the box once the required file structure is in place (see setup below).

---

## Skills

### `account-research`
Researches a company for Astronomer (Apache Airflow) sales fitness. Runs 4 parallel data collection agents across Exa AI, Leadfeeder, Common Room, and Gong — then generates a scored report and pushes it to Apollo.

**Triggers**: "research [company]", "score [company]", "run batch account research"

**What it produces**:
- **Fit score** (0–20) across 5 dimensions: Orchestration Need · Data Platform Maturity · Stack Evidence · Scale & Compliance · Buying Signals
- **Letter grade** (A/B/C/D) and confidence level (HIGH/MEDIUM/LOW)
- **Full AE brief**: company overview, tech stack, hiring signals, pain points, key contacts, prior Gong conversations, website engagement, outreach hooks, persona talking points
- **Changelog** tracking score changes across re-runs
- **Apollo sync**: writes the full report to the `Account_Research` field in Apollo automatically

**Usage**:
```
# Single company
account-research "Acme Corp, acme.com"

# Batch mode (CSV with company_name, domain columns)
account-research "batch: ~/claude-work/research-assistant/inputs/accounts.csv"
```

---

### `account-question`
Answers any question about an account using Gong call transcripts and saved account files. Loads prior research and call history, answers the question, and saves output for future sessions.

**Triggers**: "what did we talk about with [company]", "what's going on with [account]", "draft an email for [account]", any question about calls/transcripts/deal status/pain points

**Usage**:
```
account-question "Iron Mountain — what are their pain points?"
account-question "BuildingMinds — draft a follow-up email"
account-question "Figure — what did we discuss in the last call?"
```

---

## Setup

### 1. Install the skills

```bash
mkdir -p ~/.claude/skills/account-research ~/.claude/skills/account-question
cp skills/account-research/SKILL.md ~/.claude/skills/account-research/SKILL.md
cp skills/account-question/SKILL.md ~/.claude/skills/account-question/SKILL.md
```

Restart Claude Code — the skills will appear automatically.

### 2. Set up the file structure

The skills expect this directory layout under `~/claude-work/`:

```
~/claude-work/
├── gong_account_transcripts.py        # Gong transcript script (see below)
├── gong-cache/                        # Auto-created by Gong script
│   └── all_calls/
│       └── calls.json                 # Global call index (~11MB)
└── research-assistant/
    ├── prompts/
    │   ├── 01_fit_scoring.md          # Fit scoring rubric ← copy from this repo
    │   └── 02_account_research.md     # AE brief template ← copy from this repo
    ├── inputs/
    │   └── accounts.csv               # Your batch input list (company_name, domain)
    └── outputs/
        └── accounts/
            └── <company_slug>/
                ├── report.md          # Generated per-company report
                └── interactions.md    # Email drafts, notes, follow-up actions
```

Set up the prompts directory:

```bash
mkdir -p ~/claude-work/research-assistant/prompts
cp prompts/01_fit_scoring.md ~/claude-work/research-assistant/prompts/
cp prompts/02_account_research.md ~/claude-work/research-assistant/prompts/
```

### 3. Set up the Gong transcript script

The skills call a local Python script to fetch Gong call transcripts. Get it from the [claude-work repo](https://github.com/joeykenney-cpu/claude-work/tree/main/Gong-transcript-search-skill) and place it at:

```
~/claude-work/gong_account_transcripts.py
```

Or symlink it:
```bash
ln -s ~/claude-work/Gong-transcript-search-skill/gong_account_transcripts.py ~/claude-work/gong_account_transcripts.py
```

### 4. Set required env vars

```bash
# Add to ~/.zshrc or ~/.bashrc
export APOLLO_API_KEY=your_key_here
```

Gong, Leadfeeder, Exa, and Common Room auth are managed via MCP server configs — no env vars needed for those.

---

## Data Sources

| Source | What it provides |
|--------|-----------------|
| **Exa AI** | Company research, orchestration/pipeline evidence, hiring signals, engineering blogs, product announcements, vendor case studies, job descriptions |
| **Leadfeeder** | astronomer.io website visit data — which pages, how often, how recently (account ID: 281783) |
| **Common Room** | Community contacts, recent activity, website visits from known contacts |
| **Gong** | Prior Astronomer call transcripts — pain points, objections, tech stack mentions, deal stage |

---

## Apollo Notes

- Reports are written to the `Account_Research` custom field (field ID: `6998b33edacda9000deb48ca`) using `typed_custom_fields` — the name-keyed `custom_fields` format silently ignores writes
- Account lookup uses name search + domain validation before writing — avoids writing to the wrong account (the `q_organization_domain` API parameter is unreliable)

---

## Batch Input Format

CSV with a header row:

```csv
company_name,domain
Acme Corp,acme.com
Beta Inc,betainc.io
```
