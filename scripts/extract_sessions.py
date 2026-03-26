#!/usr/bin/env python3
"""
Extract Claude Code session data for skill usage analysis.
Detects skill invocations, friction signals, and tool patterns.
Outputs structured text for piping to claude -p.
"""

import json
import os
import sys
import glob
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

HOURS_BACK = int(os.environ.get("HOURS_BACK", "26"))
PROJECTS_DIR = os.path.expanduser("~/.claude/projects/")
INSTALLED_SKILLS_DIR = os.path.expanduser("~/.claude/skills/")

# Phrases that signal the user was unhappy with a result or had to redirect
FRICTION_PATTERNS = [
    r"\btry again\b",
    r"\bthat('s| is) (wrong|incorrect|not right|off)\b",
    r"\bno,?\s+(that|this|it)\b",
    r"\bactually,?\s+(can you|could you|please|just)\b",
    r"\bcan you (redo|redo|fix|correct|re-?do|re-?run)\b",
    r"\bthat didn'?t (work|help)\b",
    r"\bnot what I (want|need|meant|asked)\b",
    r"\bignore (that|the last)\b",
    r"\bstart over\b",
    r"\blet'?s try\b",
]

# Tools that suggest a skill SHOULD have fired but didn't
TOOL_TO_SKILL_HINTS = {
    "WebFetch": ["astro-docs"],
    "mcp__gong__": ["account-question", "demo-prep", "weekly-gong-review"],
    "mcp__apollo__": ["apollo-add-to-sequences"],
}


def get_installed_skills():
    if not os.path.exists(INSTALLED_SKILLS_DIR):
        return []
    return sorted([
        d for d in os.listdir(INSTALLED_SKILLS_DIR)
        if os.path.isdir(os.path.join(INSTALLED_SKILLS_DIR, d))
        and not d.endswith("-workspace")
        and not d.endswith("-snapshot")
    ])


def detect_friction(text):
    """Return matched friction patterns in a user message."""
    text_lower = text.lower()
    return [p for p in FRICTION_PATTERNS if re.search(p, text_lower)]


def parse_session_file(filepath):
    """Parse a JSONL session file and extract structured data."""
    user_messages = []
    skills_used = []
    tools_used = []
    friction_events = []
    prev_user_text = None

    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg = obj.get("message", obj)
                role = msg.get("role")
                if not role:
                    continue

                content = msg.get("content", "")

                if isinstance(content, list):
                    for item in content:
                        if not isinstance(item, dict):
                            continue
                        item_type = item.get("type", "")

                        if item_type == "text" and role == "user":
                            text = item.get("text", "").strip()
                            # Skip system injections
                            if text and not text.startswith("<") and len(text) > 5:
                                user_messages.append(text[:600])
                                # Check for friction
                                friction = detect_friction(text)
                                if friction:
                                    friction_events.append({
                                        "message": text[:300],
                                        "patterns": friction,
                                        "prev_context": prev_user_text[:200] if prev_user_text else None
                                    })
                                # Detect near-duplicate re-asks
                                if prev_user_text and similarity_score(text, prev_user_text) > 0.7:
                                    friction_events.append({
                                        "message": text[:300],
                                        "patterns": ["repeated_message"],
                                        "prev_context": prev_user_text[:200]
                                    })
                                prev_user_text = text

                        elif item_type == "tool_use":
                            tool_name = item.get("name", "")
                            tool_input = item.get("input", {})

                            if tool_name == "Skill":
                                skill_name = tool_input.get("skill", "")
                                skill_args = str(tool_input.get("args", ""))[:300]
                                if skill_name:
                                    skills_used.append({
                                        "skill": skill_name,
                                        "args": skill_args,
                                    })
                            elif tool_name:
                                tools_used.append(tool_name)

                elif isinstance(content, str) and role == "user":
                    text = content.strip()
                    if text and not text.startswith("<") and len(text) > 5:
                        user_messages.append(text[:600])
                        friction = detect_friction(text)
                        if friction:
                            friction_events.append({
                                "message": text[:300],
                                "patterns": friction,
                                "prev_context": prev_user_text[:200] if prev_user_text else None
                            })
                        prev_user_text = text

    except Exception:
        pass

    # Deduplicate tools
    tool_counts = defaultdict(int)
    for t in tools_used:
        tool_counts[t] += 1

    # Detect tool patterns that hint at missed skill triggers
    missed_hints = []
    tool_names_str = " ".join(tools_used)
    for tool_prefix, candidate_skills in TOOL_TO_SKILL_HINTS.items():
        if tool_prefix in tool_names_str:
            for cs in candidate_skills:
                already_used = any(s["skill"] == cs for s in skills_used)
                if not already_used:
                    missed_hints.append({
                        "tool_signal": tool_prefix,
                        "candidate_skill": cs
                    })

    return {
        "user_messages": user_messages,
        "skills_used": skills_used,
        "tools_used": dict(tool_counts),
        "friction_events": friction_events,
        "missed_hints": missed_hints,
    }


def similarity_score(a, b):
    """Rough word-overlap similarity between two strings."""
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    if not a_words or not b_words:
        return 0
    return len(a_words & b_words) / max(len(a_words), len(b_words))


def get_recent_sessions(hours_back):
    cutoff = datetime.now() - timedelta(hours=hours_back)
    sessions = []
    for jsonl_file in glob.glob(os.path.join(PROJECTS_DIR, "**/*.jsonl"), recursive=True):
        mtime = datetime.fromtimestamp(os.path.getmtime(jsonl_file))
        if mtime >= cutoff:
            sessions.append((jsonl_file, mtime))
    sessions.sort(key=lambda x: x[1], reverse=True)
    return sessions


def main():
    installed_skills = get_installed_skills()
    recent_sessions = get_recent_sessions(HOURS_BACK)

    if not recent_sessions:
        print(f"No sessions found in the last {HOURS_BACK} hours.")
        sys.exit(0)

    summaries = []
    for filepath, mtime in recent_sessions:
        data = parse_session_file(filepath)
        if not data["user_messages"]:
            continue
        summaries.append({
            "session_id": Path(filepath).stem[:8],
            "time": mtime.strftime("%Y-%m-%d %H:%M"),
            **data
        })

    if not summaries:
        print("No sessions with user messages found.")
        sys.exit(0)

    # Aggregate stats
    total_skill_calls = sum(len(s["skills_used"]) for s in summaries)
    total_friction = sum(len(s["friction_events"]) for s in summaries)
    skill_freq = defaultdict(int)
    for s in summaries:
        for sk in s["skills_used"]:
            skill_freq[sk["skill"]] += 1

    lines = []
    lines.append("# Claude Code Session Data")
    lines.append(f"**Period**: Last {HOURS_BACK}h  |  **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Sessions**: {len(summaries)}  |  **Skill calls**: {total_skill_calls}  |  **Friction events**: {total_friction}")
    lines.append(f"**Installed skills**: {', '.join(installed_skills)}")
    if skill_freq:
        freq_str = ", ".join(f"`{k}` ×{v}" for k, v in sorted(skill_freq.items(), key=lambda x: -x[1]))
        lines.append(f"**Skill frequency**: {freq_str}")
    lines.append("")

    # Sessions with skills
    with_skills = [s for s in summaries if s["skills_used"]]
    without_skills = [s for s in summaries if not s["skills_used"]]

    lines.append(f"## Sessions with skill use ({len(with_skills)})")
    for s in with_skills:
        lines.append(f"\n### [{s['session_id']}] {s['time']}")
        lines.append("**User asked:**")
        for msg in s["user_messages"][:4]:
            lines.append(f"- {msg}")
        lines.append("**Skills invoked:**")
        for sk in s["skills_used"]:
            args = f" — `{sk['args'][:120]}`" if sk["args"] else ""
            lines.append(f"- `{sk['skill']}`{args}")
        if s["friction_events"]:
            lines.append("**⚠ Friction detected:**")
            for fe in s["friction_events"]:
                patterns = ", ".join(fe["patterns"])
                lines.append(f"- [{patterns}] \"{fe['message'][:200]}\"")
                if fe.get("prev_context"):
                    lines.append(f"  ↳ after: \"{fe['prev_context'][:150]}\"")

    lines.append(f"\n## Sessions without skill use ({len(without_skills)})")
    for s in without_skills:
        lines.append(f"\n### [{s['session_id']}] {s['time']}")
        lines.append("**User asked:**")
        for msg in s["user_messages"][:5]:
            lines.append(f"- {msg}")
        if s["tools_used"]:
            top_tools = sorted(s["tools_used"].items(), key=lambda x: -x[1])[:6]
            lines.append(f"**Tools used**: {', '.join(f'{t}(×{c})' for t,c in top_tools)}")
        if s["friction_events"]:
            lines.append("**⚠ Friction detected:**")
            for fe in s["friction_events"]:
                lines.append(f"- \"{fe['message'][:200]}\"")
        if s["missed_hints"]:
            lines.append("**🔍 Possible missed skill triggers (tool signal):**")
            for hint in s["missed_hints"]:
                lines.append(f"- `{hint['candidate_skill']}` (detected `{hint['tool_signal']}` usage without skill)")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
