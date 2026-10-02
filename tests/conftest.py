import os, sys, tempfile
from pathlib import Path
os.environ["AR_HOME"] = tempfile.mkdtemp(prefix="ar_test_")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest
from fastapi.testclient import TestClient
from ar.api import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
