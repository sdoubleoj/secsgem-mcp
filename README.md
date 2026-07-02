# SECS/GEM MCP Server

WM-811K / MixedWM38 웨이퍼맵과 SECS/GEM 시뮬레이터 기반 합성 공정·장비 데이터를
lot/wafer 키로 결합해 제공하는 인스턴스 수준 RCA용 MCP 서버.
(설계 근거: secgem_mcp_dev.md)

## 설치

    python3.11 -m venv .venv && source .venv/bin/activate
    pip install -e . && pip install pytest pyyaml kaggle

## 데이터 준비 (원천 데이터는 배포에 미포함)

    # WM-811K — MIR Lab 공식 배포본
    wget -P .. http://mirlab.org/dataSet/public/MIR-WM811K.zip
    unzip ../MIR-WM811K.zip -d ..
    cp ../MIR-WM811K/Python/WM811K.pkl datasets/raw/

    # MixedWM38 — Kaggle (kaggle CLI 인증 필요)
    # https://www.kaggle.com/datasets/co1d7era/mixedtype-wafer-defect-datasets
    kaggle datasets download -d co1d7era/mixedtype-wafer-defect-datasets -p ../MixedWM38 --unzip
    cp ../MixedWM38/Wafer_Map_Datasets.npz datasets/raw/

    # 합성 fab 데이터 빌드 (시드 고정 — byte-identical 재현)
    python -m simulator.generate --wm811k datasets/raw/WM811K.pkl \
      --mw38 datasets/raw/Wafer_Map_Datasets.npz --out datasets --seed 20260101

## 서버 실행 / MCP 등록

    python -m server.main                      # stdio 서버 (직접 기동 시)

    # Claude Code 등록 — 절대경로 주입으로 어느 디렉토리에서든 동작
    claude mcp add secsgem \
      -e PYTHONPATH=$(pwd) -e FAB_DB=$(pwd)/datasets/fab.db \
      -- python -m server.main

## 툴 목록 (9종)

get_wafer_map · get_lot_history · run_commonality_analysis · get_normal_lot_ratio ·
query_telemetry · get_alarm_history · get_maintenance_history · detect_change_points ·
get_lot_timeline — 상세 스키마는 `server/tools/` 참조.

## 테스트

    pytest -q -m "not data"    # 데이터 없이 도는 단위 테스트 (CI와 동일)
    pytest -q                  # 데이터 빌드 후 전체 회귀

## 범위

전공정~wafer test(EDS)로 한정. 패키징 이후 미지원(secgem_mcp_dev.md §1.2).
합성 데이터: "인과 구조가 알려진 통제 환경에서의 에이전트 추론 평가"용(§10).
