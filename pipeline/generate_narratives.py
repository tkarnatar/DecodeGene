"""用 DeepSeek 為批量基因生成白話敘事（生活比喻、摘要、篩檢建議、就醫提問、辟謠）。

設計原則（grounded generation）：
  * 只根據 ClinVar 提供的證據輸入撰寫敘事，**不覆寫任何機器證據欄位**。
  * 嚴禁 AI 編造具體藥物名、確切篩檢年齡、確切百分比。
  * 增量存檔 + 斷點續跑：中斷後重跑會自動跳過已完成基因。

用法::

    python -m pipeline.generate_narratives --dry-run               # 只預覽不呼叫 API
    python -m pipeline.generate_narratives --limit 10              # 先測試前 10 個
    python -m pipeline.generate_narratives --genes NF1,TTN,ATM     # 指定基因
    python -m pipeline.generate_narratives                         # 全部

輸出 ``data/processed/bulk_narratives.json``，由後端在載入時自動合併進知識庫。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
BACKEND_ENV = ROOT / "backend" / ".env"
BULK_PATH = ROOT / "data" / "processed" / "bulk_associations.json"
OUT_PATH = ROOT / "data" / "processed" / "bulk_narratives.json"

load_dotenv(BACKEND_ENV)

for _stream in (sys.stdout, sys.stderr):
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").rstrip("/")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

SYSTEM_PROMPT = (
    "你是一名資深臨床遺傳諮詢師與頂級基因科普作家。你的任務是為「基因-疾病」條目"
    "撰寫面向大眾的白話解釋（生活比喻、摘要、篩檢建議、就醫提問、辟謠）。\n"
    "語氣要求：溫和、客觀、極度通俗，嚴禁未加解釋的晦澀術語，堅決避免引發基因焦慮。\n"
    "嚴格的「有根據生成」規則：\n"
    "1. 只根據使用者提供的「證據輸入」撰寫，不得編造證據中沒有的資訊。\n"
    "2. 嚴禁編造具體藥物名稱、確切篩檢年齡、確切百分比數字、具體劑量。\n"
    "   篩檢建議一律使用安全表述，例如「建議諮詢專科醫師制定個體化篩檢方案」。\n"
    "3. 生活比喻要生動貼近日常，但不得誤導（不得暗示「必然得病」）。\n"
    "4. 不得把「易感/風險升高」說成「一定會生病」。\n"
    "5. 辟謠的「真相」必須符合主流醫學共識，不誇大。"
)

OUTPUT_SCHEMA = {
    "chinese_name": "基因中文名（若無法確認可留空字串）",
    "metaphor_title": "生活比喻標題，含一個 emoji，例如「🧬 細胞裡的【DNA 維修工】」",
    "metaphor_story": "生活比喻故事，3-5 句，用日常事物解釋該基因的功能與突變後果",
    "plain_summary": "白話摘要，2-3 句，說明攜帶突變的實際意義，不製造焦慮",
    "screening_advice": "篩檢建議，安全表述，不編造年齡或檢查細節",
    "lifestyle_tips": ["生活建議 1", "生活建議 2", "生活建議 3"],
    "key_questions": ["就醫時可問醫生的問題 1", "問題 2", "問題 3"],
    "myth": "大眾常見迷思（用引號包起來的問句）",
    "truth": "科學真相，用「不是」或「錯」開頭糾正迷思",
}


def build_user_prompt(evidence: Dict[str, Any]) -> str:
    return (
        "請為下列基因-疾病條目撰寫白話敘事。\n\n"
        "【證據輸入】（這些是權威事實，請據此撰寫，勿編造）：\n"
        f"{json.dumps(evidence, ensure_ascii=False, indent=2)}\n\n"
        "【輸出格式】只輸出一個 JSON 物件，欄位如下（皆為簡體中文字串或字串陣列）：\n"
        f"{json.dumps(OUTPUT_SCHEMA, ensure_ascii=False, indent=2)}\n\n"
        "請嚴格只輸出 JSON，不要輸出任何多餘文字或 markdown 代碼框。"
    )


def load_bulk() -> List[Dict[str, Any]]:
    if not BULK_PATH.exists():
        print(f"[red]找不到批量資料: {BULK_PATH}[/red]")
        return []
    return json.loads(BULK_PATH.read_text(encoding="utf-8"))


def evidence_of(assoc: Dict[str, Any]) -> Dict[str, Any]:
    gene = assoc.get("gene", {})
    disease = assoc.get("disease", {})
    ev = assoc.get("evidence", {})
    return {
        "gene_symbol": gene.get("symbol", ""),
        "disease_name": disease.get("name", ""),
        "clinvar_pathogenic_count": ev.get("clinvar_pathogenic_count", 0),
        "star_rating": ev.get("star_rating", 0),
        "severity_badge": disease.get("severity_badge", ""),
    }


async def generate_one(
    symbol: str,
    evidence: Dict[str, Any],
    client: httpx.AsyncClient,
    sem: asyncio.Semaphore,
) -> Optional[Dict[str, Any]]:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(evidence)},
        ],
        "temperature": 0.4,
        "stream": False,
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    async with sem:
        for attempt in range(3):
            try:
                resp = await client.post(
                    f"{BASE_URL}/chat/completions", json=payload, headers=headers
                )
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"]
                data = json.loads(content)
                data["generated_by"] = MODEL
                return data
            except Exception as exc:  # noqa: BLE001
                await asyncio.sleep(2 * (attempt + 1))
        print(f"  [red]失敗: {symbol}[/red] ({exc})")
        return None


def load_existing() -> Dict[str, Any]:
    if OUT_PATH.exists():
        try:
            return json.loads(OUT_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


async def run(
    limit: Optional[int],
    genes: Optional[List[str]],
    dry_run: bool,
    concurrency: int,
    force: bool,
) -> None:
    associations = load_bulk()
    if not associations:
        return
    associations.sort(
        key=lambda a: a.get("evidence", {}).get("clinvar_pathogenic_count", 0), reverse=True
    )

    if genes:
        wanted = set(genes)
        associations = [a for a in associations if a["gene"]["symbol"] in wanted]
    if limit:
        associations = associations[:limit]

    if dry_run:
        print(f"[cyan]DRY-RUN: 共 {len(associations)} 個基因待處理[/cyan]")
        if associations:
            print("範例使用者 prompt：\n")
            print(build_user_prompt(evidence_of(associations[0])))
        return

    if not API_KEY:
        print("[red]未偵測到 DEEPSEEK_API_KEY。[/red]")
        print("請在 backend/.env 設定 DEEPSEEK_API_KEY，或使用 --dry-run 預覽。")
        return

    existing = {} if force else load_existing()
    todo = [a for a in associations if a["gene"]["symbol"] not in existing]
    print(f"待處理 {len(todo)} / 總計 {len(associations)} 個基因（已完成 {len(existing)}）")

    sem = asyncio.Semaphore(concurrency)
    done_since_save = 0

    async with httpx.AsyncClient(timeout=120.0) as client:
        for assoc in todo:
            symbol = assoc["gene"]["symbol"]
            narrative = await generate_one(symbol, evidence_of(assoc), client, sem)
            if narrative is None:
                continue
            existing[symbol] = narrative
            done_since_save += 1
            print(f"  [green]✔ {symbol}[/green]  ({done_since_save}/{len(todo)})")
            if done_since_save % 25 == 0:
                OUT_PATH.write_text(
                    json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8"
                )

    OUT_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[bold green]完成，共 {len(existing)} 個基因已寫入: {OUT_PATH}[/bold green]")


def main() -> None:
    parser = argparse.ArgumentParser(description="用 DeepSeek 生成批量基因白話敘事")
    parser.add_argument("--limit", type=int, default=None, help="只處理前 N 個基因（測試用）")
    parser.add_argument("--genes", type=str, default=None, help="逗號分隔的基因符號")
    parser.add_argument("--dry-run", action="store_true", help="只預覽 prompt，不呼叫 API")
    parser.add_argument("--concurrency", type=int, default=3, help="並發請求數 (預設 3)")
    parser.add_argument("--force", action="store_true", help="重新生成已完成的基因")
    args = parser.parse_args()

    genes = [g.strip() for g in (args.genes or "").split(",") if g.strip()]
    asyncio.run(
        run(
            limit=args.limit,
            genes=genes or None,
            dry_run=args.dry_run,
            concurrency=args.concurrency,
            force=args.force,
        )
    )


if __name__ == "__main__":
    main()
