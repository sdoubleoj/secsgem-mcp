import pytest

@pytest.mark.parametrize("scenario_id, expect", [
    ("SC-EDGE-RING-01", "adopt_etch"),      # 지지 신호 → 식각 채택
    ("SC-TRAP-01",      "reject_trap"),     # 함정 → 기각
    ("SC-UNMATCHED-01", "judge_unknown"),   # 매칭불가 → 판단불가+확인항목
])
def test_end_to_end(scenario_id, expect, run_pipeline):
    out = run_pipeline(scenario_id)
    assert out.verdict == expect
    assert out.has_next_actions_section