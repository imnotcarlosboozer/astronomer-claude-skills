# Astronomer Claude Code Skills

Claude Code skills for the Astronomer sales team. Research accounts, review call history, and get weekly coaching reports — all from within Claude Code.

## Getting started

Clone the repo, open Claude Code from the repo root, and run:

```
/setup
```

Claude will detect what is already configured, fetch account IDs and field IDs automatically from your APIs, and only ask you for credentials it cannot derive itself. You will need: Gong API keys, Apollo API key, and optionally a Leadfeeder API token.

---

## Contents

| Skill | What it does |
|-------|-------------|
| [`setup`](#setup-skill) | First-time setup — installs all skills, configures credentials, auto-derives account IDs |
| [`account-research`](#account-research) | Research any company for Astronomer fit — scored AE brief, tech stack, hiring signals, buying intent, and more |
| [`account-question`](#account-question) | Ask anything about an account using Gong transcripts and saved research |
| [`demo-prep`](#demo-prep) | Generate a ready-to-share SE demo prep brief from Gong call transcripts — attendees, current state, tech stack, use cases, etc. |
| [`weekly-gong-review`](#weekly-gong-review) | Weekly call coaching report — scorecard, highlights, patterns, deep links to exact timestamps |
| [`quarterly-pipeline-report`](#quarterly-pipeline-report) | Generate quarterly pipeline report with Gong transcripts and research for each account |
| [`apollo-add-to-sequences`](#apollo-add-to-sequences) | Add prospects from a CSV to Apollo sequences with auto contact enrichment and sequence activation |
| [`astro-docs`](#astro-docs) | Answer any Astronomer/Astro product question by searching and fetching live from astronomer.io and the official docs |
| [`snowflake-query`](#snowflake-query) | Query Astronomer's Snowflake warehouse efficiently — full table map, join patterns, and optimization rules baked in. Self-improving via daily cron. |

> Contributing? See [CONTRIBUTING.md](CONTRIBUTING.md) for the sanitization checklist, placeholder reference, and PR standards.

---

## Automations

| Automation | What it does |
|------------|-------------|
| [`notion-todo-sync`](automations/notion-todo-sync.md) | Hourly cron — pulls your action items from new Gong calls and appends them to a Notion database |
| [`daily-skill-review`](automations/daily-skill-review.md) | Daily cron — reviews skill usage from recent sessions, auto-updates skill descriptions, surfaces a summary at next session start |

---

## Skills

### `setup`

First-time setup for all skills. Run this once when you clone the repo on a new machine.

**Run it**: open Claude Code from the repo root and type `/setup`

Claude will:
- Check which credentials and MCP servers are already configured
- Ask only for credentials it cannot derive (Gong API keys, Apollo API key, Leadfeeder token)
- Auto-fetch your Leadfeeder account ID and Apollo field ID from the APIs — no manual lookup
- Install all skill files, scripts, and prompt templates
- Patch installed skills with your real account IDs (repo copies keep placeholders)
- Sync the Gong call cache
- Print a status summary showing what is working

**Requires**: Claude Code + this repo cloned locally. Everything else is set up for you.

---

### `account-research`
Research any company for Astronomer fit. Pulls data from Exa, Leadfeeder, Common Room, and Gong, then generates a scored AE brief and syncs it to Apollo.

**Run it**: type naturally — `"research Acme Corp, acme.com"` or `"score this account"`

**Output**: Fit score (0–20, letter grade A–D), full AE brief with tech stack, hiring signals, pain points, contacts, prior Gong conversations, website engagement, and outreach hooks. Saves to `~/claude-work/research-assistant/outputs/accounts/` and syncs to Apollo.

```
# Single company
account-research "Acme Corp, acme.com"

# Batch (CSV with company_name, domain columns)
account-research "batch: ~/claude-work/research-assistant/inputs/accounts.csv"
```

**Requires**: Claude Code + at least one data source connected (see [Setup](#setup-account-research))

---

### `account-question`
Ask anything about an account using Gong transcripts and saved research. Answers questions, drafts emails, and saves output for future sessions.

**Run it**: ask naturally — `"what did we discuss with Acme Corp?"` or `"draft a follow-up for Beta Inc"`

```
account-question "Acme Corp — what are their pain points?"
account-question "Beta Inc — draft a follow-up email"
account-question "Gamma LLC — what did we discuss in the last call?"
```

**Requires**: Claude Code + Gong transcript script (see [Setup](#setup-account-question))

---

### `demo-prep`
Generate a ready-to-share demo prep brief for a sales engineer. Pulls every Gong call for the account and synthesizes them into a structured doc grounded entirely in what the customer actually said.

**Run it**: type naturally — `"prep the SE for the Acme Corp demo"` or `/demo-prep Acme Corp`

**Output**: Who's on the call (with what each person cares about) · Current state · Tech stack (from transcripts only) · Data products and business use cases · What the champion specifically asked to see · What the technical evaluator cares about · Suggested demo flow with time allocations · Things to watch for. Saves to `~/claude-work/research-assistant/outputs/accounts/<account>/interactions.md`.

```
/demo-prep Acme Corp
prep the SE for the Beta Inc demo
```

**Requires**: Claude Code + Gong transcript script (see [Setup](#setup-demo-prep))

---

### `weekly-gong-review`
Weekly call coaching report for an AE. Pulls every call they appeared on (not just ones they hosted), scores 6 dimensions, and links every coaching point to the exact timestamp in the recording.

**Run it**: `/weekly-gong-review`

**Output**: Scorecard (6 dimensions, 1–5, week-over-week trend) · One Thing to Focus On · This Week's Highlight · Cross-Call Patterns · Call-by-Call with exact quotes, deep links, and "Try instead" reframes · Score history

```
/weekly-gong-review                              # current week
/weekly-gong-review week:2026-W09               # specific week
/weekly-gong-review rep:"Jane Smith"            # different rep
/weekly-gong-review rep:user@astronomer.io
```

**Requires**: Claude Code + Gong API credentials (see [Setup](#setup-weekly-gong-review))

---

### `quarterly-pipeline-report`
Generate a comprehensive quarterly pipeline report with Gong call transcripts and existing research for each account in your pipeline.

**Run it**: `/quarterly-pipeline-report` or type naturally — `"generate Q1 2026 pipeline report"` or `"quarterly pipeline for Vishwa"`

**Output**: Pipeline opportunities table (filtered by rep and quarter) · Gong transcripts for each account (filtered to quarter dates) · Existing research reports copied to pipeline folder · Stage breakdown with total pipeline value · Top accounts by call volume

```
/quarterly-pipeline-report                      # defaults to Vishwa, current quarter
quarterly-pipeline-report "Q1 2026"            # specific quarter
quarterly-pipeline-report "Vishwa Q2 2026"     # specific rep and quarter
```

Output is organized at `~/Account Context/Q{N}_{YEAR}_Pipeline/` with:
- Main pipeline report with opportunities table
- Per-account folders with Gong transcripts (quarter-filtered)
- Existing research files copied from `~/Account Context/[Company]/`

**Fiscal quarters** (default): Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan

**Requires**: Claude Code + Gong cache synced (see [Setup](#setup-quarterly-pipeline-report))

---

## Setup

Jump to the skill you want to use:

- [account-research](#setup-account-research)
- [account-question](#setup-account-question)
- [demo-prep](#setup-demo-prep)
- [weekly-gong-review](#setup-weekly-gong-review)
- [quarterly-pipeline-report](#setup-quarterly-pipeline-report)
- [apollo-add-to-sequences](#setup-apollo-add-to-sequences)
- [astro-docs](#setup-astro-docs)

---

### Setup: demo-prep

This skill only needs the Gong transcript script — no additional MCP servers required beyond what `account-question` already uses.

**1. Install the skill**

```bash
mkdir -p ~/.claude/skills/demo-prep
cp skills/demo-prep/SKILL.md ~/.claude/skills/demo-prep/SKILL.md
```

Restart Claude Code.

**2. Set up the Gong transcript script** (skip if already done for `account-question`)

```bash
pip install requests python-dateutil
cp gong_account_transcripts.py ~/claude-work/gong_account_transcripts.py
```

**3. Add Gong API credentials** (skip if already done)

```bash
# Add to ~/.zshrc or ~/.bash_profile
export GONG_ACCESS_KEY=your_access_key
export GONG_SECRET_KEY=your_secret_key
```

**4. Run it**

```
/demo-prep Acme Corp
```

Claude will fetch all Gong calls for the account, read the transcripts, and produce a structured brief. Output is displayed in the conversation and saved to:

```
~/claude-work/research-assistant/outputs/accounts/<account>/interactions.md
```

---

### Setup: weekly-gong-review

This skill only needs Gong API credentials — no MCP servers required.

**1. Install the skill**

```bash
mkdir -p ~/.claude/skills/weekly-gong-review
cp skills/weekly-gong-review/SKILL.md ~/.claude/skills/weekly-gong-review/SKILL.md
```

Restart Claude Code.

**2. Add Gong API credentials**

Get your Access Key and Secret Key from Gong: **Settings → API → Access Keys**

```bash
# Add to ~/.zshrc or ~/.bash_profile
export GONG_ACCESS_KEY=your_access_key
export GONG_SECRET_KEY=your_secret_key
```

```bash
source ~/.zshrc
```

**3. Run it**

```
/weekly-gong-review
```

Claude will prompt for the rep's Astronomer email on first run, look up their Gong user ID, and cache it. Subsequent runs start immediately.

---

### Setup: account-question

**1. Install the skill**

```bash
mkdir -p ~/.claude/skills/account-question
cp skills/account-question/SKILL.md ~/.claude/skills/account-question/SKILL.md
```

Restart Claude Code.

**2. Set up the Gong transcript script**

```bash
# Install dependencies
pip install requests python-dateutil

# Place the script
cp gong_account_transcripts.py ~/claude-work/gong_account_transcripts.py
```

**3. Add Gong API credentials** (skip if already done for weekly-gong-review)

```bash
# Add to ~/.zshrc or ~/.bash_profile
export GONG_ACCESS_KEY=your_access_key
export GONG_SECRET_KEY=your_secret_key
```

**4. Run it**

```
account-question "Acme Corp — what are their pain points?"
```

---

### Setup: account-research

This skill works with any combination of data sources. Start with just web search and add connections as you get access.

| Source | What it adds | Required? |
|--------|-------------|-----------|
| Claude web search | Company overview, hiring signals, tech stack, news | Built-in — always on |
| **Gong** | Prior call history, pain points, objections, deal stage | Recommended |
| **Leadfeeder** | astronomer.io visit data — which pages, how recently | Recommended |
| **Apollo** | Writes report back to `Account_Research` field in CRM | Recommended |
| Common Room | Known contacts, community activity | Optional |
| Exa AI | More targeted web search with date filtering | Optional |

**1. Install the skill**

```bash
mkdir -p ~/.claude/skills/account-research
cp skills/account-research/SKILL.md ~/.claude/skills/account-research/SKILL.md
```

Also copy the prompt templates:

```bash
mkdir -p ~/claude-work/research-assistant/prompts
cp prompts/01_fit_scoring.md ~/claude-work/research-assistant/prompts/
cp prompts/02_account_research.md ~/claude-work/research-assistant/prompts/
```

Restart Claude Code.

**2. Connect data sources**

Set up whichever ones you have access to:

<details>
<summary><strong>Gong</strong></summary>

```bash
claude mcp add --transport http gong https://mcp.gong.io/mcp
```

Also set up the Gong transcript script (same as account-question setup above).

</details>

<details>
<summary><strong>Apollo</strong></summary>

```bash
claude mcp add --transport http apollo https://mcp.apollo.io/mcp
```

```bash
# Add to ~/.zshrc or ~/.bash_profile
export APOLLO_API_KEY=your_apollo_api_key
```

</details>

<details>
<summary><strong>Leadfeeder</strong></summary>

1. Get your API token from Leadfeeder → Settings → API Tokens
2. Place the MCP server from `mcp-servers/leadfeeder/` in this repo:

```bash
mkdir -p ~/.claude/mcp-servers/leadfeeder
cp mcp-servers/leadfeeder/index.js ~/.claude/mcp-servers/leadfeeder/
cd ~/.claude/mcp-servers/leadfeeder && npm install
```

3. Register it:

```bash
claude mcp add leadfeeder --scope user \
  -e LEADFEEDER_API_TOKEN=your_token \
  -- node ~/.claude/mcp-servers/leadfeeder/index.js
```

</details>

<details>
<summary><strong>Common Room (optional)</strong></summary>

```bash
claude mcp add --transport http commonroom https://mcp.commonroom.io/mcp
```

</details>

<details>
<summary><strong>Exa AI (optional)</strong></summary>

```bash
npm install -g exa-mcp-server
claude mcp add --transport stdio exa -- npx exa-mcp-server
```

```bash
# Add to ~/.zshrc or ~/.bash_profile
export EXA_API_KEY=your_exa_api_key
```

</details>

**3. Verify connections**

```bash
claude mcp list
```

**4. Create your account list** (for batch mode)

Export from Salesforce: Reports → New Report → Accounts → add Account Name + Website → Export CSV. Save it as:

```
~/claude-work/research-assistant/inputs/accounts.csv
```

The file needs two columns:

```csv
company_name,domain
Acme Corp,acme.com
Beta Inc,betainc.io
```

**5. Run it**

```
account-research "Acme Corp, acme.com"
account-research "batch: ~/claude-work/research-assistant/inputs/accounts.csv"
```

Reports save to `~/claude-work/research-assistant/outputs/accounts/<company>/report.md` and sync to Apollo automatically.

---

### Setup: quarterly-pipeline-report

This skill pulls pipeline data from Gong's Salesforce integration and generates per-account context.

**1. Install the skill**

```bash
mkdir -p ~/.claude/skills/quarterly-pipeline-report
cp skills/quarterly-pipeline-report/SKILL.md ~/.claude/skills/quarterly-pipeline-report/SKILL.md
```

Copy the pipeline script to your Scripts folder:

```bash
mkdir -p ~/Scripts
cp scripts/quarterly_pipeline_context.py ~/Scripts/
chmod +x ~/Scripts/quarterly_pipeline_context.py
```

Restart Claude Code.

**2. Set up the Gong transcript script** (skip if already done for `account-question`)

```bash
pip install requests python-dateutil
cp gong_account_transcripts.py ~/claude-work/gong_account_transcripts.py
```

**3. Add Gong API credentials** (skip if already done)

```bash
# Add to ~/.zshrc or ~/.bash_profile
export GONG_ACCESS_KEY=your_access_key
export GONG_SECRET_KEY=your_secret_key
```

```bash
source ~/.zshrc
```

**4. Sync the Gong cache**

The skill uses a cached index of all Gong calls for fast filtering. Sync it once:

```bash
python3 ~/claude-work/gong_account_transcripts.py --sync
```

This creates `~/claude-work/gong-cache/all_calls/calls.json` with all call metadata.

**Optional**: Set up daily sync (recommended for large Gong instances):

```bash
# crontab -e
0 6 * * * python3 ~/claude-work/gong_account_transcripts.py --sync
```

**5. Update rep email mapping** (if using for multiple reps)

Edit `~/Scripts/quarterly_pipeline_context.py` and add entries to `REP_EMAIL_MAP`:

```python
REP_EMAIL_MAP = {
    "vishwa": "user@astronomer.io",
    "alec": "user@astronomer.io",
    # Add more reps here
}
```

**6. Run it**

```
/quarterly-pipeline-report
quarterly-pipeline-report "Q1 2026"
quarterly-pipeline-report "Vishwa Q2 2026"
```

Or run the script directly:

```bash
python3 ~/Scripts/quarterly_pipeline_context.py --rep "Vishwa" --quarter "Q1 2026" --fiscal
```

Output location: `~/Account Context/Q{N}_{YEAR}_Pipeline/`

---

### `astro-docs`
Answer any question about how Astronomer or Astro works by searching and fetching live from astronomer.io and the official docs. Always fetches live — never answers from training data, since the product changes frequently.

**Run it**: ask naturally — `"how does hibernation work in Astro?"`, `"what's the difference between a standard and dedicated cluster?"`, `"does Astro support SSO enforcement?"`

**Output**: Direct answer grounded in the current docs, with source URLs so the user can read further.

**Requires**: No additional setup — uses built-in WebFetch and Exa search tools (Exa optional; falls back to WebFetch-only if not configured)

---

### `apollo-add-to-sequences`
Add prospects from a CSV to Apollo sequences with automatic contact enrichment and sequence activation. Supports 800+ sequences via pagination, webinar ATTENDED/NO SHOW routing, and auto-activation after enrollment.

**Run it**: mention a CSV path — `"~/Downloads/report.csv add these to apollo sequences"`

**Output**: Enrolls contacts, creates missing records via Apollo enrichment, activates sequences, and prints a summary with any contacts needing manual intervention.

```
~/Downloads/report.csv add these to apollo sequences
add contacts from ~/Downloads/outreach.csv to sequences
```

**CSV format**: `First Name`, `Last Name`, `Email`, `Recommended Outreach Sequence`, `Last Activity` (optional)

**Requires**: `APOLLO_API_KEY` env var + `pip install requests` (see [Setup](#setup-apollo-add-to-sequences))

---

### Setup: astro-docs

No external credentials or MCP servers required. The skill uses WebFetch (built-in) to fetch live pages from astronomer.io. If the Exa MCP is configured, it will use Exa search first to find the most relevant doc pages before fetching.

**1. Install the skill**

```bash
mkdir -p ~/.claude/skills/astro-docs
cp skills/astro-docs/SKILL.md ~/.claude/skills/astro-docs/SKILL.md
```

Restart Claude Code.

**2. Run it**

```
how does hibernation work in Astro?
what's the difference between a standard and dedicated cluster?
does Astro support SSO enforcement — which tier requires it?
```

Claude will search astronomer.io and the docs, fetch the relevant pages, and answer with source URLs.

---

### Setup: apollo-add-to-sequences

**1. Install the skill**

```bash
mkdir -p ~/.claude/skills/apollo-add-to-sequences
cp skills/apollo-add-to-sequences/SKILL.md ~/.claude/skills/apollo-add-to-sequences/SKILL.md
```

Restart Claude Code.

**2. Copy the script**

```bash
mkdir -p ~/claude-work/scripts
cp scripts/add_to_apollo_sequences.py ~/claude-work/scripts/
cp scripts/apollo_config.py ~/claude-work/scripts/
```

**3. Install dependencies**

```bash
pip install requests
```

**4. Set your Apollo API key**

```bash
# Add to ~/.zshrc or ~/.bash_profile
export APOLLO_API_KEY=your_apollo_api_key
```

```bash
source ~/.zshrc
```

**5. Run it**

```
~/Downloads/report.csv add these to apollo sequences
```

Or directly:

```bash
cd ~/claude-work/scripts
python3 add_to_apollo_sequences.py ~/Downloads/report.csv
```

---

## Technical Notes

<details>
<summary>Apollo integration details</summary>

- Reports write to the `Account_Research` custom field (field ID: `{YOUR_APOLLO_FIELD_ID}`) using `typed_custom_fields` — the name-keyed `custom_fields` format silently ignores writes
- Account lookup uses name search + domain validation to avoid writing to the wrong record

</details>

<details>
<summary>Gong transcript cache</summary>

The transcript script uses a two-tier cache:
1. **Global index** at `~/claude-work/gong-cache/all_calls/calls.json` — slim records synced incrementally on each query
2. **Per-account transcripts** — full text fetched and cached separately per account

Optional daily sync cron (recommended for large Gong instances):

```bash
# crontab -e
0 6 * * * python3 ~/claude-work/gong_account_transcripts.py --sync
```

</details>

<details>
<summary>QMD semantic search integration</summary>

**What**: QMD indexes Gong transcript markdown files and research reports for fast semantic search. Used by `account-question` to surface relevant transcript passages without loading everything, and to enable cross-account queries like "which accounts mentioned Dagster as a competitor?".

**Where it's used**: `account-question` automatically checks QMD before falling back to the transcript script. If QMD is not set up, the skill works normally — it just uses the script path.

**Setup**:

1. **Install QMD MCP server** — add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "qmd": {
      "command": "npx",
      "args": ["-y", "@tobilu/qmd", "mcp"]
    }
  }
}
```

2. **Copy the conversion script**:
```bash
cp gong_json_to_markdown.py ~/claude-work/gong_json_to_markdown.py
```

3. **Convert existing transcripts to markdown**:
```bash
python3 ~/claude-work/gong_json_to_markdown.py --all
```

4. **Index in QMD and generate embeddings**:
```bash
cd ~/claude-work
npx -y @tobilu/qmd update gong
npx -y @tobilu/qmd embed
```

5. **Verify**:
```bash
npx -y @tobilu/qmd query "data orchestration pain points" -c gong
```

**Cross-account queries** (from CLI):
```bash
npx -y @tobilu/qmd query "accounts discussing Dagster as competitor" -c gong
npx -y @tobilu/qmd query "MWAA migration concerns" -c gong
```

**Automated sync** — add to your daily Gong cron so the index stays fresh:
```bash
# crontab -e
0 6 * * * cd ~/claude-work && python3 gong_account_transcripts.py --sync && python3 gong_json_to_markdown.py --sync && npx -y @tobilu/qmd update gong
```

**Architecture**: JSON remains the source of truth. Markdown files are generated alongside JSON and tracked via `metadata.json` timestamps — stale files are auto-detected on `--sync`. See [docs/qmd-integration-plan.md](docs/qmd-integration-plan.md) for full details.

</details>

<details>
<summary>Leadfeeder cache</summary>

Both `account-research` (single and batch) and subagents share a 24-hour disk cache at `~/claude-work/leadfeeder-cache/leads.json`. On a cache hit, the full Leadfeeder leads list is read from disk — no API pagination needed. Cache is populated automatically on first run (or when stale) and updated in place.

This means repeated single-company runs within a day skip the 5-page Leadfeeder pagination entirely.

</details>

---

### `snowflake-query`

Query Astronomer's Snowflake data warehouse efficiently. Knows the full HQ database schema, join patterns, and optimization rules — writes correct queries on the first try without schema exploration.

**Invoke it**: ask any question requiring Snowflake data — `"how much did Pulumi spend yesterday"`, `"show me all users for Huli"`, `"which accounts are over 80% credit utilization"`

**What's baked in:**
- Full table map across `IN_*`, `MODEL_*`, `METRICS_*`, and `MART_*` schemas
- Standard join patterns (account lookup → metrics, users for account, usage vs. contract)
- `*_MULTI` table rules (always filter `TIME_GRAIN` + `DATE`)
- Anti-patterns for the largest tables (7.4B-row `TASK_RUNS`, etc.)
- Self-updating: daily cron appends learned patterns from actual query history

**Setup**: Requires Snowflake MCP server + RSA key pair auth configured (included in `/setup`).

**Self-improvement**: A daily cron at 8:17 AM reviews query history from the past 24 hours, extracts new patterns and corrections, and appends them to the `Learned Patterns Log` section. If anything meaningful changed, it auto-commits and pushes.
