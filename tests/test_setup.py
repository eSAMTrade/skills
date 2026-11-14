import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from aicodesign import ai_draft

PACKAGE = Path(__file__).resolve().parents[1]


@ai_draft("GPT-6.1 Terra")
class SetupTest(unittest.TestCase):
    @staticmethod
    @ai_draft("GPT-6.1 Terra")
    def _run(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(PACKAGE / "setup.py"), *args], capture_output=True, text=True)

    @ai_draft("GPT-6.1 Terra")
    def test_each_selected_skill_has_all_local_markdown_references(self) -> None:
        names = sorted(path.name for path in (PACKAGE / "skills").iterdir() if (path / "SKILL.md").is_file())
        self.assertEqual(len(names), 10)
        with tempfile.TemporaryDirectory() as directory:
            for name in names:
                with self.subTest(skill=name):
                    target = Path(directory) / name
                    result = self._run("install", str(target), "--assistant", "codex", "--skill", name)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    skills = target / ".agents/skills"
                    for markdown in skills.rglob("*.md"):
                        for link in re.findall(r"\]\(([^)]+)\)", markdown.read_text()):
                            path, _, anchor = link.partition("#")
                            if re.match(r"[a-zA-Z]+:|/", path):
                                continue
                            reference = markdown.parent / path if path else markdown
                            self.assertTrue(reference.is_file(), f"{name}: {markdown}: {link}")
                            if anchor:
                                headings = re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", reference.read_text(), re.MULTILINE)
                                slugs = {re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-") for heading in headings}
                                self.assertIn(anchor, slugs, f"{name}: {markdown}: {link}")

    @ai_draft("GPT-6.1 Terra")
    def test_default_install_copies_skills_to_both_default_locations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"

            result = self._run("install", str(target))

            self.assertEqual(result.returncode, 0, result.stderr)
            for host in (".agents", ".claude"):
                self.assertTrue((target / host / "skills/code-standards/SKILL.md").is_file())
                self.assertTrue((target / host / "skills/grill-form/grill.js").is_file())
            for host in (".github", ".codex", ".vscode", ".opencode"):
                self.assertFalse((target / host).exists())

    @ai_draft("GPT-6.1 Terra")
    def test_subset_installs_dependency_closure_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"

            result = self._run("install", str(target), "--assistant", "codex", "--skill", "grill-form")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({p.name for p in (target / ".agents/skills").iterdir()}, {"grill-form", "writing-style"})
            self.assertFalse((target / ".claude").exists())

    @ai_draft("GPT-6.1 Terra")
    def test_full_install_remains_self_contained_after_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "original"
            result = self._run("install", str(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            relocated = root / "relocated"
            target.rename(relocated)

            for host in (".agents", ".claude"):
                skills = relocated / host / "skills"
                self.assertEqual(len(list(skills.iterdir())), 10)
                for path in skills.rglob("*"):
                    self.assertFalse(path.is_symlink(), str(path))
                for skill_file in skills.rglob("*.md"):
                    content = skill_file.read_text()
                    self.assertNotIn(".github/shared", content, str(skill_file))
                    for link in re.findall(r"\]\(([^)]+)\)", content):
                        relative = link.split("#", 1)[0]
                        if relative and not re.match(r"[a-zA-Z]+:|/", relative):
                            self.assertTrue((skill_file.parent / relative).exists(), f"{skill_file}: {link}")

    @ai_draft("GPT-6.1 Terra")
    def test_cyclic_dependency_closure_is_finite_and_excludes_unrelated_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            result = self._run("install", str(target), "--assistant", "opencode", "--skill", "orchestrate-subagents")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({p.name for p in (target / ".opencode/skills").iterdir()},
                             {"orchestrate-subagents", "py-dev", "java-dev", "code-standards", "writing-style", "spec-writer"})
            self.assertFalse((target / ".agents").exists())

    @ai_draft("GPT-6.1 Terra")
    def test_repeated_assistants_and_skills_are_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            args = ("install", str(target), "--assistant", "codex", "--assistant", "copilot", "--assistant", "claude",
                    "--skill", "grill-form", "--skill", "spec-writer")

            first = self._run(*args)
            second = self._run(*args)

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            for host in (".agents", ".claude"):
                self.assertEqual({p.name for p in (target / host / "skills").iterdir()}, {"grill-form", "spec-writer", "writing-style"})

    @ai_draft("GPT-6.1 Terra")
    def test_late_conflict_rejects_entire_install_before_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            conflict = target / ".claude/skills/writing-style/SKILL.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("local change")

            result = self._run("install", str(target), "--skill", "grill-form")

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(conflict.read_text(), "local change")
            self.assertFalse((target / ".agents").exists())
            self.assertFalse((target / ".claude/skills/grill-form").exists())

    @ai_draft("GPT-6.1 Terra")
    def test_force_replaces_selected_files_and_keeps_extra_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            args = ("install", str(target), "--assistant", "claude", "--skill", "grill-form")
            first = self._run(*args)
            self.assertEqual(first.returncode, 0, first.stderr)
            skill = target / ".claude/skills/grill-form/SKILL.md"
            skill.write_text("local change")
            extra = skill.parent / "local.txt"
            extra.write_text("keep")

            conflict = self._run(*args)
            forced = self._run(*args, "--force")

            self.assertNotEqual(conflict.returncode, 0)
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertEqual(skill.read_bytes(), (PACKAGE / "skills/grill-form/SKILL.md").read_bytes())
            self.assertEqual(extra.read_text(), "keep")

    @ai_draft("GPT-6.1 Terra")
    def test_install_rejects_symlinked_destination_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside"
            outside.mkdir()
            target = root / "target"
            target.mkdir()
            (target / ".claude").symlink_to(outside, target_is_directory=True)

            result = self._run("install", str(target))

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(outside.iterdir()), [])
            self.assertFalse((target / ".agents").exists())

    @ai_draft("GPT-6.1 Terra")
    def test_sync_rejects_blocked_parent_before_replacing_earlier_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "destination"
            early = destination / "skills/grill-form/SKILL.md"
            early.parent.mkdir(parents=True)
            early.write_text("preserve")
            blocked = destination / "skills/web-ui-guidelines/references"
            blocked.parent.mkdir(parents=True)
            blocked.write_text("preserve")

            result = self._run("sync", str(PACKAGE), str(destination), "--force")

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(early.read_text(), "preserve")
            self.assertEqual(blocked.read_text(), "preserve")

    @ai_draft("GPT-6.1 Terra")
    def test_force_rejects_symlinked_destination_file_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside.txt"
            outside.write_text("preserve")
            target = root / "target"
            link = target / ".claude/skills/writing-style/SKILL.md"
            link.parent.mkdir(parents=True)
            link.symlink_to(outside)

            result = self._run("install", str(target), "--skill", "grill-form", "--force")

            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(link.is_symlink())
            self.assertEqual(outside.read_text(), "preserve")
            self.assertFalse((target / ".agents").exists())
            self.assertFalse((target / ".claude/skills/grill-form").exists())

    @ai_draft("GPT-6.1 Terra")
    def test_install_rejects_symlinked_target_and_ancestor_even_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for link_is_root in (True, False):
                with self.subTest(link_is_root=link_is_root):
                    case = root / str(link_is_root)
                    outside = case / "outside"
                    outside.mkdir(parents=True)
                    marker = outside / "marker.txt"
                    marker.write_text("preserve")
                    alias = case / "alias"
                    alias.symlink_to(outside, target_is_directory=True)
                    target = alias if link_is_root else alias / "project"

                    result = self._run("install", str(target), "--skill", "grill-form", "--force")

                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(marker.read_text(), "preserve")
                    self.assertEqual({path.name for path in outside.iterdir()}, {"marker.txt"})

    @ai_draft("GPT-6.1 Terra")
    def test_sync_rejects_symlinked_source_root_and_ancestor_even_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for link_is_root in (True, False):
                with self.subTest(link_is_root=link_is_root):
                    case = root / str(link_is_root)
                    outside = case / "outside"
                    source = outside if link_is_root else outside / "collection"
                    shutil.copytree(PACKAGE / "skills", source / "skills")
                    alias = case / "alias"
                    alias.symlink_to(outside, target_is_directory=True)
                    source_argument = alias if link_is_root else alias / "collection"
                    destination = case / "destination"

                    result = self._run("sync", str(source_argument), str(destination), "--skill", "grill-form", "--force")

                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(destination.exists())
                    self.assertEqual((source / "skills/grill-form/SKILL.md").read_bytes(), (PACKAGE / "skills/grill-form/SKILL.md").read_bytes())

    @ai_draft("GPT-6.1 Terra")
    def test_sync_rejects_symlinked_destination_root_and_ancestor_even_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for link_is_root in (True, False):
                with self.subTest(link_is_root=link_is_root):
                    case = root / str(link_is_root)
                    outside = case / "outside"
                    outside.mkdir(parents=True)
                    marker = outside / "marker.txt"
                    marker.write_text("preserve")
                    alias = case / "alias"
                    alias.symlink_to(outside, target_is_directory=True)
                    destination = alias if link_is_root else alias / "collection"

                    result = self._run("sync", str(PACKAGE), str(destination), "--skill", "grill-form", "--force")

                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(marker.read_text(), "preserve")
                    self.assertEqual({path.name for path in outside.iterdir()}, {"marker.txt"})

    @ai_draft("GPT-6.1 Terra")
    def test_sync_rejects_symlinked_source_before_creating_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            shutil.copytree(PACKAGE / "skills", source / "skills")
            skill = source / "skills/grill-form/SKILL.md"
            skill.unlink()
            skill.symlink_to(PACKAGE / "skills/grill-form/SKILL.md")
            destination = root / "destination"

            result = self._run("sync", str(source), str(destination), "--skill", "grill-form")

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())

    @ai_draft("GPT-6.1 Terra")
    def test_sync_missing_source_fails_before_creating_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            shutil.copytree(PACKAGE / "skills", source / "skills")
            (source / "skills/writing-style/SKILL.md").unlink()
            destination = root / "destination"

            result = self._run("sync", str(source), str(destination), "--skill", "grill-form")

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())

    @ai_draft("GPT-6.1 Terra")
    def test_sync_copies_only_allowlisted_files_and_dependency_closure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            shutil.copytree(PACKAGE / "skills", source / "skills")
            (source / "skills/grill-form/private.txt").write_text("private")
            destination = root / "destination"

            result = self._run("sync", str(source), str(destination), "--skill", "grill-form")
            second = self._run("sync", str(source), str(destination), "--skill", "grill-form")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual({p.name for p in (destination / "skills").iterdir()}, {"grill-form", "writing-style"})
            self.assertFalse((destination / "skills/grill-form/private.txt").exists())
            self.assertEqual((destination / "skills/grill-form/SKILL.md").read_bytes(), (source / "skills/grill-form/SKILL.md").read_bytes())

    @ai_draft("GPT-6.1 Terra")
    def test_sync_rejects_late_conflict_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "destination"
            conflict = destination / "skills/writing-style/SKILL.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("local change")

            result = self._run("sync", str(PACKAGE), str(destination), "--skill", "grill-form")

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(conflict.read_text(), "local change")
            self.assertFalse((destination / "skills/grill-form").exists())

    @ai_draft("GPT-6.1 Terra")
    def test_sync_force_replaces_conflicting_file_without_removing_extra(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "destination"
            args = ("sync", str(PACKAGE), str(destination), "--skill", "grill-form")
            first = self._run(*args)
            self.assertEqual(first.returncode, 0, first.stderr)
            skill = destination / "skills/grill-form/SKILL.md"
            skill.write_text("local change")
            extra = skill.parent / "local.txt"
            extra.write_text("keep")

            conflict = self._run(*args)
            forced = self._run(*args, "--force")

            self.assertNotEqual(conflict.returncode, 0)
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertEqual(skill.read_bytes(), (PACKAGE / "skills/grill-form/SKILL.md").read_bytes())
            self.assertEqual(extra.read_text(), "keep")

    @ai_draft("GPT-6.1 Terra")
    def test_unknown_skill_and_assistant_are_rejected_before_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for option, value in (("--skill", "not-a-skill"), ("--assistant", "not-an-assistant")):
                target = root / value

                result = self._run("install", str(target), option, value)

                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
