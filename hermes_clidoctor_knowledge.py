"""Project knowledge-base diagnostics for ``hermes doctor``."""

from __future__ import annotations

import os
from pathlib import Path

from hermes_cli.doctor_report import Finding, check_fail, check_ok, check_warn, doctor_check


@doctor_check()
def _check_obsidian_vault(should_fix: bool, f: Finding) -> None:
    """Report whether the explicitly configured Obsidian vault is usable by Hermes."""
    configured_path = os.getenv("OBSIDIAN_VAULT_PATH", "").strip()
    if not configured_path:
        check_warn("Obsidian vault directory", "(OBSIDIAN_VAULT_PATH is not configured)")
        return

    vault = Path(configured_path).expanduser()
    if not vault.is_dir():
        check_fail("Obsidian vault directory", "(configured path does not exist)")
        f.manual_issues.append(
            f"Obsidian vault path does not exist: {vault}. Set OBSIDIAN_VAULT_PATH to the vault directory."
        )
        return

    if not os.access(vault, os.R_OK | os.W_OK | os.X_OK):
        check_fail("Obsidian vault directory", "(read/write access denied)")
        f.manual_issues.append(
            f"Obsidian vault is not readable and writable: {vault}. Check its filesystem permissions."
        )
        return

    check_ok("Obsidian vault directory", f"({vault})")
