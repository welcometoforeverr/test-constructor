"""Pytest path setup for the project."""

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def legacy_seed(db):
    """Seed a disposable Django test DB, never the working database."""
    from django.core.management import call_command

    call_command("import_legacy", verbosity=0)
