from fastapi.testclient import TestClient
from devopst.main import app

client = TestClient(app)


def test_runs_and_refuses_a_write():
    payload = client.post("/agent/run", json={"goal": 'why did CI fail', **{'payload': {'log': ['pytest failed']}}}).json()
    assert payload["refused"] is False
    assert payload["applied"] is False
    assert payload["hypothesis"] == "tests"
    refused = client.post("/agent/run", json={"goal": 'force push with --no-verify'}).json()
    assert refused["refused"] is True
