from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="Runnerbot 1 API",
    version="0.4.0",
    description="Runnerbot 1 Venture 1: AI Farming Assistant + Pesticide Safety + Export Compliance + IKIC Cold Chain Ops",
)

# -------------------------------------------------------------------
# EXISTING DEMO KNOWLEDGE BASES
# -------------------------------------------------------------------

PESTICIDE_DB: Dict[str, Dict[str, str]] = {
    "paraquat": {
        "toxicity": "Highly Hazardous Pesticide (HHP)",
        "eu_status": "Banned",
        "nigeria_status": "High-risk / restricted concern",
        "risk_summary": "Severe acute toxicity risk to handlers and major environmental concern.",
        "safer_alternative": "Mechanical weed control, mulching, cover crops, lower-tox targeted weed management.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "High export-risk product from a buyer trust and compliance standpoint.",
        "runnerbot_verdict": "Avoid where possible. Escalate to safer weed-control planning.",
    },
    "atrazine": {
        "toxicity": "Highly Hazardous Pesticide (HHP)",
        "eu_status": "Banned",
        "nigeria_status": "High-risk / restricted concern",
        "risk_summary": "Water contamination and long-term ecological risk profile.",
        "safer_alternative": "Mechanical weeding, crop rotation, mulching, lower-tox selective alternatives where approved.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "High residue and market credibility risk.",
        "runnerbot_verdict": "Do not position this as a preferred solution in export-oriented value chains.",
    },
    "dichlorvos": {
        "toxicity": "Highly Hazardous Pesticide (HHP)",
        "eu_status": "Banned",
        "nigeria_status": "Residue-sensitive / avoid",
        "risk_summary": "High food safety concern and frequent export residue issue.",
        "safer_alternative": "Hermetic storage, safer storage controls, approved lower-tox pest management.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Very high risk of export rejection.",
        "runnerbot_verdict": "Strong avoid signal for any value chain targeting premium or export markets.",
    },
    "chlorpyrifos": {
        "toxicity": "Highly Hazardous / neurotoxicity concern",
        "eu_status": "Banned",
        "nigeria_status": "High-risk concern",
        "risk_summary": "High regulatory sensitivity and strong human exposure concerns.",
        "safer_alternative": "Integrated pest management, biological controls, lower-tox approved alternatives.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "High residue and compliance risk.",
        "runnerbot_verdict": "Avoid in serious compliance-led farming systems.",
    },
    "glyphosate": {
        "toxicity": "Moderate / debated",
        "eu_status": "Restricted / tightly scrutinized",
        "nigeria_status": "Registered in several contexts",
        "risk_summary": "Use only with disciplined handling, documentation, and label compliance.",
        "safer_alternative": "Spot treatment, integrated weed management, manual control where feasible.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Moderate risk depending on crop, interval, and buyer specification.",
        "runnerbot_verdict": "Use only with strict discipline and clear residue-management logic.",
    },
    "mancozeb": {
        "toxicity": "Moderate",
        "eu_status": "Restricted / phase-out concern",
        "nigeria_status": "Use with caution",
        "risk_summary": "Requires careful timing, residue discipline, and label adherence.",
        "safer_alternative": "Resistant varieties, sanitation, biofungicides where available.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Moderate residue risk if timing is poor.",
        "runnerbot_verdict": "Can only sit inside a disciplined spray-record and interval system.",
    },
    "lambda-cyhalothrin": {
        "toxicity": "Moderate to high depending on exposure",
        "eu_status": "Restricted / MRL-sensitive",
        "nigeria_status": "Commonly used",
        "risk_summary": "Useful in some contexts but demands disciplined application and interval control.",
        "safer_alternative": "Biocontrol, monitoring-led threshold spraying, lower-tox targeted alternatives where feasible.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Moderate to high if overused or poorly timed.",
        "runnerbot_verdict": "Use only when justified by scouting and with export timing discipline.",
    },
    "cypermethrin": {
        "toxicity": "Moderate",
        "eu_status": "Restricted / MRL-sensitive",
        "nigeria_status": "Commonly used",
        "risk_summary": "Common product but can create residue and resistance issues when overused.",
        "safer_alternative": "Threshold-based spraying, IPM, biological controls where available.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Moderate risk if records and intervals are weak.",
        "runnerbot_verdict": "Only defensible with proper scouting, dosage discipline, and records.",
    },
    "imidacloprid": {
        "toxicity": "Moderate / pollinator concern",
        "eu_status": "Restricted",
        "nigeria_status": "Registered in several contexts",
        "risk_summary": "Needs careful crop-specific judgement and environmental awareness.",
        "safer_alternative": "Biological controls, resistant varieties, targeted lower-tox interventions.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Moderate export sensitivity depending on crop and timing.",
        "runnerbot_verdict": "Do not use casually; justify economically and agronomically.",
    },
    "carbendazim": {
        "toxicity": "Moderate to high concern",
        "eu_status": "Restricted / high scrutiny",
        "nigeria_status": "Use with caution",
        "risk_summary": "Residue and regulatory sensitivity require disciplined application and record-keeping.",
        "safer_alternative": "Resistant varieties, sanitation, biofungicides, and tighter disease prevention programs.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Moderate to high for residue-sensitive value chains.",
        "runnerbot_verdict": "Only defensible inside a well-documented disease-control program.",
    },
    "metalaxyl": {
        "toxicity": "Moderate",
        "eu_status": "Restricted / monitored",
        "nigeria_status": "Use with caution",
        "risk_summary": "Can be useful in disease programs but needs strict interval discipline and resistance management.",
        "safer_alternative": "Drainage improvement, sanitation, resistant seed, integrated disease management.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Moderate risk where documentation and timing are weak.",
        "runnerbot_verdict": "Use only where agronomically justified and properly recorded.",
    },
    "2,4-d": {
        "toxicity": "Moderate / drift-sensitive",
        "eu_status": "Restricted / scrutiny varies",
        "nigeria_status": "Commonly used with caution",
        "risk_summary": "Drift and misapplication can create crop injury, environmental issues, and market concerns.",
        "safer_alternative": "Spot treatment, mechanical control, cover cropping, integrated weed management.",
        "ppe": "Gloves, goggles, mask, long sleeves, boots.",
        "export_risk": "Moderate where buyer standards are strict.",
        "runnerbot_verdict": "Only use under disciplined weed-management logic, not convenience spraying.",
    },
}

PRODUCT_ALIASES: Dict[str, str] = {
    "sniper": "dichlorvos",
    "gramoxone": "paraquat",
    "roundup": "glyphosate",
}

PRICE_DB: Dict[str, int] = {
    "tomato": 550000,
    "pepper": 800000,
    "cassava": 160000,
    "maize": 420000,
    "plantain": 300000,
    "beans": 700000,
    "cocoa": 3200000,
    "okra": 600000,
    "eggplant": 500000,
    "leafy vegetables": 650000,
    "mushrooms": 1200000,
    "herbs": 900000,
}

WEATHER_DB: Dict[str, Dict[str, str]] = {
    "ogun": {
        "forecast": "Light rain expected in the next 48 hours.",
        "advice": "Spray only in dry windows, avoid late-day application, and improve drainage before heavy moisture pressure.",
    },
    "lagos": {
        "forecast": "Humid conditions with scattered showers.",
        "advice": "Move harvested produce quickly, protect from moisture, and tighten same-day logistics discipline.",
    },
}

CROP_FERT_PLANS: Dict[str, str] = {
    "tomato": "Establish with balanced basal nutrition, then support fruiting with disciplined split applications and calcium-aware management.",
    "pepper": "Use moderate basal nutrition, avoid excess nitrogen, and maintain stable watering to protect fruit quality.",
    "maize": "Apply balanced basal nutrition at planting and split nitrogen support at 3–5 weeks based on rainfall and crop vigor.",
    "cassava": "Prioritize potassium, soil structure, and organic matter; avoid blanket application without field logic.",
    "plantain": "Use compost-rich fertility, split feeding, and heavy mulch to protect moisture and root health.",
    "beans": "Keep nitrogen moderate, prioritize phosphorus and crop health, and avoid overfeeding lush but weak growth.",
    "cocoa": "Balanced nutrition, shade discipline, sanitation, and disease prevention should work together as one management system.",
    "okra": "Moderate fertility, steady moisture, and strong pest scouting give the best return profile.",
}

EXPORT_RULES: Dict[str, Dict[str, str]] = {
    "beans": {
        "priority_market": "EU / premium regional buyers",
        "residue_risk": "High if hazardous insecticides are used close to harvest.",
        "compliance_advice": "Use only approved products, document every spray, respect pre-harvest intervals, and route through disciplined cooperative controls.",
    },
    "cocoa": {
        "priority_market": "EU / global processors",
        "residue_risk": "High sensitivity to banned residues and weak traceability.",
        "compliance_advice": "Keep batch records, approved input lists, spray logs, and strong cooperative traceability discipline.",
    },
    "tomato": {
        "priority_market": "Domestic premium / regional",
        "residue_risk": "Moderate to high depending on fungicide and insecticide timing.",
        "compliance_advice": "Avoid late hazardous applications, document intervals, and align harvest with market and residue logic.",
    },
    "pepper": {
        "priority_market": "Domestic premium / regional / selective export",
        "residue_risk": "Moderate to high if repeat spraying is undocumented.",
        "compliance_advice": "Use lower-tox controls where possible, maintain records, and verify buyer specs before harvest.",
    },
    "okra": {
        "priority_market": "Domestic premium / selective export",
        "residue_risk": "Moderate, especially under frequent spray cycles.",
        "compliance_advice": "Tight spray intervals, records, and buyer-driven compliance discipline are essential.",
    },
}

INTELLIGENCE_SUMMARY = {
    "top_flagged_products_demo": ["Paraquat", "Dichlorvos", "Atrazine", "Chlorpyrifos"],
    "priority_states_demo": ["Ogun", "Kaduna", "Benue"],
    "priority_crops_demo": ["Beans", "Tomato", "Pepper", "Cocoa"],
    "insight": "Demo signal: hazardous product checks cluster around export-sensitive crops and intensive vegetable value chains.",
}

DEMO_HIGHLIGHTS = [
    "Farmer-first channels: WhatsApp, USSD, and voice-ready logic.",
    "Pesticide safety intelligence: toxicity, EU/Nigeria status, safer alternatives, PPE.",
    "Export-readiness layer: residue-risk logic for premium value chains.",
    "Data moat: every check can become structured compliance and policy intelligence.",
]

# -------------------------------------------------------------------
# IKIC COLD CHAIN DATA
# -------------------------------------------------------------------

CROP_PERISHABILITY = {
    "tomato": {"urgency": 10, "base_hours": 8, "premium_uplift": 0.22, "loss_without_cold": 0.28},
    "leafy vegetables": {"urgency": 10, "base_hours": 6, "premium_uplift": 0.30, "loss_without_cold": 0.35},
    "mushrooms": {"urgency": 10, "base_hours": 6, "premium_uplift": 0.25, "loss_without_cold": 0.32},
    "herbs": {"urgency": 9, "base_hours": 8, "premium_uplift": 0.18, "loss_without_cold": 0.24},
    "pepper": {"urgency": 8, "base_hours": 14, "premium_uplift": 0.18, "loss_without_cold": 0.20},
    "okra": {"urgency": 8, "base_hours": 12, "premium_uplift": 0.15, "loss_without_cold": 0.22},
    "eggplant": {"urgency": 7, "base_hours": 16, "premium_uplift": 0.14, "loss_without_cold": 0.18},
    "beans": {"urgency": 5, "base_hours": 24, "premium_uplift": 0.12, "loss_without_cold": 0.12},
    "cassava": {"urgency": 3, "base_hours": 30, "premium_uplift": 0.08, "loss_without_cold": 0.10},
    "plantain": {"urgency": 5, "base_hours": 20, "premium_uplift": 0.10, "loss_without_cold": 0.14},
}

IKIC_DEMO_HIGHLIGHTS = [
    "FreshCarrier can carry 2 crates / 40 kg and maintain passive cold chain up to 48 hours in hot zones.",
    "IKIC’s advanced IoT concept includes cold-chain status, geolocation, smart lock, and inventory awareness.",
    "Cooling-as-a-Service and corridor cold-chain hubs create a strong SME and enterprise operating model.",
    "Runnerbot 1 can become the decision layer that decides what to cool, when to move it, and how to protect margin.",
]

# -------------------------------------------------------------------
# MODELS
# -------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(default="English")
    crop: Optional[str] = None
    location: Optional[str] = None


class ProductCheckRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100)


class PestTriageRequest(BaseModel):
    crop: str = Field(..., min_length=1, max_length=50)
    symptoms: str = Field(..., min_length=1, max_length=300)
    location: Optional[str] = None


class ExportCheckRequest(BaseModel):
    crop: str = Field(..., min_length=1, max_length=50)
    product_name: Optional[str] = None


# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------

def normalize_name(name: str) -> str:
    return name.strip().lower()


def get_product_info(name: str) -> Dict[str, str]:
    key = normalize_name(name)
    if key in PRODUCT_ALIASES:
        key = PRODUCT_ALIASES[key]
    if key in PESTICIDE_DB:
        return PESTICIDE_DB[key]
    raise HTTPException(status_code=404, detail=f"No demo record found for '{name}'.")


def detect_pest(symptoms: str) -> Dict[str, str | float]:
    s = symptoms.lower()
    if any(k in s for k in ["armyworm", "holes", "frass", "chewed"]):
        return {
            "diagnosis": "Possible Fall Armyworm Pressure",
            "confidence": 0.72,
            "action": "Immediate scouting is advised. Isolate hotspot areas, avoid blanket panic spraying, and escalate to captain review for field-confirmed action.",
        }
    if any(k in s for k in ["yellow", "curl", "sticky", "aphid"]):
        return {
            "diagnosis": "Possible Aphid Pressure",
            "confidence": 0.68,
            "action": "Inspect leaf undersides, reduce crop stress, and prioritize targeted lower-tox interventions over routine over-application.",
        }
    if any(k in s for k in ["spot", "blight", "dark patch", "wilting"]):
        return {
            "diagnosis": "Possible Fungal Stress / Early Blight Pattern",
            "confidence": 0.64,
            "action": "Remove infected tissue, improve airflow, avoid unnecessary overhead watering, and align fungicide use with safety and residue discipline.",
        }
    return {
        "diagnosis": "General Crop Stress",
        "confidence": 0.45,
        "action": "This should be escalated. Check watering, drainage, nutrition balance, and route to captain review for a more reliable next action.",
    }


def get_export_check(crop: str, product_name: Optional[str]) -> Dict[str, str]:
    crop_key = normalize_name(crop)
    if crop_key not in EXPORT_RULES:
        result = {
            "priority_market": "General market",
            "residue_risk": "Unknown / crop-specific logic still needed",
            "compliance_advice": "Maintain spray records, respect intervals, and verify buyer specs before positioning as export-ready.",
        }
    else:
        result = EXPORT_RULES[crop_key].copy()
    if product_name:
        try:
            product = get_product_info(product_name)
            result["product_risk_overlay"] = (
                f"{product_name.title()} | {product['eu_status']} | {product['toxicity']} | {product['export_risk']}"
            )
        except HTTPException:
            result["product_risk_overlay"] = f"{product_name.title()} | no demo record found."
    else:
        result["product_risk_overlay"] = "No product overlay applied."
    return result


def runnerbot_response(message: str, crop: Optional[str], location: Optional[str]) -> str:
    msg = message.lower().strip()
    crop_key = normalize_name(crop) if crop else None
    location_key = normalize_name(location) if location else None

    if "price" in msg:
        if crop_key and crop_key in PRICE_DB:
            return (
                f"Current demo market signal for {crop_key}: ₦{PRICE_DB[crop_key]:,}. "
                f"Runnerbot interpretation: price alone is not the decision — timing, post-harvest handling, and buyer fit determine real margin."
            )
        return "I can provide demo market signals for tomato, pepper, cassava, maize, plantain, beans, cocoa, okra, mushrooms, herbs, eggplant, and leafy vegetables."

    if "weather" in msg:
        if location_key and location_key in WEATHER_DB:
            w = WEATHER_DB[location_key]
            return f"{w['forecast']} Runnerbot recommendation: {w['advice']}"
        return "For this demo I currently provide weather guidance for Ogun and Lagos."

    if "fert" in msg or "fertilizer" in msg or "fertiliser" in msg:
        if crop_key and crop_key in CROP_FERT_PLANS:
            return f"Runnerbot nutrient guidance for {crop_key}: {CROP_FERT_PLANS[crop_key]}"
        return "For this demo I currently support fertiliser guidance for tomato, pepper, maize, cassava, plantain, beans, cocoa, and okra."

    if "safe" in msg or "chemical" in msg or "pesticide" in msg:
        return "Use Product Safety Check for toxicity, EU and Nigeria status, safer alternatives, PPE guidance, and export-risk logic."

    if "export" in msg or "residue" in msg or "eu" in msg:
        return "Use Export Compliance Check to review residue sensitivity, product-specific compliance risk, and export-readiness discipline."

    if "cold" in msg or "carrier" in msg or "ikic" in msg:
        return "Use the IKIC / Cold Chain Ops tab to assess spoilage risk, loading priority, value preserved, and next-best-action for FreshCarrier operations."

    if "help" in msg or "start" in msg or "hello" in msg:
        return (
            "Welcome to Runnerbot 1. I help farmers, cooperatives, and agribusiness operators make safer, smarter, more export-ready, and more cold-chain-efficient decisions."
        )

    return (
        "Runnerbot 1 currently supports pesticide safety checks, pest triage, export compliance, market signals, weather intelligence, crop guidance, and IKIC cold-chain operations."
    )

# -------------------------------------------------------------------
# IKIC HELPERS
# -------------------------------------------------------------------

def get_crop_meta(crop: str) -> Dict[str, float]:
    return CROP_PERISHABILITY.get(normalize_name(crop), {"urgency": 5, "base_hours": 18, "premium_uplift": 0.12, "loss_without_cold": 0.15})

def trip_intelligence(crop: str, trip_hours: float, ambient_c: float, freshcarrier: bool, charged: bool, destination: str) -> Dict[str, object]:
    meta = get_crop_meta(crop)
    base_hours = meta["base_hours"]

    # no cooling baseline
    no_cold_penalty = max(0, trip_hours - base_hours)
    no_cold_risk = min(95, int(25 + no_cold_penalty * 8 + max(0, ambient_c - 30) * 1.5))

    # with FreshCarrier
    if freshcarrier:
        cold_window = 48 if charged else 24
        cold_fit = trip_hours <= cold_window
        temp_penalty = max(0, ambient_c - 35) * 0.6
        risk = max(5, int((trip_hours / max(cold_window, 1)) * 28 + temp_penalty + (10 - meta["urgency"]) * 1.2))
    else:
        cold_window = 0
        cold_fit = False
        risk = no_cold_risk

    if risk <= 25:
        spoilage = "Low"
        quality = 90 - risk // 2
        premium = "Yes"
    elif risk <= 45:
        spoilage = "Medium"
        quality = 78 - max(0, (risk - 25) // 2)
        premium = "Borderline"
    else:
        spoilage = "High"
        quality = 60 - max(0, (risk - 45) // 2)
        premium = "No"

    if freshcarrier and charged and cold_fit:
        action = f"Load into FreshCarrier and route to {destination}. Protect premium quality and avoid unnecessary delay."
    elif freshcarrier and not charged:
        action = "Recharge thermostatic batteries before dispatch or shorten route. Current readiness is not fully credible for premium handling."
    elif not freshcarrier and meta["urgency"] >= 8:
        action = "Do not move uncooled if premium value matters. Prioritise FreshCarrier or nearest cold room."
    else:
        action = "Proceed only if buyer quality threshold is modest. Otherwise reroute through cooling."

    return {
        "cold_chain_fit": "Yes" if cold_fit else "No",
        "cold_chain_window_hours": cold_window,
        "spoilage_risk": spoilage,
        "risk_score": risk,
        "quality_score": max(20, min(98, quality)),
        "premium_market_eligible": premium,
        "best_next_action": action,
        "commercial_note": "The decision should protect realised selling price, not just physical arrival.",
        "no_cold_baseline_risk_score": no_cold_risk,
    }

def load_priority(crops: List[str]) -> List[Dict[str, object]]:
    ranked = []
    for c in crops:
        c2 = normalize_name(c)
        meta = get_crop_meta(c2)
        ranked.append({"crop": c2.title(), "priority_score": meta["urgency"], "reason": "High perishability and margin sensitivity" if meta["urgency"] >= 8 else "More tolerant but still benefits from cooling discipline"})
    ranked.sort(key=lambda x: x["priority_score"], reverse=True)
    return ranked

def value_preserved(crop: str, volume_kg: float, base_price_ngn: float, trips_per_week: int) -> Dict[str, object]:
    meta = get_crop_meta(crop)
    loss_pct = meta["loss_without_cold"]
    uplift_pct = meta["premium_uplift"]

    baseline_revenue = volume_kg * base_price_ngn
    revenue_lost_without_cold = baseline_revenue * loss_pct
    premium_gain = baseline_revenue * uplift_pct
    total_preserved_per_trip = revenue_lost_without_cold + premium_gain
    monthly_preserved = total_preserved_per_trip * trips_per_week * 4

    return {
        "loss_without_cold_pct": round(loss_pct * 100, 1),
        "premium_uplift_pct": round(uplift_pct * 100, 1),
        "value_preserved_per_trip_ngn": round(total_preserved_per_trip, 0),
        "monthly_value_preserved_ngn": round(monthly_preserved, 0),
        "decision_summary": "Cooling is economically justified when preserving quality meaningfully shifts realised price or reduces waste."
    }

def carrier_monitor(trip_hours_elapsed: float, charged: bool, lock_enabled: bool, crates_loaded: int) -> Dict[str, object]:
    total_window = 48 if charged else 24
    remaining = max(0, total_window - trip_hours_elapsed)
    if remaining > 18:
        status = "Healthy"
    elif remaining > 6:
        status = "Watch"
    else:
        status = "Critical"

    alert = "No active alert." if status == "Healthy" else "Cold-life margin is tightening. Reconfirm ETA and receiving readiness."
    return {
        "temperature_status": "Within controlled band (demo)",
        "remaining_cold_life_hours": round(remaining, 1),
        "battery_status": "Fully charged" if charged else "Partially charged",
        "geo_status": "Trip active (demo)",
        "lock_status": "Locked" if lock_enabled else "Unlocked",
        "inventory_count": crates_loaded,
        "alert": alert,
        "system_status": status,
    }

def caas_model(units: int, trips_per_week: int, avg_value_preserved_per_trip: float) -> Dict[str, object]:
    monthly_trips = trips_per_week * 4
    monthly_value = avg_value_preserved_per_trip * monthly_trips
    util = min(95, 35 + trips_per_week * 6)
    return {
        "recommended_operating_model": "Cooling-as-a-Service micro-fleet",
        "estimated_monthly_trips": monthly_trips,
        "estimated_utilisation_pct": util,
        "estimated_monthly_value_preserved_ngn": round(monthly_value, 0),
        "commercial_readout": "Stronger economics emerge when units are pooled across multiple farmers, aggregators, or route clusters."
    }
