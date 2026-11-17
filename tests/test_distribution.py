# Copyright (c) 2026 Rahul Chalamala
"""Exercise installable distribution failures before the public export."""

import json
import runpy
import shutil
import stat
import tempfile
import unittest
from pathlib import Path

import pytest


class DistributionTests(unittest.TestCase):
    """Check the exported bundle with missing, conflicting and corrupted inputs."""

    def setUp(self) -> None:
        """Copy the bundle into an isolated export directory."""
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "plugin"
        shutil.copytree(Path(__file__).resolve().parents[1], self.root)
        for path in (self.root, *self.root.rglob("*")):
            path.chmod(path.stat().st_mode | stat.S_IWUSR)

    def _check(self) -> None:
        runpy.run_path(str(self.root / "scripts/check.py"), run_name="__main__")

    def test_standalone_export_passes(self) -> None:
        """Validate without any surrounding monorepo files."""
        self._check()

    def test_missing_entry_point_fails(self) -> None:
        """Reject a bundle that cannot activate its advertised workflow."""
        shutil.rmtree(self.root / "skills/engineering")
        with pytest.raises(ValueError, match="entry point"):
            self._check()

    def test_missing_dependency_fails(self) -> None:
        """Reject a bundle whose debugging dependency was omitted."""
        shutil.rmtree(self.root / "skills/tdd")
        with pytest.raises(FileNotFoundError):
            self._check()

    def test_upstream_edit_requires_lock_update(self) -> None:
        """Reject an unrecorded edit to a pinned upstream skill."""
        skill = self.root / "skills/grilling/SKILL.md"
        skill.write_text(skill.read_text() + "\nUnrecorded instruction\n")
        with pytest.raises(ValueError, match="grilling"):
            self._check()

    def test_first_party_dependency_must_exist(self) -> None:
        """Reject an entry point that calls an unavailable skill."""
        skill = self.root / "skills/engineering/SKILL.md"
        skill.write_text(skill.read_text() + "\nUse engineering:unavailable-helper.\n")
        with pytest.raises(ValueError, match="unavailable-helper"):
            self._check()

    def test_examples_are_not_missing_resources(self) -> None:
        """Allow example paths while checking real reference links."""
        skill = self.root / "skills/engineering/SKILL.md"
        skill.write_text(skill.read_text() + "\n```md\n[Example](example/file.md)\n```\n")
        self._check()
        skill.write_text(skill.read_text() + "\n[Required reference](missing.md)\n")
        with pytest.raises(ValueError, match=r"missing\.md"):
            self._check()

    def test_manifests_must_install_the_same_plugin(self) -> None:
        """Reject a marketplace whose entry disagrees with its plugin manifest."""
        path = self.root / ".codex-plugin/marketplace.json"
        marketplace = json.loads(path.read_text())
        marketplace["plugins"][0]["name"] += "-other"
        path.write_text(json.dumps(marketplace))
        with pytest.raises(ValueError, match="codex"):
            self._check()


if __name__ == "__main__":
    unittest.main()
