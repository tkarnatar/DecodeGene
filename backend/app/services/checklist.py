"""就诊提问清单生成器 (ChecklistService).

根据基因与疾病，自动生成面向临床医生的《门诊就医提问清单》与筛查建议，
支持一键复制 / 打印。
"""
from __future__ import annotations

from typing import Optional

from ..core.database import kb
from ..models.schema import DoctorChecklist


class ChecklistService:
    def __init__(self, knowledge_base=None) -> None:
        self.kb = knowledge_base or kb

    def generate(self, gene_symbol: str) -> Optional[DoctorChecklist]:
        assoc = self.kb.get_by_symbol(gene_symbol)
        if assoc is None:
            return None
        return assoc.doctor_checklist

    def render_checklist(self, gene_symbol: str) -> str:
        """Render a printable, copy-friendly text card."""
        assoc = self.kb.get_by_symbol(gene_symbol)
        if assoc is None:
            return f"未找到基因 {gene_symbol} 的就医清单数据。"
        cl = assoc.doctor_checklist
        lines = [
            "📋 【DecodeGene 专属就医提问卡】（可直接截图或给医生看）",
            f"关注基因/疾病: {assoc.gene.symbol} {assoc.gene.chinese_name} / {cl.disease_name}",
            f"推荐就诊科室: {cl.recommended_specialty}",
            "",
            "—— 就诊时您可以这样问 ——",
        ]
        for i, q in enumerate(cl.key_questions, 1):
            lines.append(f"{i}. {q}")
        lines.append("")
        lines.append("—— 筛查与检查建议 ——")
        for i, t in enumerate(cl.screening_tests, 1):
            lines.append(f"{i}. {t}")
        lines.append("")
        lines.append("⚠️ 本清单仅供参考，请以执业医师的专业意见为准。")
        return "\n".join(lines)
