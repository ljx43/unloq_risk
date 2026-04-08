from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pandas as pd


@dataclass(frozen=True)
class Company:
    company_name: str
    jurisdiction: str | None = None
    company_number: str | None = None
    aliases: list[str] | None = None


def _now_iso_shanghai() -> str:
    sh_tz = timezone(timedelta(hours=8))
    return datetime.now(tz=sh_tz).isoformat(timespec="seconds")


def _domain(url: str) -> str:
    try:
        return (urlparse(url).netloc or "").lower()
    except Exception:
        return ""


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _load_input(path: Path) -> list[Company]:
    data = json.loads(path.read_text(encoding="utf-8"))
    companies = data.get("companies")
    if not isinstance(companies, list) or not companies:
        raise ValueError("input JSON must contain non-empty 'companies' list")

    out: list[Company] = []
    for c in companies:
        if not isinstance(c, dict) or not c.get("company_name"):
            raise ValueError("each companies[] item must include company_name")
        out.append(
            Company(
                company_name=str(c["company_name"]),
                jurisdiction=(str(c["jurisdiction"]) if c.get("jurisdiction") else None),
                company_number=(str(c["company_number"]) if c.get("company_number") else None),
                aliases=(list(c.get("aliases") or []) or None),
            )
        )
    return out


def build_run(companies: list[Company]) -> dict[str, Any]:
    """Builds a monitoring run.

    Note: this is a *demo runner* that outputs the required Excel/JSON structure.
    The evidence/events are currently seeded for a few sample companies only.
    """

    run_id = f"nem_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    retrieval_timestamp = _now_iso_shanghai()

    raw_evidence: list[dict[str, Any]] = []

    def add_evidence(
        *,
        company: Company,
        query_group: str,
        search_query: str,
        source_type: str,
        title: str,
        url: str,
        snippet: str,
        raw_text: str,
        event_date: str | None = None,
        publish_date: str | None = None,
        initial_relevance: str = "medium",
        initial_risk_hint: str | None = None,
        language: str = "en",
    ) -> None:
        dedup_key = _sha256_hex(f"{company.company_name}|{url}|{title}")
        raw_evidence.append(
            {
                "run_id": run_id,
                "company_name": company.company_name,
                "jurisdiction": company.jurisdiction,
                "company_number": company.company_number,
                "query_group": query_group,
                "search_query": search_query,
                "source_website": _domain(url),
                "source_type": source_type,
                "title": title,
                "event_date": event_date,
                "publish_date": publish_date,
                "url": url,
                "snippet": snippet,
                "raw_text": raw_text,
                "language": language,
                "initial_relevance": initial_relevance,
                "initial_risk_hint": initial_risk_hint,
                "retrieval_timestamp": retrieval_timestamp,
                "dedup_key": dedup_key,
            }
        )

    deduped_events: list[dict[str, Any]] = []

    def add_event(
        *,
        company: Company,
        event_cluster_id: str,
        normalized_event: str,
        category: str,
        severity: str,
        signal_stage: str,
        event_date: str | None,
        first_seen_date: str | None,
        support_urls: list[str],
        source_websites: list[str],
        evidence_summary: str,
    ) -> None:
        deduped_events.append(
            {
                "run_id": run_id,
                "company_name": company.company_name,
                "event_cluster_id": event_cluster_id,
                "normalized_event": normalized_event,
                "category": category,
                "severity": severity,
                "signal_stage": signal_stage,
                "event_date": event_date,
                "first_seen_date": first_seen_date,
                "source_count": len(support_urls),
                "source_websites": ";".join(sorted(set(source_websites))),
                "support_urls": ";".join(support_urls),
                "evidence_summary": evidence_summary,
            }
        )

    # Seed evidence for known sample companies (safe demo data).
    by_name = {c.company_name: c for c in companies}

    if "BRAVADO LIMITED" in by_name:
        bravado = by_name["BRAVADO LIMITED"]
        add_evidence(
            company=bravado,
            query_group="legal_insolvency",
            search_query="BRAVADO LIMITED liquidation insolvency winding up",
            source_type="registry",
            title="BRAVADO LIMITED overview - Companies House",
            url="https://find-and-update.company-information.service.gov.uk/company/01584795",
            snippet="Company status shows 'Liquidation' (Companies House).",
            raw_text="Companies House overview indicates BRAVADO LIMITED (01584795) status: Liquidation.",
            publish_date=None,
            event_date=None,
            initial_relevance="high",
            initial_risk_hint="company_status_liquidation",
        )
        add_evidence(
            company=bravado,
            query_group="creditor_action",
            search_query="BRAVADO LIMITED creditors meeting statutory demand winding-up petition",
            source_type="legal_notice",
            title="BRAVADO LIMITED | Meetings of Creditors | The Gazette (5039673)",
            url="https://www.thegazette.co.uk/notice/5039673",
            snippet="Virtual meeting of creditors convened; nomination of liquidators.",
            raw_text="Notice states a virtual meeting of creditors would be held on 27 January 2026; purpose includes nomination of liquidators.",
            publish_date="2026-01-22",
            event_date="2026-01-27",
            initial_relevance="high",
            initial_risk_hint="creditors_meeting",
        )
        add_event(
            company=bravado,
            event_cluster_id="BRAVADO_001",
            normalized_event="Insolvent liquidation / voluntary winding-up with liquidators appointed",
            category="Legal / Insolvency",
            severity="High",
            signal_stage="default",
            event_date="2026-01-27",
            first_seen_date="2026-01-22",
            support_urls=[
                "https://www.thegazette.co.uk/notice/5039673",
                "https://find-and-update.company-information.service.gov.uk/company/01584795",
            ],
            source_websites=["thegazette.co.uk", "find-and-update.company-information.service.gov.uk"],
            evidence_summary="Gazette notices and Companies House status indicate insolvency and liquidation proceedings.",
        )

    df_raw = pd.DataFrame(raw_evidence)
    df_events = pd.DataFrame(deduped_events)

    def highest_severity(sevs: list[str]) -> str | None:
        order = {"Low": 1, "Medium": 2, "High": 3}
        if not sevs:
            return None
        return max(sevs, key=lambda s: order.get(s, 0))

    run_summary_rows: list[dict[str, Any]] = []
    if not df_raw.empty:
        df_raw_company = df_raw["company_name"].astype(str)
    else:
        df_raw_company = pd.Series([], dtype=str)

    for company in companies:
        raw_hits = int((df_raw_company == company.company_name).sum())
        ev = df_events[df_events.get("company_name", pd.Series([], dtype=str)) == company.company_name]
        deduped = int(len(ev))
        high_risk = int((ev["severity"] == "High").sum()) if deduped else 0
        latest_event_date = None
        if deduped and ev["event_date"].notna().any():
            latest_event_date = ev["event_date"].dropna().astype(str).sort_values().iloc[-1]
        highest = highest_severity(ev["severity"].astype(str).tolist()) if deduped else None
        run_summary_rows.append(
            {
                "run_id": run_id,
                "company_name": company.company_name,
                "raw_hits": raw_hits,
                "deduped_events": deduped,
                "high_risk_events": high_risk,
                "latest_event_date": latest_event_date,
                "highest_severity": highest,
            }
        )
    df_summary = pd.DataFrame(run_summary_rows)

    # Company summaries JSON + alert text
    company_summaries: list[dict[str, Any]] = []
    alert_blocks: list[str] = []

    def overall_risk_for_company(company_name: str) -> str:
        ev = df_events[df_events.get("company_name", pd.Series([], dtype=str)) == company_name]
        if ev.empty:
            return "Low"
        sev = highest_severity(ev["severity"].astype(str).tolist())
        return sev or "Low"

    for company in companies:
        overall = overall_risk_for_company(company.company_name)
        ev = df_events[df_events.get("company_name", pd.Series([], dtype=str)) == company.company_name].copy()
        key_findings: list[dict[str, Any]] = []
        if not ev.empty:
            for _, row in ev.iterrows():
                src_sites = str(row.get("source_websites") or "").split(";")
                src_site = src_sites[0] if src_sites and src_sites[0] else None
                key_findings.append(
                    {
                        "event": row.get("normalized_event"),
                        "category": row.get("category"),
                        "severity": row.get("severity"),
                        "signal_stage": row.get("signal_stage"),
                        "event_date": row.get("event_date"),
                        "source_website": src_site,
                        "summary": row.get("evidence_summary"),
                    }
                )

        risk_implication = ""
        if company.company_name == "BRAVADO LIMITED":
            risk_implication = "Public notices indicate formal insolvency/liquidation signals."
        else:
            risk_implication = "No seeded evidence for this company in demo mode."

        key_signals: list[str] = []
        for f in key_findings:
            if f.get("event_date"):
                key_signals.append(f"{f['event']} ({f['event_date']})")
            elif f.get("event"):
                key_signals.append(str(f["event"]))

        sources = sorted(
            {
                site
                for raw in (ev["source_websites"].astype(str).tolist() if not ev.empty else [])
                for site in str(raw).split(";")
                if site
            }
        )

        recommended_alert_message = (
            f"{company.company_name} risk signals observed: "
            + ("; ".join(key_signals[:3]) if key_signals else "(none)")
            + "."
        )

        company_summaries.append(
            {
                "company_name": company.company_name,
                "overall_risk_level": overall,
                "key_findings": key_findings,
                "risk_implication": risk_implication,
                "recommended_alert_message": recommended_alert_message,
            }
        )

        alert_blocks.append(
            "\n".join(
                [
                    f"[Company] {company.company_name}",
                    f"Risk Level: {overall}",
                    "Key Signals: " + "; ".join(key_signals[:3]) if key_signals else "Key Signals: (none)",
                    f"Implication: {risk_implication}" if risk_implication else "Implication: (n/a)",
                    "Source Websites: " + "; ".join(sources) if sources else "Source Websites: (n/a)",
                ]
            )
        )

    return {
        "run_id": run_id,
        "retrieval_timestamp": retrieval_timestamp,
        "raw_evidence": df_raw,
        "deduped_events": df_events,
        "run_summary": df_summary,
        "company_summaries": company_summaries,
        "alert_text": "\n\n".join(alert_blocks),
    }


def _write_outputs(run: dict[str, Any], out_dir: Path) -> tuple[Path, Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    date_tag = datetime.now().strftime("%Y%m%d")
    xlsx_path = out_dir / f"negative_event_monitoring_{date_tag}.xlsx"
    json_path = out_dir / f"negative_event_summary_{date_tag}.json"
    alert_path = out_dir / f"negative_event_alerts_{date_tag}.txt"

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        run["raw_evidence"].to_excel(writer, index=False, sheet_name="raw_evidence")
        run["deduped_events"].to_excel(writer, index=False, sheet_name="deduped_events")
        run["run_summary"].to_excel(writer, index=False, sheet_name="run_summary")

    json_path.write_text(json.dumps(run["company_summaries"], ensure_ascii=False, indent=2), encoding="utf-8")
    alert_path.write_text(run["alert_text"], encoding="utf-8")

    return xlsx_path, json_path, alert_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="input.json", help="Input JSON matching the skill schema")
    parser.add_argument("--out-dir", default="output", help="Output directory")
    args = parser.parse_args()

    companies = _load_input(Path(args.input))
    run = build_run(companies)
    xlsx_path, json_path, alert_path = _write_outputs(run, Path(args.out_dir))

    print(str(xlsx_path))
    print(str(json_path))
    print(str(alert_path))


if __name__ == "__main__":
    main()
