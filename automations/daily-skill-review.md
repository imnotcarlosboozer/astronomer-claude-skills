# Daily Skill Review

Daily cron that analyzes your Claude Code session history for skill usage patterns, auto-applies high-confidence skill description improvements, and surfaces a summary at the start of your next session.

## What it does

Every morning, the cron:
1. Parses all Claude Code session JSONL files from the last 26 hours (`extract_sessions.py`)
2. Detects friction signals — user corrections, re-asks, repeated messages
3. Maps tool usage to missed skill triggers (e.g., heavy Gong API use without `account-question` firing)
4. Runs `claude -p` to generate a structured review with skill optimization recommendations
5. Auto-applies description changes with confidence ≥ 0.85, backing up originals first
6. Appends new observations to a rolling `patterns.md` for cross-day memory
7. Writes an `inbox.md` summary that surfaces in your next Claude Code session

If no sessions are found, it writes a stub report and exits cleanly.

## What you get

**At the start of your next Claude Code session** — a one-line inbox notice with:
- How many skill descriptions were auto-updated overnight
- Top 3 priority actions from the review
- Link to the full report

**The full report** at `~/claude-work/skill-optimizer/reports/YYYY-MM-DD.md` includes:
- Skill usage summary with frequency counts
- Optimization opportunities — friction quotes tied to specific sessions
- Missed triggers — sessions where a skill should have fired but didn't
- New skill ideas — recurring tasks with no existing coverage
- Priority actions ranked by impact

## Setup

### 1. Copy the scripts

```bash
mkdir -p ~/claude-work/scripts
cp scripts/extract_sessions.py ~/claude-work/scripts/
cp scripts/apply_skill_updates.py ~/claude-work/scripts/
cp scripts/daily_skill_review.sh ~/claude-work/scripts/
cp scripts/session_start_hook.py ~/claude-work/scripts/
chmod +x ~/claude-work/scripts/daily_skill_review.sh
```

### 2. Register the daily cron

Add to your system crontab (this persists — no 7-day auto-expire):

```bash
crontab -e
```

Add this line:

```
53 8 * * * ~/claude-work/scripts/daily_skill_review.sh >> ~/claude-work/skill-optimizer/cron.log 2>&1
```

Adjust the time to whatever works for you. The script skips silently if it already ran today.

### 3. Register the session-start hook

Add a `UserPromptSubmit` hook to `~/.claude/settings.json`. This is what surfaces the inbox at the start of each session:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/claude-work/scripts/session_start_hook.py"
          }
        ]
      }
    ]
  }
}
```

> **Note**: Use the full absolute path to `session_start_hook.py` — tilde expansion is not guaranteed in hook config.

### 4. Update skill hints (optional)

Edit `extract_sessions.py` and add entries to `TOOL_TO_SKILL_HINTS` for any skills you've added:

```python
TOOL_TO_SKILL_HINTS = {
    "WebFetch": ["astro-docs"],
    "mcp__gong__": ["account-question", "demo-prep", "weekly-gong-review"],
    "mcp__apollo__": ["apollo-add-to-sequences"],
    # Add your own mappings here
}
```

This controls what "missed trigger" hints appear in the report when a skill should have fired but didn't.

### 5. Run it manually to verify

```bash
~/claude-work/scripts/daily_skill_review.sh
```

Check the output:

```bash
cat ~/claude-work/skill-optimizer/reports/$(date +%Y-%m-%d).md
```

## File layout

```
~/claude-work/skill-optimizer/
├── reports/          # Daily reports — one .md per day
├── backups/          # Skill backups before any auto-update, organized by date
│   └── YYYY-MM-DD/
│       └── <skill-name>/SKILL.md
├── patterns.md       # Rolling cross-day observations
├── inbox.md          # Current session-start summary (overwritten each run)
└── cron.log          # Cron output log
```

## Notes

- The cron uses `claude -p` (non-interactive mode) — Claude Code must be installed and authenticated
- Auto-updates only touch the `description` field in skill frontmatter — the skill body is never modified
- All auto-updates are backed up before applying. Restore with: `cp ~/claude-work/skill-optimizer/backups/<date>/<skill>/SKILL.md ~/.claude/skills/<skill>/SKILL.md`
- The session-start hook only fires once per day — the `.inbox_shown` sentinel prevents repeated injection
- `patterns.md` accumulates indefinitely. Trim it manually if it gets long (~50 bullets is plenty)
