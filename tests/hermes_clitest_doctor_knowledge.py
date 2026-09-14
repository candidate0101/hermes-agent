"""Behavior tests for project-knowledge-base diagnostics."""

from hermes_cli import doctor_knowledge


def test_obsidian_check_reports_a_configured_missing_vault(monkeypatch, capsys, tmp_path):
    missing_vault = tmp_path / "missing-vault"
    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(missing_vault))

    finding = doctor_knowledge._check_obsidian_vault(False)

    assert finding.manual_issues == [
        f"Obsidian vault path does not exist: {missing_vault}. Set OBSIDIAN_VAULT_PATH to the vault directory."
    ]
    assert "Obsidian vault directory" in capsys.readouterr().out


def test_obsidian_check_accepts_an_accessible_configured_vault(monkeypatch, capsys, tmp_path):
    vault = tmp_path / "Project knowledge base"
    vault.mkdir()
    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault))

    finding = doctor_knowledge._check_obsidian_vault(False)

    assert finding.manual_issues == []
    assert "Obsidian vault directory" in capsys.readouterr().out
