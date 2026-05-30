#!/usr/bin/env python3
"""
generate_skills_manifest.py
───────────────────────────
Run once from the same folder as genai-lab.html:

    python generate_skills_manifest.py

Re-run every time you add, rename, or remove a skill folder.
Commits skills-manifest.json alongside genai-lab.html.

Directory layout expected:
    genai-lab.html                        ← this script lives here too
    genailab/
      skills/
        claude/
          Design/
            SKILL.md
          Document/
            SKILL.md
          ...
        openai/
          cli-creator/
            SKILL.md
          ...
        custom/
          karpathy-guidelines/
            SKILL.md
"""

import os, json, re

SKILLS_ROOT = os.path.join("skills")
OUTPUT_FILE = "skills-manifest.json"

PROVIDER_ORDER = {"claude": 0, "openai": 1, "custom": 2}

def parse_skill_md(filepath):
    try:
        text = open(filepath, encoding="utf-8").read()
    except Exception:
        return {"name": "", "description": ""}

    name, description = "", ""

    # 1. YAML frontmatter between --- markers
    fm = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if fm:
        fm_text = fm.group(1)
        n = re.search(r'^name\s*:\s*(.+)$', fm_text, re.MULTILINE)
        d = re.search(r'^description\s*:\s*([\s\S]+?)(?=\n\w|\n---|\Z)', fm_text, re.MULTILINE)
        if n: name = n.group(1).strip()
        if d: description = re.sub(r'\n\s+', ' ', d.group(1)).strip()

    # 2. Fallback: first # heading
    if not name:
        h = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
        if h: name = h.group(1).strip()

    # 3. Fallback: first real paragraph
    if not description:
        body = re.sub(r'^---[\s\S]*?---\s*', '', text, flags=re.MULTILINE)
        body = re.sub(r'^#[^\n]*\n', '', body, flags=re.MULTILINE).strip()
        for para in re.split(r'\n{2,}', body):
            clean = re.sub(r'[*_`#>\[\]|\\]', '', para).strip()
            clean = re.sub(r'\s+', ' ', clean)
            if len(clean) > 20:
                description = clean
                break

    return {"name": name, "description": description}

def build_manifest():
    if not os.path.isdir(SKILLS_ROOT):
        print(f"ERROR: '{SKILLS_ROOT}' not found. Run from the same folder as genai-lab.html.")
        return

    providers = sorted(
        [d for d in os.listdir(SKILLS_ROOT) if os.path.isdir(os.path.join(SKILLS_ROOT, d))],
        key=lambda x: (PROVIDER_ORDER.get(x, 99), x)
    )

    manifest = {}
    total = 0

    for provider in providers:
        ppath = os.path.join(SKILLS_ROOT, provider)
        folders = sorted(
            [d for d in os.listdir(ppath) if os.path.isdir(os.path.join(ppath, d))]
        )

        skills = []
        for folder in folders:
            md_path = os.path.join(ppath, folder, "SKILL.md")
            parsed  = parse_skill_md(md_path) if os.path.isfile(md_path) else {"name": "", "description": ""}

            skills.append({
                "folder":      folder,
                "name":        parsed["name"] or folder.replace("-", " ").replace("_", " ").title(),
                "description": parsed["description"],
                # relative URL from genai-lab.html → used by fetch()
                "skill_md":    f"genailab/skills/{provider}/{folder}/SKILL.md",
            })
            total += 1
            print(f"  [{provider}] {folder}: {parsed['name'] or '(name from folder)'}")

        manifest[provider] = skills

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n✓  {OUTPUT_FILE} written — {total} skills across {len(providers)} providers")
    print(f"   Commit this file alongside genai-lab.html.")

if __name__ == "__main__":
    build_manifest()
