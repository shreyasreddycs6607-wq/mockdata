from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json, random

DATA = json.loads(Path(__file__).with_name("bhoomimitra_mock_data.json").read_text(encoding="utf-8"))
app = FastAPI(title="BhoomiMitra Mock Government Integration API", version="1.0")

@app.get("/health")
def health():
    return {"status": "ok", "service": "synthetic-demo-api"}

@app.get("/api/v1/land-records/{survey_number:path}")
def land_record(survey_number: str):
    for parcel, person in zip(DATA["parcels"], DATA["interested_persons"]):
        if parcel["survey_number"] == survey_number:
            return {
                "source": "MOCK_KARNATAKA_LAND_RECORDS",
                "survey_number": survey_number,
                "ulpin_demo": parcel["ulpin_demo"],
                "owner_name": person["name"],
                "relationship_type": person["relationship_type"],
                "village": parcel["village"],
                "taluk": parcel["taluk"],
                "district": parcel["district"],
                "state": parcel["state"],
                "area_acres": parcel["area_acres"],
                "land_type": parcel["land_type"],
                "rtc_status": parcel["rtc_status"],
                "mutation_status": parcel["mutation_status"],
            }
    raise HTTPException(status_code=404, detail="Synthetic survey record not found")

@app.get("/api/v1/cadastral/{survey_number:path}")
def cadastral(survey_number: str):
    for parcel in DATA["parcels"]:
        if parcel["survey_number"] == survey_number:
            return {
                "source": "MOCK_BHU_NAKSHA",
                "survey_number": survey_number,
                "ulpin_demo": parcel["ulpin_demo"],
                "geometry_type": "Polygon",
                "official_boundary": parcel["official_boundary"],
                "field_verified_boundary": parcel["field_verified_boundary"],
                "geometry_discrepancy": parcel["geometry_discrepancy"],
            }
    raise HTTPException(status_code=404, detail="Synthetic cadastral record not found")

@app.get("/api/v1/projects/{project_id}")
def project(project_id: str):
    for p in DATA["projects"]:
        if p["project_id"] == project_id:
            return p
    raise HTTPException(status_code=404, detail="Project not found")

@app.get("/api/v1/dashboard")
def dashboard():
    projects = DATA["projects"]
    return {
        "project_count": len(projects),
        "land_proposed_ha": round(sum(p["land_proposed_ha"] for p in projects), 2),
        "land_notified_ha": round(sum(p["land_notified_ha"] for p in projects), 2),
        "land_acquired_ha": round(sum(p["land_acquired_ha"] for p in projects), 2),
        "land_possessed_ha": round(sum(p["land_possessed_ha"] for p in projects), 2),
        "compensation_assessed": sum(p["compensation_assessed"] for p in projects),
        "compensation_paid": sum(p["compensation_paid"] for p in projects),
        "families_affected": sum(p["families_affected"] for p in projects),
        "families_displaced": sum(p["families_displaced"] for p in projects),
        "high_risk_projects": [p["project_id"] for p in projects if p["timeline_risk"] == "High"],
    }

class MutationRequest(BaseModel):
    ulpin_demo: str
    survey_number: str
    new_holder: str
    possession_date: str

@app.post("/api/v1/mutation")
def mutation(req: MutationRequest):
    return {
        "source": "MOCK_KARNATAKA_LAND_RECORDS",
        "status": "ACKNOWLEDGED",
        "mutation_reference": f"MOCK-MUT-2026-{random.randint(1000,9999)}",
        "survey_number": req.survey_number,
        "ulpin_demo": req.ulpin_demo,
        "message": "Synthetic mutation request accepted for demonstration."
    }
