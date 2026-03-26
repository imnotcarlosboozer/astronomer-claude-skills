#!/usr/bin/env python3
"""
UserPromptSubmit hook — surfaces the skill review inbox once per day.

Prints a system prompt injection if:
  - inbox.md exists and has content
  - It hasn't been shown yet today (tracked via a .shown sentinel file)

The output is injected into the context as a system message before Claude sees
the user's first prompt of the session.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

INBOX_FILE = os.path.expanduser("~/claude-work/skill-optimizer/inbox.md")
SHOWN_SENTINEL = os.path.expanduser("~/claude-work/skill-optimizer/.inbox_shown")


def already_shown_today():
    if not os.path.exists(SHOWN_SENTINEL):
        return False
    sentinel_mtime = datetime.fromtimestamp(os.path.getmtime(SHOWN_SENTINEL))
    return sentinel_mtime.date() == datetime.now().date()


def mark_shown():
    Path(SHOWN_SENTINEL).touch()


def main():
    if already_shown_today():
        sys.exit(0)

    if not os.path.exists(INBOX_FILE):
        sys.exit(0)

    with open(INBOX_FILE, "r") as f:
        inbox = f.read().strip()

    if not inbox:
        sys.exit(0)

    # Print injection — Claude Code hook stdout is injected as context
    print("\n---")
    print("**Overnight skill review is ready:**")
    print(inbox)
    print("---\n")

    mark_shown()


if __name__ == "__main__":
    main()
