#!/usr/bin/env python3
"""Install one portable skill for a chosen agent; Python 3.9+, stdlib only."""

import argparse
from pathlib import Path
import sys


SKILL_NAME = "adaptive-testing"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / SKILL_NAME
CORE_FILES = ("SKILL.md", "references/selective-validation.md")
PROJECT_ROOTS = {
    "codex": ".agents/skills",
    "claude-code": ".claude/skills",
    "antigravity": ".agents/skills",
    "antigravity-cli": ".agents/skills",
    "cursor": ".cursor/skills",
}
USER_ROOTS = {
    "codex": ".agents/skills",
    "claude-code": ".claude/skills",
    "antigravity": ".gemini/config/skills",
    "antigravity-cli": ".gemini/antigravity-cli/skills",
    "cursor": ".cursor/skills",
}


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--tool", required=True,
                        choices=tuple(PROJECT_ROOTS) + ("generic",))
    location = result.add_mutually_exclusive_group(required=True)
    location.add_argument("--project", type=Path,
                          help="Existing project root (not the skills directory).")
    location.add_argument("--user", action="store_true",
                          help="Install for the current OS user.")
    location.add_argument("--skills-dir", type=Path,
                          help="Explicit skills root; adaptive-testing is appended.")
    result.add_argument("--dry-run", action="store_true",
                        help="Show destination and files without writing anything.")
    return result


def destination_for(args, home=None):
    if args.skills_dir is not None:
        root = args.skills_dir.expanduser().resolve()
    elif args.tool == "generic":
        raise ValueError("generic requires --skills-dir for the host's actual skill path")
    elif args.project is not None:
        project = args.project.expanduser().resolve()
        if not project.is_dir():
            raise ValueError(f"Project directory does not exist: {project}")
        root = project / PROJECT_ROOTS[args.tool]
    else:
        root = (home if home is not None else Path.home()) / USER_ROOTS[args.tool]
    return root / SKILL_NAME


def bundle_for(tool):
    names = CORE_FILES
    if tool == "codex":
        names += ("agents/openai.yaml",)
    # Read everything before making any destination files.
    return {name: (SOURCE / name).read_bytes() for name in names}


def install(destination, bundle, dry_run=False):
    if destination.is_symlink() or getattr(destination, "is_junction", lambda: False)():
        raise ValueError(f"Destination is a link; inspect it manually: {destination}")
    if destination.exists():
        # Optional host UI metadata does not prevent sharing the same core bundle.
        identical = destination.is_dir() and all(
            (destination / name).is_file()
            and (destination / name).read_bytes() == bundle[name]
            for name in CORE_FILES
        )
        if identical:
            return "Already installed; no files changed"
        raise ValueError(
            f"Destination already exists with different or incomplete content: {destination}. "
            "Compare and update the existing skill manually; nothing was overwritten."
        )
    if dry_run:
        return "Dry run; no files changed"
    destination.mkdir(parents=True, exist_ok=False)
    for name, content in bundle.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also protects against files created concurrently.
        with target.open("xb") as output:
            output.write(content)
    return "Installed"


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        destination = destination_for(args)
        bundle = bundle_for(args.tool)
        outcome = install(destination, bundle, args.dry_run)
    except (OSError, ValueError) as error:
        print(f"Install error: {error}", file=sys.stderr)
        return 1
    print(f"{outcome}: {destination}")
    if not outcome.startswith("Already installed"):
        for name in bundle:
            print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
