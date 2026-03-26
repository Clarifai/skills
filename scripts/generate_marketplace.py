#!/usr/bin/env python3
"""Generate marketplace.json from SKILL.md frontmatter in .github/skills/."""

import json
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / ".github" / "skills"
OUTPUT = Path(__file__).parent.parent / "marketplace.json"


def parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text()
    # Strip ````skill wrapper if present (clarifai-grpc uses this)
    text = re.sub(r"^````skill\s*\n", "", text)
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    frontmatter = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter


def main():
    skills = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = parse_frontmatter(skill_md)
        if not fm.get("name"):
            print(f"  SKIP {skill_dir.name} (no name in frontmatter)")
            continue
        skills.append({
            "id": skill_dir.name,
            "name": fm["name"],
            "description": fm.get("description", ""),
            "tags": [],
        })
        print(f"  {skill_dir.name}")

    marketplace = {
        "version": 1,
        "repo": "Clarifai/skills",
        "branch": "main",
        "skills_path": ".github/skills",
        "skills": skills,
    }

    OUTPUT.write_text(json.dumps(marketplace, indent=2) + "\n")
    print(f"\nWrote {len(skills)} skills to {OUTPUT}")


if __name__ == "__main__":
    main()
