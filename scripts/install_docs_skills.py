from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SKILLS = ["docs-init", "docs-executor", "docs-plan-ap", "docs-plan-sddr", "docs-reviewer"]
LEGACY_CODEX_SKILLS = [
    "xml-docs-init-executor",
    "xml-docs-init-plan-ap",
    "xml-docs-init-plan-sddr",
    "xml-docs-init-reviewer",
]


class InstallError(RuntimeError):
    pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def copy_tree(source: Path, destination: Path, backup_root: Path | None = None) -> str:
    if not source.is_dir():
        raise InstallError(f"Missing source skill: {source}")

    action = "created"
    if destination.exists():
        action = "updated"
        if backup_root is not None:
            backup_root.mkdir(parents=True, exist_ok=True)
            backup_destination = backup_root / destination.name
            if backup_destination.exists():
                raise InstallError(f"Backup path already exists: {backup_destination}")
            shutil.copytree(destination, backup_destination)
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    return action


def basic_validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{skill_dir.name}: missing SKILL.md")
        return errors

    text = skill_md.read_text(encoding="utf-8")
    if text.startswith("---\n") is False:
        errors.append(f"{skill_dir.name}: missing YAML frontmatter")
    if f"name: {skill_dir.name}" not in text:
        errors.append(f"{skill_dir.name}: frontmatter name mismatch")
    if "description:" not in text:
        errors.append(f"{skill_dir.name}: missing description")
    if "[TODO" in text:
        errors.append(f"{skill_dir.name}: contains TODO placeholder")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        errors.append(f"{skill_dir.name}: missing agents/openai.yaml")
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        if "allow_implicit_invocation: false" not in yaml_text:
            errors.append(f"{skill_dir.name}: explicit invocation policy missing")

    return errors


def run_quick_validate(skill_dir: Path) -> tuple[bool, str]:
    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    if not validator.is_file():
        return True, "quick_validate.py not found; used internal validation only"

    result = subprocess.run([sys.executable, str(validator), str(skill_dir)], capture_output=True, text=True, check=False)
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def validate_all(skill_roots: list[Path]) -> list[str]:
    errors: list[str] = []
    for skill_dir in skill_roots:
        errors.extend(basic_validate_skill(skill_dir))
        ok, output = run_quick_validate(skill_dir)
        if not ok:
            errors.append(f"{skill_dir.name}: quick_validate failed: {output}")
    return errors


def disable_legacy(codex_skills: Path, disabled_root: Path) -> list[str]:
    moved: list[str] = []
    disabled_root.mkdir(parents=True, exist_ok=True)
    for name in LEGACY_CODEX_SKILLS:
        source = codex_skills / name
        if not source.exists():
            continue
        destination = disabled_root / name
        if destination.exists():
            raise InstallError(f"Disabled legacy path already exists: {destination}")
        shutil.move(str(source), str(destination))
        moved.append(str(destination))
    return moved


def clean_docs_skills(target_root: Path, disabled_root: Path) -> list[str]:
    moved: list[str] = []
    if not target_root.exists():
        return moved

    disabled_root.mkdir(parents=True, exist_ok=True)
    for source in target_root.iterdir():
        if not source.is_dir():
            continue
        is_docs_skill = source.name.startswith("docs-") or source.name.startswith("xml-docs-")
        is_current_skill = source.name in SKILLS
        if not is_docs_skill or is_current_skill:
            continue
        destination = disabled_root / source.name
        if destination.exists():
            raise InstallError(f"Disabled DOCS path already exists: {destination}")
        shutil.move(str(source), str(destination))
        moved.append(str(destination))
    return moved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install DOCS method skills.")
    parser.add_argument("command", nargs="?", choices=["install", "update"], default="install", help="Install or update skills. Both copy the current repository version.")
    parser.add_argument("--codex-skills", default=str(Path.home() / ".codex" / "skills"), help="Target .codex skills directory.")
    parser.add_argument("--agents-skills", default=str(Path.home() / ".agents" / "skills"), help="Target .agents skills directory.")
    parser.add_argument("--keep-legacy", action="store_true", help="Do not disable xml-docs-init-* legacy skills.")
    parser.add_argument("--clean-docs", action="store_true", help="Move any installed docs-* or xml-docs-* skill not in this package.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    source_root = root / "skills"
    codex_skills = Path(args.codex_skills).expanduser().resolve()
    agents_skills = Path(args.agents_skills).expanduser().resolve()
    stamp = timestamp()
    backup_root = codex_skills.parent / "skills-backups" / stamp

    try:
        source_errors = validate_all([source_root / name for name in SKILLS])
        if source_errors:
            raise InstallError("Source validation failed: " + "; ".join(source_errors))

        installed: dict[str, str] = {}
        disabled: list[str] = []
        if args.clean_docs:
            disabled.extend(clean_docs_skills(codex_skills, codex_skills.parent / "skills-disabled" / stamp / ".codex"))
            disabled.extend(clean_docs_skills(agents_skills, codex_skills.parent / "skills-disabled" / stamp / ".agents"))

        codex_installed_dirs: list[Path] = []
        for name in SKILLS:
            destination = codex_skills / name
            installed[str(destination)] = copy_tree(source_root / name, destination, backup_root / ".codex")
            codex_installed_dirs.append(destination)

        agents_docs_init = agents_skills / "docs-init"
        installed[str(agents_docs_init)] = copy_tree(source_root / "docs-init", agents_docs_init, backup_root / ".agents")

        installed_errors = validate_all(codex_installed_dirs + [agents_docs_init])
        if installed_errors:
            raise InstallError("Installed validation failed: " + "; ".join(installed_errors))

        if not args.keep_legacy:
            disabled.extend(disable_legacy(codex_skills, codex_skills.parent / "skills-disabled" / stamp))

        payload = {
            "installed": installed,
            "disabled": disabled,
            "backup_root": str(backup_root),
            "codex_skills": str(codex_skills),
            "agents_docs_init": str(agents_docs_init),
            "valid": True,
        }
        print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))
        return 0
    except InstallError as exc:
        print(json.dumps({"error": str(exc), "valid": False}, ensure_ascii=True, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
