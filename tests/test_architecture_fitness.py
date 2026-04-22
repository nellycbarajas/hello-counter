"""Architecture-fitness lint: domain layer must not import infrastructure.

Enforces the `layered` boundary declared in
`memory/project_architecture_profile.md §5.1`. Runs as part of the
`lint` stage on CI.
"""

from pathlib import Path


def test_domain_does_not_import_infrastructure():
    domain_dir = Path(__file__).parent.parent / "app" / "domain"
    offenders = []
    for py_file in domain_dir.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if "app.infrastructure" in stripped or "from ..infrastructure" in stripped:
                offenders.append(f"{py_file}: {stripped}")
    assert not offenders, (
        "Layered architecture violated — domain imports infrastructure:\n"
        + "\n".join(offenders)
    )
