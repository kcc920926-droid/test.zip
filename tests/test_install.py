"""Filesystem-level installer checks. Never write to real user skill folders."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("installer", REPO / "scripts/install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="testzip-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project with spaces"
        self.project.mkdir()

    def args(self, tool, *extra):
        return installer.parser().parse_args(["--tool", tool, *map(str, extra)])

    def test_project_install_for_every_supported_host(self):
        expected = {
            "codex": ".agents/skills/adaptive-testing",
            "claude-code": ".claude/skills/adaptive-testing",
            "antigravity": ".agents/skills/adaptive-testing",
            "antigravity-cli": ".agents/skills/adaptive-testing",
            "cursor": ".cursor/skills/adaptive-testing",
        }
        for tool, relative in expected.items():
            with self.subTest(tool=tool):
                project = self.project / tool
                project.mkdir()
                dest = installer.destination_for(self.args(tool, "--project", project))
                self.assertEqual(dest, project / relative)
                installer.install(dest, installer.bundle_for(tool))
                self.assertEqual((dest / "SKILL.md").read_bytes(),
                                 (installer.SOURCE / "SKILL.md").read_bytes())
                self.assertTrue((dest / "references/selective-validation.md").is_file())
                self.assertEqual((dest / "agents/openai.yaml").exists(), tool == "codex")

    def test_personal_locations_are_resolved_under_fake_home(self):
        expected = {
            "codex": ".agents/skills/adaptive-testing",
            "claude-code": ".claude/skills/adaptive-testing",
            "antigravity": ".gemini/config/skills/adaptive-testing",
            "antigravity-cli": ".gemini/antigravity-cli/skills/adaptive-testing",
            "cursor": ".cursor/skills/adaptive-testing",
        }
        home = self.root / "fake home"
        for tool, relative in expected.items():
            with self.subTest(tool=tool):
                dest = installer.destination_for(self.args(tool, "--user"), home=home)
                self.assertEqual(dest, home / relative)

    def test_dry_run_creates_no_directories(self):
        dest = self.root / "not created" / "adaptive-testing"
        outcome = installer.install(dest, installer.bundle_for("claude-code"), dry_run=True)
        self.assertIn("Dry run", outcome)
        self.assertFalse(dest.parent.exists())

    def test_identical_reinstall_preserves_files_and_local_extras(self):
        dest = self.root / "adaptive-testing"
        bundle = installer.bundle_for("claude-code")
        installer.install(dest, bundle)
        extra = dest / "local-note.txt"
        extra.write_text("keep me", encoding="utf-8")
        before = (dest / "SKILL.md").stat().st_mtime_ns
        self.assertIn("Already installed", installer.install(dest, bundle))
        self.assertEqual((dest / "SKILL.md").stat().st_mtime_ns, before)
        self.assertEqual(extra.read_text(encoding="utf-8"), "keep me")

    def test_existing_customization_is_never_overwritten(self):
        dest = self.root / "adaptive-testing"
        installer.install(dest, installer.bundle_for("claude-code"))
        custom = dest / "SKILL.md"
        custom.write_text("local customization", encoding="utf-8")
        for dry_run in (True, False):
            with self.subTest(dry_run=dry_run):
                with self.assertRaises(ValueError):
                    installer.install(dest, installer.bundle_for("codex"), dry_run)
                self.assertEqual(custom.read_text(encoding="utf-8"), "local customization")
                self.assertFalse((dest / "agents").exists())

    def test_shared_project_bundle_needs_no_second_install(self):
        dest = installer.destination_for(self.args("antigravity", "--project", self.project))
        installer.install(dest, installer.bundle_for("antigravity"))
        codex_dest = installer.destination_for(self.args("codex", "--project", self.project))
        self.assertEqual(dest, codex_dest)
        self.assertIn("Already installed", installer.install(dest, installer.bundle_for("codex")))
        self.assertFalse((dest / "agents").exists())

    def test_partial_install_is_not_silently_overwritten(self):
        dest = self.root / "adaptive-testing"
        dest.mkdir()
        with self.assertRaises(ValueError):
            installer.install(dest, installer.bundle_for("cursor"))
        self.assertEqual(list(dest.iterdir()), [])

    def test_generic_requires_explicit_location(self):
        with self.assertRaises(ValueError):
            installer.destination_for(self.args("generic", "--user"))
        dest = installer.destination_for(
            self.args("generic", "--skills-dir", self.root / "custom skills")
        )
        installer.install(dest, installer.bundle_for("generic"))
        self.assertEqual(dest, self.root / "custom skills/adaptive-testing")
        self.assertFalse((dest / "agents").exists())

    def test_missing_project_is_rejected_without_creation(self):
        missing = self.root / "typo"
        with self.assertRaises(ValueError):
            installer.destination_for(self.args("cursor", "--project", missing))
        self.assertFalse(missing.exists())

    def test_cli_works_from_another_directory_and_handles_spaces(self):
        result = subprocess.run(
            [sys.executable, str(REPO / "scripts/install.py"), "--tool", "claude-code",
             "--project", str(self.project)], cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.project / ".claude/skills/adaptive-testing/SKILL.md").is_file())

    def test_cli_conflict_reports_failure_and_preserves_content(self):
        root = self.root / "custom"
        dest = root / "adaptive-testing"
        dest.mkdir(parents=True)
        (dest / "SKILL.md").write_text("mine", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(REPO / "scripts/install.py"), "--tool", "generic",
             "--skills-dir", str(root)], capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nothing was overwritten", result.stderr)
        self.assertEqual((dest / "SKILL.md").read_text(encoding="utf-8"), "mine")


if __name__ == "__main__":
    unittest.main()
