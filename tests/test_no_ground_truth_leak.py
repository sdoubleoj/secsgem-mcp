import pathlib, re

def test_server_never_imports_ground_truth():
    for p in pathlib.Path("server").rglob("*.py"):
        src = p.read_text(encoding="utf-8")
        assert "ground_truth" not in src, f"{p}가 ground_truth를 참조함 — 정답 노출 위험"
        

# 실행 스크립트
# pytest tests/test_no_ground_truth_leak.py -q