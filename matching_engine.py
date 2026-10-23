"""JOEL X v0.2 — rule-based evidence alignment; not verified hiring eligibility."""
import json
from typing import Dict, Any

# Candidate-provided profile; independently verify claims before external use.
CANDIDATE_PROFILE = {
    "identity": {
        "name": "Joel Gabriel Pascal",
        "citizenships": ["UK", "Israel"],
        "tax_residency": "Israel",
        "timezone": "UTC+2 / UTC+3",
        "languages": {"English": "Native", "French": "Fluent"},
    },
    "commercial_evidence": {
        "total_closed_revenue": "$4M+",
        "webz_io": {"closed": "$2.5M+", "quota_attainment": 1.18, "domain": "Enterprise Data & APIs"},
        "guesty": {"closed": "$1.5M+", "quota_attainment": 1.12, "domain": "SaaS / Market Expansion"},
        "self_sourced_pipeline": "$3.5M+",
    },
    "technical_capabilities": [
        "API Sales", "REST APIs", "Webhooks", "GoHighLevel", "Python",
        "Model Context Protocol (MCP)", "Cloudflare Workers", "GitHub",
        "CRM Architecture", "Technical Discovery", "POC Management",
    ],
}


class EvidenceBasedMatchingEngine:
    def __init__(self, candidate: Dict[str, Any]):
        self.candidate = candidate

    def verify_eligibility(self, jd_text: str) -> Dict[str, Any]:
        jd_lower = jd_text.lower()
        restrictions = [
            "must reside in the uk", "uk tax resident required",
            "us tax resident required", "must be based in france",
        ]
        requires_local_residency = any(p in jd_lower for p in restrictions)
        emea_compatible = any(
            p in jd_lower for p in
            ["emea", "europe", "utc", "uk", "london", "paris", "remote - europe"]
        )
        if requires_local_residency:
            return {
                "status": "REQUIRES_MANUAL_REVIEW",
                "reason": "A location or tax-residency restriction appears; verify its exact scope.",
            }
        if emea_compatible:
            return {
                "status": "POTENTIALLY_COMPATIBLE",
                "reason": "Possible timezone overlap. Employer hiring countries, residence and work authorization are unverified; UK citizenship alone is insufficient.",
            }
        return {
            "status": "UNKNOWN",
            "reason": "Insufficient location and employment eligibility evidence in the description.",
        }

    def evaluate_role(self, role_title: str, company: str, jd_text: str) -> Dict[str, Any]:
        jd_lower = jd_text.lower()
        eligibility = self.verify_eligibility(jd_text)

        # Keyword signals, not verified mandatory-qualification satisfaction.
        mandatory_criteria = {
            "Enterprise Sales / AE": any(k in jd_lower for k in ["account executive", "enterprise", "saas", "b2b"]),
            "Quota Track Record": any(k in jd_lower for k in ["quota", "track record", "closing", "revenue"]),
            "Technical / API Comfort": any(k in jd_lower for k in ["api", "data", "technical", "developer", "platform", "infrastructure"]),
        }
        mandatory_score = sum(mandatory_criteria.values()) / len(mandatory_criteria) * 60.0
        evidence_matches = []
        preferred_score = 0.0
        if any(k in jd_lower for k in ["french", "france", "francophone"]):
            preferred_score += 15
            evidence_matches.append("Reported fluent French; Guesty French market and quota figures require source verification.")
        if any(k in jd_lower for k in ["api", "data", "developer", "security", "infra"]):
            preferred_score += 15
            evidence_matches.append("Reported technical API sales; Webz.io revenue and quota figures require source verification.")
        if any(k in jd_lower for k in ["startup", "early stage", "operator", "founding", "automation"]):
            preferred_score += 10
            evidence_matches.append("GTM and technical project experience; verify specific implementation maturity.")
        preferred_score = min(preferred_score, 40.0)
        total_score = round(mandatory_score + preferred_score, 1)
        if eligibility["status"] == "REQUIRES_MANUAL_REVIEW":
            total_score = min(total_score, 40.0)

        if any(k in jd_lower for k in ["api", "developer", "security", "infrastructure"]):
            recommended_cv = "CV D (Technical Commercial / API / Cyber)"
        elif any(k in jd_lower for k in ["startup", "operator", "founding", "revops"]):
            recommended_cv = "CV B (GTM / Startup Operator)"
        else:
            recommended_cv = "CV A (Enterprise SaaS / Strategic Sales)"

        return {
            "target": {"company": company, "role": role_title},
            "eligibility_status": eligibility,
            "weighted_alignment_score": f"{total_score}%",
            "score_note": "Heuristic JD keyword coverage, not probability of hiring or verified candidate qualification.",
            "score_breakdown": {
                "mandatory_keyword_score": f"{mandatory_score:.1f} / 60.0",
                "preferred_keyword_score": f"{preferred_score:.1f} / 40.0",
            },
            "mandatory_keyword_signals": mandatory_criteria,
            "recommended_cv": recommended_cv,
            "differentiating_evidence": evidence_matches,
        }


if __name__ == "__main__":
    print("=== JOEL X — Evidence-Based Career Matching Engine (v0.2 prototype) ===")
    infisical_jd = """
    Infisical is an open-source security platform. We are seeking an Enterprise Account Executive
    covering EMEA remote. Must have a track record of closing B2B technical SaaS or API platform deals.
    Comfort speaking with CISOs and developer leads is required. French fluency is a plus.
    Must be located in EMEA timezones.
    """
    engine = EvidenceBasedMatchingEngine(CANDIDATE_PROFILE)
    report = engine.evaluate_role("Enterprise AE", "Infisical", infisical_jd)
    print("\n[HEURISTIC EVALUATION REPORT — SAMPLE JD, NOT LIVE VERIFIED]")
    print(json.dumps(report, indent=2))
