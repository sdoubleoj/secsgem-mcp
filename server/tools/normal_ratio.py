"""P3 — Negative evidence 전용"""
from server.schemas import respond
from server.db import query

def register(mcp):
    @mcp.tool()
    def get_normal_lot_ratio(equipment_id: str | None = None,
                             chamber_id: str | None = None,
                             time_range: tuple[str, str] | None = None) -> dict:
        """의심 장비를 지나간 정상 lot 모수. 가설 기각 근거 (P3)"""
        assert equipment_id or chamber_id, "equipment_id 또는 chamber_id 필수"
        col, val = ("equipment_id", equipment_id) if equipment_id else ("chamber", chamber_id)
        sql = (f"SELECT w.is_normal, COUNT(DISTINCT h.lot_id) c "
               f"FROM lot_history h JOIN wafer w USING(lot_id) "
               f"WHERE h.{col}=? " +
               ("AND h.ts_in BETWEEN ? AND ? " if time_range else "") +
               "GROUP BY w.is_normal")
        args = (val, *time_range) if time_range else (val,)
        rows = {bool(r["is_normal"]): r["c"] for r in query(sql, args)}
        normal, defect = rows.get(True, 0), rows.get(False, 0)
        total = normal + defect
        return respond({
            col: val, "normal_lots": normal, "defect_lots": defect,
            "total_lots": total,
            "normal_ratio": round(normal / total, 3) if total else None,
        }, queried=str(time_range) if time_range else None,
           missing=[] if total else [f"{val} 통과 lot 없음"])