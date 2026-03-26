#!/usr/bin/env python3
"""
Parse structured claude -p output from daily_skill_review.sh and auto-apply
high-confidence skill description updates. Backs up before any change.

Input format expected in the report (fenced JSON block):
```json
{
  "updates": [
    {
      "skill": "account-question",
      "field": "description",
      "new_value": "...",
      "confidence": 0.9,
      "reason": "Triggers missed when user says 'how is the relationship with X'"
    }
  ]
}
```

Only applies updates with confidence >= 0.85. Lower confidence items are
left in the report for the user to action manually.

Usage:
  python3 apply_skill_updates.py <report_file>
"""

import json
import os
import re
import sys
import shutil
from datetime import datetime
from pathlib import Path

SKILLS_DIR = os.path.expanduser("~/.claude/skills/")
BACKUP_DIR = os.path.expanduser("~/claude-work/skill-optimizer/backups/")
CONFIDENCE_THRESHOLD = 0.85


def extract_json_block(text):
    """Extract the first ```json ... ``` block from text."""
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def backup_skill(skill_name):
    """Back up the skill's SKILL.md before modifying it."""
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_path):
        return None

    date_str = datetime.now().strftime("%Y-%m-%d")
    backup_dir = os.path.join(BACKUP_DIR, date_str, skill_name)
    os.makedirs(backup_dir, exist_ok=True)

    dest = os.path.join(backup_dir, "SKILL.md")
    shutil.copy2(skill_path, dest)
    return dest


def apply_description_update(skill_name, new_description):
    """Replace the description field in the YAML frontmatter of SKILL.md."""
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_path):
        print(f"  SKIP: skill '{skill_name}' not found at {skill_path}")
        return False

    with open(skill_path, "r") as f:
        content = f.read()

    # Match the description field in YAML frontmatter (handles multi-line values)
    # The frontmatter is between the first two --- delimiters
    frontmatter_match = re.match(r"^(---\s*\n)(.*?)(---\s*\n)", content, re.DOTALL)
    if not frontmatter_match:
        print(f"  SKIP: could not parse frontmatter in {skill_path}")
        return False

    pre, frontmatter, post_delim = frontmatter_match.groups()
    rest_of_file = content[frontmatter_match.end():]

    # Replace description field — handles single-line and quoted multi-line
    # Strategy: replace from 'description:' to next key or end of frontmatter
    new_desc_escaped = new_description.replace("\n", "\n  ")
    new_frontmatter = re.sub(
        r"(^description:\s*)(.+?)(\n(?=\S)|\Z)",
        lambda m: f"description: |\n  {new_desc_escaped}\n",
        frontmatter,
        flags=re.DOTALL | re.MULTILINE,
    )

    if new_frontmatter == frontmatter:
        # description key not found — append it
        new_frontmatter = frontmatter.rstrip("\n") + f"\ndescription: |\n  {new_desc_escaped}\n"

    new_content = pre + new_frontmatter + post_delim + rest_of_file
    with open(skill_path, "w") as f:
        f.write(new_content)

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: apply_skill_updates.py <report_file>")
        sys.exit(1)

    report_path = sys.argv[1]
    if not os.path.exists(report_path):
        print(f"Report not found: {report_path}")
        sys.exit(1)

    with open(report_path, "r") as f:
        report_text = f.read()

    json_str = extract_json_block(report_text)
    if not json_str:
        print("No JSON update block found in report — nothing to apply.")
        sys.exit(0)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON block: {e}")
        sys.exit(1)

    updates = data.get("updates", [])
    if not updates:
        print("No updates in JSON block.")
        sys.exit(0)

    applied = []
    skipped = []

    for update in updates:
        skill = update.get("skill", "")
        field = update.get("field", "")
        new_value = update.get("new_value", "")
        confidence = float(update.get("confidence", 0))
        reason = update.get("reason", "")

        if not skill or not new_value:
            continue

        if confidence < CONFIDENCE_THRESHOLD:
            skipped.append(f"  LOW CONFIDENCE ({confidence:.2f}): {skill} — {reason}")
            continue

        if field != "description":
            skipped.append(f"  UNSUPPORTED FIELD: {field} for {skill}")
            continue

        backup_dest = backup_skill(skill)
        if not backup_dest:
            skipped.append(f"  SKIP (not installed): {skill}")
            continue

        success = apply_description_update(skill, new_value)
        if success:
            applied.append(f"  APPLIED ({confidence:.2f}): {skill} — {reason}")
            applied.append(f"    Backup: {backup_dest}")
        else:
            skipped.append(f"  FAILED: {skill}")

    if applied:
        print("=== Applied Updates ===")
        for line in applied:
            print(line)

    if skipped:
        print("\n=== Skipped (manual review needed) ===")
        for line in skipped:
            print(line)

    if not applied and not skipped:
        print("No actionable updates found.")


if __name__ == "__main__":
    main()
