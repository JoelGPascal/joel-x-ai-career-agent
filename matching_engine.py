"""JOEL X Career Matching Engine v0.1 — heuristic prototype, not a calibrated probability."""
import json
import re
from typing import Dict, Any

CANDIDATE_PROFILE = {
    "name": "Joel Gabriel Pascal",
    "citizenship": ["UK", "Israel"],
    "languages": ["English (Native)", "French (Fluent)"],
    "location_base": "Tel Aviv, Israel (EMEA Timezone)",
    "metrics": {
        "closed_revenue": "$4M+",
        "webz_closed": "$2.5M+",
        "webz_quota": "118%",
        "guesty_closed": "$1.5M+",
        "guesty_quota": "112%",
        "pipeline_generated": "$3.5M+",
    },
    "technical_skills": [
        "API Sales", "REST APIs", "Webhooks", "GoHighLevel", "Python",
        "Model Context Protocol (MCP)", "Cloudflare Workers", "GitHub",
        "CRM Architecture", "Postman", "Technical POCs",
    ],
    "target_markets": ["EMEA", "UK", "France", "North America", "APAC"],
}


class MatchingEngine:
    def __init__(self, profile: Dict[str, Any]):
        self.profile = profile

    def evaluate_jd(self, jd_text: str) -> Dict[str, Any]:
        jd_lower = jd_text.lower()
        tech_matches = [
            skill for skill in self.profile["technical_skills"]
            if skill.lower() in jd_lower
        ]
        french_required = any(
            re.search(r"\b" + re.escape(k) + r"\b", jd_lower)
            for k in ["french", "france", "francophone"]
        )
        uk_emea_required = any(
            re.search(r"\b" + re.escape(k) + r"\b", jd_lower)
            for k in ["uk", "emea", "europe", "remote emea"]
        )
        api_tech_sale = any(
            re.search(r"\b" + re.escape(k) + r"\b", jd_lower)
            for k in ["api", "developer", "data", "technical", "poc", "saas"]
        )
        score = 50
        if tech_matches:
            score += min(len(tech_matches) * 5, 20)
        if french_required:
            score += 15
        if uk_emea_required:
            score += 10
        if api_tech_sale:
            score += 5
        score = min(score, 98)

        if any(k in jd_lower for k in ["api", "developer", "security"]):
            recommended_cv = "CV D (Technical Commercial / API / Cyber)"
        elif any(k in jd_lower for k in ["startup", "founding", "operator"]):
            recommended_cv = "CV B (GTM / Startup Operator)"
        else:
            recommended_cv = "CV A (Enterprise SaaS / Strategic Sales)"

        return {
            "heuristic_score": score,
            "score_note": "Rule-based ranking only; not a hiring probability or eligibility check.",
            "recommended_cv": recommended_cv,
            "matched_skills": tech_matches,
            "french_advantage": french_required,
            "emea_alignment": uk_emea_required,
            "leveraged_metrics": [
                f"$2.5M+ closed at Webz.io ({self.profile['metrics']['webz_quota']} quota)",
                f"$1.5M+ closed at Guesty ({self.profile['metrics']['guesty_quota']} quota, French market launch)",
                "$3.5M+ self-sourced enterprise pipeline",
            ],
        }


if __name__ == "__main__":
    print("=== JOEL X CAREER MATCHING ENGINE v0.1 initialized ===")
    sample_jd = """
    We are looking for an Enterprise Account Executive to drive EMEA expansion.
    Experience selling complex APIs, data platforms, or SaaS required.
    Fluent French is a strong plus. Must be comfortable running technical POCs
    and managing 3-9 month sales cycles. UK/EMEA remote friendly.
    """
    engine = MatchingEngine(CANDIDATE_PROFILE)
    results = engine.evaluate_jd(sample_jd)
    print("\n[MATCHING EVALUATION RESULTS]")
    print(json.dumps(results, indent=2))
