"""REST 接口: 基因检索、通俗/专业视图、遗传概率计算、就医清单、辟谣、AI 翻译."""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from ...core.config import settings
from ...core.database import kb
from ...models.schema import (
    ChatRequest,
    FamilyInheritanceQuery,
    FamilyInheritanceResult,
    GeneDiseaseAssociation,
    GeneticReportQuery,
    ReportExplanation,
)
from ...services.ai_reasoning import DeepSeekPublicAgent
from ...services.checklist import ChecklistService
from ...services.inheritance import InheritanceCalculator

router = APIRouter()

calculator = InheritanceCalculator()
checklist_service = ChecklistService(kb)
agent = DeepSeekPublicAgent(settings)


def _render_association(assoc: GeneDiseaseAssociation, view: str = "simple") -> Dict[str, Any]:
    """Render an association in either 通俗模式 (simple) or 专业模式 (pro)."""
    if view == "pro":
        return {
            "association_id": assoc.association_id,
            "gene": {
                "symbol": assoc.gene.symbol,
                "name": assoc.gene.name,
                "chinese_name": assoc.gene.chinese_name,
                "chromosome": assoc.gene.chromosome,
                "academic_summary": assoc.gene.academic_summary,
            },
            "disease": {
                "id": assoc.disease.id,
                "name": assoc.disease.name,
                "chinese_name": assoc.disease.chinese_name,
            },
            "evidence": {
                "overall_score": assoc.evidence.overall_score,
                "opentargets_score": assoc.evidence.opentargets_score,
                "clinvar_pathogenic_count": assoc.evidence.clinvar_pathogenic_count,
                "professional_rating": assoc.evidence.professional_rating,
            },
        }
    return {
        "association_id": assoc.association_id,
        "gene": {
            "symbol": assoc.gene.symbol,
            "chinese_name": assoc.gene.chinese_name,
            "chromosome": assoc.gene.chromosome,
            "metaphor_title": assoc.gene.metaphor_title,
            "metaphor_story": assoc.gene.metaphor_story,
            "plain_summary": assoc.gene.plain_summary,
        },
        "disease": {
            "id": assoc.disease.id,
            "name": assoc.disease.name,
            "chinese_name": assoc.disease.chinese_name,
            "categories": assoc.disease.categories,
            "severity_badge": assoc.disease.severity_badge,
        },
        "evidence": {
            "plain_rating": assoc.evidence.plain_rating,
            "star_rating": assoc.evidence.star_rating,
            "clinvar_summary_chinese": assoc.evidence.clinvar_summary_chinese,
        },
        "lifestyle_prevention": {
            "screening_advice": assoc.lifestyle_prevention.screening_advice,
            "lifestyle_tips": assoc.lifestyle_prevention.lifestyle_tips,
        },
        "doctor_checklist": {
            "gene_symbol": assoc.doctor_checklist.gene_symbol,
            "disease_name": assoc.doctor_checklist.disease_name,
            "recommended_specialty": assoc.doctor_checklist.recommended_specialty,
            "key_questions": assoc.doctor_checklist.key_questions,
            "screening_tests": assoc.doctor_checklist.screening_tests,
        },
        "myth_buster": assoc.myth_buster.model_dump() if assoc.myth_buster else None,
    }


@router.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ai_enabled": agent.available,
        "associations": len(kb.associations),
    }


@router.get("/associations")
def list_associations() -> List[Dict[str, Any]]:
    return [_render_association(a, "simple") for a in kb.associations]


@router.get("/genes/{symbol}")
def get_gene(symbol: str, view: str = Query("simple")) -> Dict[str, Any]:
    assoc = kb.get_by_symbol(symbol)
    if assoc is None:
        raise HTTPException(status_code=404, detail=f"未找到基因 {symbol}")
    return _render_association(assoc, view)


@router.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(10, le=50)) -> Dict[str, Any]:
    results = kb.search(q, limit)
    return {
        "query": q,
        "count": len(results),
        "results": [_render_association(a, "simple") for a in results],
    }


@router.post("/calculate/inheritance", response_model=FamilyInheritanceResult)
def calculate_inheritance(query: FamilyInheritanceQuery) -> FamilyInheritanceResult:
    return calculator.calculate(query)


@router.get("/checklist/{gene_symbol}")
def get_checklist(gene_symbol: str) -> Dict[str, Any]:
    checklist = checklist_service.generate(gene_symbol)
    if checklist is None:
        raise HTTPException(status_code=404, detail=f"未找到基因 {gene_symbol} 的就医清单")
    return checklist.model_dump()


@router.get("/checklist/{gene_symbol}/text")
def get_checklist_text(gene_symbol: str) -> Dict[str, str]:
    text = checklist_service.render_checklist(gene_symbol)
    return {"text": text}


@router.get("/myths")
def list_myths() -> List[Dict[str, Any]]:
    return [
        {"gene": a.gene.symbol, "chinese_name": a.gene.chinese_name, **a.myth_buster.model_dump()}
        for a in kb.associations
        if a.myth_buster is not None
    ]


@router.post("/report/explain", response_model=ReportExplanation)
async def explain_report(query: GeneticReportQuery) -> ReportExplanation:
    return await agent.explain_report(query)


@router.post("/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        agent.chat_qa_stream(req.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
