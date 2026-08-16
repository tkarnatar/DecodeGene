"""Pydantic models for DecodeGene (大众化通俗模式 + 专业科研模式 dual schema)."""
from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class GeneEntity(BaseModel):
    symbol: str
    name: str = ""
    chinese_name: str = ""
    chromosome: str = ""
    metaphor_title: str = ""
    metaphor_story: str = ""
    plain_summary: str = ""
    academic_summary: str = ""
    metaphor_title_en: str = ""
    metaphor_story_en: str = ""
    plain_summary_en: str = ""


class DiseaseEntity(BaseModel):
    id: str = ""
    name: str = ""
    chinese_name: str = ""
    category: str = ""
    categories: List[str] = Field(default_factory=list)
    severity_level: str = ""
    severity_badge: str = ""
    common_symptoms: List[str] = Field(default_factory=list)


class Evidence(BaseModel):
    overall_score: float = 0.0
    plain_rating: str = ""
    professional_rating: str = ""
    star_rating: int = 0
    clinvar_pathogenic_count: int = 0
    clinvar_summary_chinese: str = ""
    opentargets_score: float = 0.0


class LifestylePrevention(BaseModel):
    screening_advice: str = ""
    lifestyle_tips: List[str] = Field(default_factory=list)
    screening_advice_en: str = ""
    lifestyle_tips_en: List[str] = Field(default_factory=list)


class DoctorChecklist(BaseModel):
    gene_symbol: str = ""
    disease_name: str = ""
    recommended_specialty: str = ""
    key_questions: List[str] = Field(default_factory=list)
    screening_tests: List[str] = Field(default_factory=list)
    key_questions_en: List[str] = Field(default_factory=list)


class MythBuster(BaseModel):
    myth: str = ""
    truth: str = ""
    myth_en: str = ""
    truth_en: str = ""


class GeneDiseaseAssociation(BaseModel):
    association_id: str = ""
    gene: GeneEntity
    disease: DiseaseEntity
    evidence: Evidence = Field(default_factory=Evidence)
    lifestyle_prevention: LifestylePrevention = Field(default_factory=LifestylePrevention)
    doctor_checklist: DoctorChecklist = Field(default_factory=DoctorChecklist)
    myth_buster: Optional[MythBuster] = None


class GeneticReportQuery(BaseModel):
    raw_text: str = ""
    detected_gene: Optional[str] = None
    detected_variant: Optional[str] = None
    zygosity: Optional[str] = None


class ChatRequest(BaseModel):
    message: str = ""


class FamilyInheritanceQuery(BaseModel):
    pattern: Literal["AD", "AR", "XR", "XD"] = "AD"
    father_status: Literal["affected", "carrier", "normal"] = "normal"
    mother_status: Literal["affected", "carrier", "normal"] = "normal"


class SexRisk(BaseModel):
    disease_risk_pct: float = 0.0
    carrier_risk_pct: float = 0.0
    normal_pct: float = 0.0


class FamilyInheritanceResult(BaseModel):
    pattern: str = "AD"
    father_status: str = "normal"
    mother_status: str = "normal"
    child_disease_risk_pct: float = 0.0
    child_carrier_risk_pct: float = 0.0
    child_normal_pct: float = 0.0
    plain_explanation: str = ""
    by_sex: Optional[Dict[str, SexRisk]] = None
    recommendations: List[str] = Field(default_factory=list)


class ReportExplanation(BaseModel):
    what_found: str = ""
    actual_impact: str = ""
    next_steps: str = ""
    lifestyle: str = ""
    disclaimer: str = ""
    model: Optional[str] = None
    offline_fallback: bool = False


def association_from_dict(data: dict) -> GeneDiseaseAssociation:
    """Map the raw demo JSON dictionary into the typed schema."""
    gene = data.get("gene") or {}
    disease = data.get("disease") or {}
    evidence = data.get("evidence") or {}
    prev = data.get("lifestyle_prevention") or {}
    chk = data.get("doctor_checklist") or {}
    myth = data.get("myth_buster")
    metaphor = gene.get("metaphor") or {}

    severity = disease.get("severity_level") or disease.get("severity_badge") or ""

    screening_tests = list(chk.get("screening_tests") or [])
    if prev.get("screening_advice") and prev["screening_advice"] not in screening_tests:
        screening_tests.insert(0, prev["screening_advice"])

    return GeneDiseaseAssociation(
        association_id=data.get("association_id")
        or f"GDA_{gene.get('symbol', 'UNKNOWN')}",
        gene=GeneEntity(
            symbol=gene.get("symbol", ""),
            name=gene.get("name", gene.get("symbol", "")),
            chinese_name=gene.get("chinese_name", ""),
            chromosome=gene.get("chromosome", ""),
            metaphor_title=metaphor.get("title", gene.get("metaphor_title", "")),
            metaphor_story=metaphor.get("story", gene.get("metaphor_story", "")),
            plain_summary=gene.get("plain_summary", ""),
            academic_summary=gene.get("academic_summary", ""),
        ),
        disease=DiseaseEntity(
            id=disease.get("id", ""),
            name=disease.get("name", ""),
            chinese_name=disease.get("chinese_name", ""),
            category=(disease.get("categories") or [""])[0],
            categories=disease.get("categories", []),
            severity_level=severity,
            severity_badge=disease.get("severity_badge", severity),
            common_symptoms=disease.get("common_symptoms", []),
        ),
        evidence=Evidence(
            overall_score=float(evidence.get("overall_score", 0.0)),
            plain_rating=evidence.get("plain_rating", ""),
            professional_rating=evidence.get(
                "professional_rating", evidence.get("plain_rating", "")
            ),
            star_rating=int(evidence.get("star_rating", 0)),
            clinvar_pathogenic_count=int(
                evidence.get("clinvar_pathogenic_count", 0)
            ),
            clinvar_summary_chinese=evidence.get("clinvar_summary_chinese", ""),
            opentargets_score=float(evidence.get("opentargets_score", 0.0)),
        ),
        lifestyle_prevention=LifestylePrevention(
            screening_advice=prev.get("screening_advice", ""),
            lifestyle_tips=prev.get("lifestyle_tips", []),
        ),
        doctor_checklist=DoctorChecklist(
            gene_symbol=gene.get("symbol", ""),
            disease_name=disease.get("chinese_name", disease.get("name", "")),
            recommended_specialty=chk.get("specialty", chk.get("recommended_specialty", "")),
            key_questions=chk.get("questions", chk.get("key_questions", [])),
            screening_tests=screening_tests,
        ),
        myth_buster=MythBuster(**myth) if myth else None,
    )
