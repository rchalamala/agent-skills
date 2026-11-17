# Copyright (c) 2026 Rahul Chalamala
"""Validate the distributable plugin and its pinned upstream resources."""

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def _require(condition: object, detail: object) -> None:
    if not condition:
        raise ValueError(str(detail))


def _manifests(root: Path) -> str:
    canonical = json.loads((root / "plugin.json").read_text())
    for harness in ("claude", "codex", "cursor"):
        directory = root / f".{harness}-plugin"
        manifest = json.loads((directory / "plugin.json").read_text())
        for key in ("name", "version", "description", "repository", "license"):
            _require(manifest[key] == canonical[key], (harness, key))
        marketplace = json.loads((directory / "marketplace.json").read_text())
        _require(len(marketplace["plugins"]) == 1, harness)
        plugin = marketplace["plugins"][0]
        _require(plugin["name"] == canonical["name"], harness)
        _require((root / plugin["source"]).resolve() == root, harness)
    codex = json.loads((root / ".codex-plugin/plugin.json").read_text())
    _require(codex["skills"] == "./skills/", "Codex must discover the packaged skills")
    return str(canonical["name"])


def _upstreams(root: Path, skills: set[str]) -> set[str]:
    tracked: set[str] = set()
    lock = json.loads((root / "upstream.lock.json").read_text())
    for upstream in lock.values():
        _require(bool(re.fullmatch(r"[0-9a-f]{40}", upstream["revision"])), upstream)
        for relative, expected in upstream["files"].items():
            path = root / relative
            _require(path.resolve().is_relative_to(root), relative)
            _require(not path.is_symlink(), relative)
            _require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, relative)
            tracked.add(relative)
        for skill in upstream["skills"]:
            _require(skill.rsplit("/", 1)[-1] in skills, skill)
    return tracked


def _links(path: Path, content: str) -> None:
    prose = re.sub(r"```[^\n]*\n[\s\S]*?```", "", content)
    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", prose):
        url = urlsplit(target)
        if url.scheme or not url.path:
            continue
        _require((path.parent / unquote(url.path)).exists(), (path, target))


def _resources(root: Path, tracked: set[str], skills: set[str], namespace: str) -> None:
    for path in (root / "skills").rglob("*"):
        _require(not path.is_symlink(), path)
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if not path.is_relative_to(root / "skills" / namespace):
            _require(relative in tracked, relative)
        if path.suffix == ".md":
            content = path.read_text()
            for target in re.findall(rf"{namespace}:([a-z][a-z-]+)", content):
                _require(target in skills, (relative, target))
            for target in re.findall(r'Skill tool with "([a-z-]+)"', content):
                _require(target in skills, (relative, target))
            _links(path, content)


def _invocation(root: Path) -> None:
    for skill in (root / "skills").glob("*/SKILL.md"):
        frontmatter = yaml.safe_load(skill.read_text().split("---", 2)[1])
        _require(isinstance(frontmatter, dict), skill)
        _require(frontmatter.get("name") == skill.parent.name, skill)
        _require(bool(frontmatter.get("description")), skill)
        if frontmatter.get("disable-model-invocation") is True:
            policy = yaml.safe_load((skill.parent / "agents/openai.yaml").read_text())
            _require(policy["policy"]["allow_implicit_invocation"] is False, skill)


def main() -> None:
    """Reject inconsistent manifests, upstream drift and broken skill references."""
    root = Path(__file__).resolve().parents[1]
    skills = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    namespace = _manifests(root)
    _require(namespace in skills, "missing engineering entry point")
    tracked = _upstreams(root, skills)
    _resources(root, tracked, skills, namespace)
    _invocation(root)


if __name__ == "__main__":
    main()
