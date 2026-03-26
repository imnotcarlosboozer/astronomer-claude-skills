#!/bin/bash
# Daily skill usage review — extracts recent Claude Code sessions and runs
# an AI analysis looking for skill optimization opportunities and gaps.
# Output saved to ~/claude-work/skill-optimizer/reports/YYYY-MM-DD.md
#
# Auto-adaptive loop:
#   1. Extract session data (extract_sessions.py)
#   2. Load patterns.md for cross-day memory
#   3. Run claude -p analysis (structured output with JSON update block)
#   4. Apply high-confidence skill description updates (apply_skill_updates.py)
#   5. Append new observations to patterns.md
#   6. Write inbox.md for session-start hook to surface
#
# Add to system crontab (crontab -e):
#   53 8 * * * /Users/joeykenney/claude-work/scripts/daily_skill_review.sh >> /Users/joeykenney/claude-work/skill-optimizer/cron.log 2>&1

set -e

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="$HOME/claude-work/skill-optimizer/reports"
OUTPUT_FILE="$OUTPUT_DIR/$DATE.md"
PATTERNS_FILE="$HOME/claude-work/skill-optimizer/patterns.md"
INBOX_FILE="$HOME/claude-work/skill-optimizer/inbox.md"
SCRIPT="$HOME/claude-work/scripts/extract_sessions.py"
APPLY_SCRIPT="$HOME/claude-work/scripts/apply_skill_updates.py"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$HOME/claude-work/skill-optimizer/backups"

# Skip if we already ran today
if [ -f "$OUTPUT_FILE" ]; then
  echo "[$DATE] Report already exists — skipping."
  exit 0
fi

echo "[$DATE] Extracting sessions..."
SESSION_DATA=$(python3 "$SCRIPT" 2>/dev/null)

if [ -z "$SESSION_DATA" ] || echo "$SESSION_DATA" | grep -q "No sessions found"; then
  echo "[$DATE] No sessions to analyze."
  printf "# Skill Review — %s\n\nNo sessions found in the last 26 hours." "$DATE" > "$OUTPUT_FILE"
  exit 0
fi

# Load cross-day patterns if they exist
PATTERNS_CONTEXT=""
if [ -f "$PATTERNS_FILE" ]; then
  PATTERNS_CONTEXT=$(cat "$PATTERNS_FILE")
fi

echo "[$DATE] Running analysis..."

PROMPT="You are reviewing Claude Code session data to help improve skill usage and identify gaps.

Today's date: $DATE

$([ -n "$PATTERNS_CONTEXT" ] && echo "## Cross-Day Patterns (from prior days)
$PATTERNS_CONTEXT

---
")
## Session Data (last 24 hours)
$SESSION_DATA

---

Produce a skill review report with these sections. Skip any section with nothing meaningful to report.

## Skill Usage Summary
Which skills were used, how many times, and for what purposes.

## Optimization Opportunities
For each skill invoked: any signs of friction, re-asks, corrections, or triggering in the wrong context? Quote the specific user message. Be concrete.

## Missed Skill Triggers
Sessions where no skill fired but one should have. For each: what was asked, which installed skill fits, and why it probably didn't trigger (description gap? unusual phrasing?).

## New Skill Ideas
Recurring tasks or question types with no existing skill coverage. For each idea: proposed name, one-liner, trigger phrases, what it would do.

## Priority Actions
Top 3 things to act on today, ranked by impact.

## Pattern Updates
2-3 bullet observations worth adding to the rolling patterns log. Be concise (one line each). Focus on durable patterns — not one-off events. Start each bullet with a date like [$DATE].

---

IMPORTANT: At the very end of your response, output a JSON block (and ONLY this block, no extra commentary after it) with any high-confidence skill description improvements you recommend. Use confidence 0.85-1.0 only for clear wins with strong evidence. Leave the updates array empty if nothing is high-confidence.

\`\`\`json
{
  \"updates\": [
    {
      \"skill\": \"skill-name\",
      \"field\": \"description\",
      \"new_value\": \"Full replacement description text\",
      \"confidence\": 0.9,
      \"reason\": \"One sentence explaining the evidence\"
    }
  ]
}
\`\`\`

Be direct and specific — this is a working doc, not a polished summary."

echo "$PROMPT" | claude -p --output-format text > "$OUTPUT_FILE" 2>/dev/null

echo "[$DATE] Report saved to $OUTPUT_FILE"

# Apply high-confidence updates
echo "[$DATE] Applying skill updates..."
python3 "$APPLY_SCRIPT" "$OUTPUT_FILE" 2>/dev/null | tee -a "$HOME/claude-work/skill-optimizer/cron.log" || true

# Extract pattern updates from the report and append to patterns.md
echo "[$DATE] Updating patterns..."
python3 - <<'PYEOF' "$OUTPUT_FILE" "$PATTERNS_FILE"
import sys
import re

report_path = sys.argv[1]
patterns_path = sys.argv[2]

with open(report_path, "r") as f:
    report = f.read()

# Find the "## Pattern Updates" section
match = re.search(r"## Pattern Updates\s*\n(.*?)(?=\n## |\Z)", report, re.DOTALL)
if not match:
    sys.exit(0)

new_bullets = match.group(1).strip()
if not new_bullets:
    sys.exit(0)

# Append to patterns.md (create if missing)
try:
    with open(patterns_path, "a") as f:
        f.write("\n" + new_bullets + "\n")
    print(f"Appended pattern updates to {patterns_path}")
except Exception as e:
    print(f"Failed to update patterns: {e}")
PYEOF

# Write inbox.md for session-start hook
echo "[$DATE] Writing inbox..."
python3 - <<'PYEOF' "$OUTPUT_FILE" "$INBOX_FILE" "$DATE"
import sys
import re
import os

report_path = sys.argv[1]
inbox_path = sys.argv[2]
date_str = sys.argv[3]

with open(report_path, "r") as f:
    report = f.read()

# Extract Priority Actions
actions_match = re.search(r"## Priority Actions\s*\n(.*?)(?=\n## |\Z)", report, re.DOTALL)
actions = actions_match.group(1).strip() if actions_match else "No priority actions."

# Check if any skill updates were applied
applied_count = 0
log_path = os.path.expanduser("~/claude-work/skill-optimizer/cron.log")
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        log = f.read()
    applied_count = log.count("APPLIED")

lines = [f"# Skill Review Inbox — {date_str}", ""]
if applied_count:
    lines.append(f"**{applied_count} skill description(s) auto-updated overnight.** Backups in `~/claude-work/skill-optimizer/backups/{date_str}/`.")
    lines.append("")
lines.append("**Priority actions from overnight review:**")
lines.append(actions)
lines.append("")
lines.append(f"Full report: `~/claude-work/skill-optimizer/reports/{date_str}.md`")

with open(inbox_path, "w") as f:
    f.write("\n".join(lines))

print(f"Inbox written to {inbox_path}")
PYEOF

echo "[$DATE] Done."
