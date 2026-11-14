# /// script
# requires-python = ">=3.12"
# dependencies = ["aicodesign>=0.1.1"]
# ///
"""Copy portable skills and their dependencies into projects or another collection."""
import argparse
import shutil
from collections.abc import Sequence
from pathlib import Path

from aicodesign import ai_draft

PACKAGE = Path(__file__).resolve().parent
SKILL_FILES: dict[str, tuple[str, ...]] = {
    "grill-form": ("SKILL.md", "grill.js", "agents/openai.yaml"),
    "grill-me": ("SKILL.md", "agents/openai.yaml"),
    "handoff": ("SKILL.md", "agents/openai.yaml"),
    "orchestrate-subagents": ("SKILL.md",),
    "web-ui-guidelines": (
        "SKILL.md", "agents/openai.yaml", "references/content.md", "references/guidelines.md", "references/interaction.md", "references/layout.md",
        "references/performance.md", "references/theming.md"
    ),
    "writing-style": ("SKILL.md",),
    "spec-writer": ("SKILL.md",),
    "py-dev": ("SKILL.md",),
    "java-dev": ("SKILL.md",),
    "code-standards": (
        "SKILL.md", "references/code-design.md", "references/java.instructions.md", "references/python.instructions.md", "references/py-test-rules.instructions.md",
        "references/instruction-compliance-gate.instructions.md", "references/file-creation-rules.instructions.md"
    )
}
DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "grill-form": ("writing-style",),
    "grill-me": ("writing-style",),
    "spec-writer": ("writing-style",),
    "code-standards": ("writing-style", "spec-writer"),
    "orchestrate-subagents": ("py-dev", "java-dev"),
    "py-dev": ("orchestrate-subagents", "code-standards", "writing-style", "spec-writer"),
    "java-dev": ("orchestrate-subagents", "code-standards", "writing-style", "spec-writer")
}
ASSISTANT_PATHS = {"codex": ".agents/skills", "copilot": ".agents/skills", "claude": ".claude/skills", "opencode": ".opencode/skills"}


@ai_draft("GPT-6 Astra")
def selected_files(skills: Sequence[str]) -> tuple[Path, ...]:
    """Return the allowlisted files for these skills and their transitive dependencies."""
    selected: set[str] = set()
    pending = list(skills)
    while pending:
        name = pending.pop()
        if name not in SKILL_FILES:
            raise ValueError(f"Unknown skill: {name}")
        if name in selected:
            continue
        selected.add(name)
        pending.extend(DEPENDENCIES.get(name, ()))
    return tuple(Path(name) / filename for name in sorted(selected) for filename in SKILL_FILES[name])


@ai_draft("GPT-6 Astra")
def copy_files(source: Path, destinations: Sequence[Path], files: Sequence[Path], force: bool) -> None:
    """Preflight every selected path, then copy files without deleting unrelated content."""
    copies: list[tuple[Path, Path]] = []
    for relative in files:
        src = source / relative
        if src.is_symlink() or any(parent.is_symlink() for parent in src.parents):
            raise ValueError(f"Source contains a symlink: {src}")
        if not src.is_file():
            raise FileNotFoundError(f"Missing source: {src}")
        for destination in destinations:
            dst = destination / relative
            if dst.is_symlink() or any(parent.is_symlink() or (parent.exists() and not parent.is_dir()) for parent in dst.parents):
                raise ValueError(f"Invalid destination path: {dst}")
            if dst.exists():
                if not dst.is_file():
                    raise FileExistsError(f"Destination is not a file: {dst}")
                if dst.read_bytes() == src.read_bytes():
                    continue
                if not force:
                    raise FileExistsError(f"Destination differs: {dst}; use --force to overwrite selected files")
            copies.append((src, dst))
    for src, dst in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    print(f"Copied {len(copies)} files; {len(files)} selected files per destination.")


@ai_draft("GPT-6 Astra")
def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    install_parser = commands.add_parser("install", help="Copy skills into a project, including dependencies")
    install_parser.add_argument("target", type=Path)
    install_parser.add_argument("--assistant", action="append", choices=tuple(ASSISTANT_PATHS), help="Repeat to select assistants; default: codex, copilot and claude")
    sync_parser = commands.add_parser("sync", help="Copy a portable subset between collection roots")
    sync_parser.add_argument("source", type=Path)
    sync_parser.add_argument("destination", type=Path)
    for command_parser in (install_parser, sync_parser):
        command_parser.add_argument("--skill", action="append", choices=tuple(SKILL_FILES), help="Repeat to select skills; default: all")
        command_parser.add_argument("--force", action="store_true", help="Overwrite differing selected files; never delete unrelated files")
    args = parser.parse_args(argv)
    files = selected_files(args.skill if args.skill is not None else tuple(SKILL_FILES))
    if args.command == "install":
        target = args.target.absolute()
        assistants = args.assistant if args.assistant is not None else ("codex", "copilot", "claude")
        destinations = tuple(dict.fromkeys(target / ASSISTANT_PATHS[name] for name in assistants))
        source = PACKAGE / "skills"
    else:
        source = args.source.absolute() / "skills"
        destinations = (args.destination.absolute() / "skills",)
    try:
        copy_files(source, destinations, files, args.force)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
