from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="Runnerbot 1 API",
    version="0.3.0",
    description="Runnerbot 1 Venture 1: AI Farming Assistant + Pesticide Safety + Export Compliance Demo",
)

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
        return "I can provide demo market signals for tomato, pepper, cassava, maize, plantain, beans, cocoa, and okra."

    if "weather" in msg:
        if location_key and location_key in WEATHER_DB:
            w = WEATHER_DB[location_key]
            return (
                f"{w['forecast']} "
                f"Runnerbot recommendation: {w['advice']}"
            )
        return "For this demo I currently provide weather guidance for Ogun and Lagos."

    if "fert" in msg or "fertilizer" in msg or "fertiliser" in msg:
        if crop_key and crop_key in CROP_FERT_PLANS:
            return f"Runnerbot nutrient guidance for {crop_key}: {CROP_FERT_PLANS[crop_key]}"
        return "For this demo I currently support fertiliser guidance for tomato, pepper, maize, cassava, plantain, beans, cocoa, and okra."

    if "safe" in msg or "chemical" in msg or "pesticide" in msg:
        return (
            "Use Product Safety Check for toxicity, EU and Nigeria status, safer alternatives, PPE guidance, and export-risk logic."
        )

    if "export" in msg or "residue" in msg or "eu" in msg:
        return (
            "Use Export Compliance Check to review residue sensitivity, product-specific compliance risk, and export-readiness discipline."
        )

    if "help" in msg or "start" in msg or "hello" in msg:
        return (
            "Welcome to Runnerbot 1. I help farmers, cooperatives, and agribusiness operators make safer, smarter, and more export-ready decisions across pesticide safety, crop health, weather, prices, and compliance."
        )

    return (
        "Runnerbot 1 currently supports pesticide safety checks, pest triage, export compliance, market signals, weather intelligence, and crop guidance. "
        "For the strongest demo path, use Product Safety Check, Pest Triage, and Export Compliance Check."
    )


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "runnerbot1-api", "time": datetime.utcnow().isoformat()}


@app.get("/demo-highlights")
def demo_highlights() -> Dict[str, object]:
    return {"highlights": DEMO_HIGHLIGHTS, "timestamp": datetime.utcnow().isoformat()}


@app.post("/chat")
def chat(req: ChatRequest) -> Dict[str, str]:
    reply = runnerbot_response(req.message, req.crop, req.location)
    return {
        "reply": reply,
        "language": req.language,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/product-check")
def product_check(req: ProductCheckRequest) -> Dict[str, str]:
    info = get_product_info(req.product_name)
    return {
        "product_name": req.product_name,
        **info,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/pest-triage")
def pest_triage(req: PestTriageRequest) -> Dict[str, str | float | bool]:
    result = detect_pest(req.symptoms)
    return {
        "crop": req.crop,
        "location": req.location or "Not provided",
        **result,
        "escalate_to_captain": result["confidence"] < 0.60,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/export-check")
def export_check(req: ExportCheckRequest) -> Dict[str, str]:
    result = get_export_check(req.crop, req.product_name)
    return {
        "crop": req.crop,
        **result,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/intelligence-summary")
def intelligence_summary() -> Dict[str, object]:
    return {
        **INTELLIGENCE_SUMMARY,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/metrics")
def metrics() -> Dict[str, int]:
    return {
        "demo_signups_target_q4": 1000,
        "demo_pro_target_q4": 300,
        "demo_month6_target_farmers": 5000,
        "demo_month6_target_pro": 1200,
    }
