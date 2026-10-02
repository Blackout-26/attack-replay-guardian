import csv, io
from ar import config as C

T = "Your account will be suspended today. Verify your details immediately using the link below."


def test_health(client):
    j = client.get("/health").json()
    assert j["status"] == "ok" and j["llm_used"] is False


def test_analyze_five_minimum_features(client):
    r = client.post("/analyze", json={"text": T}).json()
    assert r["label"] == "Suspicious" and r["threat_type"] and r["risk"]["band"] in ("Low", "Medium", "High") and r["reason"] and r["action"]
    assert r["meta"]["llm_used"] is False


def test_analyze_invalid_inputs(client):
    assert client.post("/analyze", json={"text": ""}).status_code == 400
    assert client.post("/analyze", json={"text": "   "}).status_code == 400
    assert client.post("/analyze", json={}).status_code == 400
    assert client.post("/analyze", json={"text": 5}).status_code == 400
    assert client.post("/analyze", json={"text": "x" * (C.MAX_CHARS + 1)}).status_code == 413
    r = client.post("/analyze", json={"text": ["secret-marker"]})
    assert "secret-marker" not in r.text   # errors never echo input


def _rows(b): return list(csv.reader(io.StringIO(b.decode())))


def test_batch_roundtrip_preserves_rows_and_columns(client):
    src = "id,content\n1,\"" + T + "\"\n2,Your appointment at the clinic is confirmed for Tuesday at 10:00.\n3,\n4,\"multi\nline, with comma\"\n"
    r = client.post("/batch", content=src.encode(), headers={"content-type": "text/csv"})
    rows = _rows(r.content)
    assert r.status_code == 200 and rows[0] == ["label", "type", "risk", "explanation", "action"] and len(rows) == 5
    assert rows[1][0] == "Suspicious" and rows[2][0] == "Benign" and rows[3][0] == "Unknown"


def test_batch_multipart_and_headerless_and_errors(client):
    r = client.post("/batch", files={"file": ("x.csv", b"content\n" + T.encode())})
    assert r.status_code == 200 and len(_rows(r.content)) == 2
    assert client.post("/batch", content=b"single line message", headers={"content-type": "text/csv"}).status_code == 200
    assert client.post("/batch", content=b"a,b\n1,2\n", headers={"content-type": "text/csv"}).status_code == 400
    assert client.post("/batch", content=b"", headers={"content-type": "text/csv"}).status_code == 400
    assert client.post("/batch", content=b"x" * (C.MAX_BATCH_BYTES + 1), headers={"content-type": "text/csv"}).status_code == 413


def test_batch_formula_injection_and_odd_encoding(client):
    r = client.post("/batch", content=b"text\n=HYPERLINK(\"http://x\")\n\xff\xfe bad bytes\n", headers={"content-type": "text/csv"})
    assert r.status_code == 200
    assert all(not c[:1] in "=+-@" for row in _rows(r.content)[1:] for c in row if c)


def test_batch_include_input(client):
    r = client.post("/batch?include_input=true", content=b"content\nhello there\n", headers={"content-type": "text/csv"})
    assert _rows(r.content)[0][-1] == "input_row"
