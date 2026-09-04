from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import csv, random, json

BASE = Path(__file__).parent

def read_csv(name):
    with open(BASE / name, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

PROJECTS = read_csv('projects.csv')
PARCELS = read_csv('parcels.csv')
PERSONS = read_csv('interested_persons.csv')

app = FastAPI(title='BhoomiMitra Mock Government Integration API', version='1.0')

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'synthetic-demo-api'}

@app.get('/api/v1/land-records/{survey_number:path}')
def land_record(survey_number: str):
    for parcel in PARCELS:
        if parcel['survey_number'] == survey_number:
            person = next((x for x in PERSONS if x['parcel_id'] == parcel['parcel_id']), None)
            return {
                'source': 'MOCK_KARNATAKA_LAND_RECORDS',
                'survey_number': survey_number,
                'ulpin_demo': parcel['ulpin_demo'],
                'owner_name': person['name'] if person else None,
                'relationship_type': person['relationship_type'] if person else None,
                'village': parcel['village'],
                'taluk': parcel['taluk'],
                'district': parcel['district'],
                'state': parcel['state'],
                'area_acres': float(parcel['area_acres']),
                'land_type': parcel['land_type'],
                'rtc_status': parcel['rtc_status'],
                'mutation_status': parcel['mutation_status'],
                'synthetic': True
            }
    raise HTTPException(status_code=404, detail='Synthetic survey record not found')

@app.get('/api/v1/cadastral/{survey_number:path}')
def cadastral(survey_number: str):
    for parcel in PARCELS:
        if parcel['survey_number'] == survey_number:
            official = json.loads(parcel['official_boundary'])
            field = json.loads(parcel['field_verified_boundary'])
            return {
                'source': 'MOCK_BHU_NAKSHA',
                'survey_number': survey_number,
                'ulpin_demo': parcel['ulpin_demo'],
                'geometry_type': 'Polygon',
                'official_boundary': official,
                'field_verified_boundary': field,
                'geometry_discrepancy': parcel['geometry_discrepancy'] == 'True',
                'synthetic': True
            }
    raise HTTPException(status_code=404, detail='Synthetic cadastral record not found')

@app.get('/api/v1/projects/{project_id}')
def project(project_id: str):
    for p in PROJECTS:
        if p['project_id'] == project_id:
            return p
    raise HTTPException(status_code=404, detail='Project not found')

@app.get('/api/v1/dashboard')
def dashboard():
    def num(k): return sum(float(p[k]) for p in PROJECTS)
    return {
        'project_count': len(PROJECTS),
        'land_proposed_ha': round(num('land_proposed_ha'), 2),
        'land_notified_ha': round(num('land_notified_ha'), 2),
        'land_acquired_ha': round(num('land_acquired_ha'), 2),
        'land_possessed_ha': round(num('land_possessed_ha'), 2),
        'compensation_assessed': sum(int(p['compensation_assessed']) for p in PROJECTS),
        'compensation_paid': sum(int(p['compensation_paid']) for p in PROJECTS),
        'families_affected': sum(int(p['families_affected']) for p in PROJECTS),
        'families_displaced': sum(int(p['families_displaced']) for p in PROJECTS),
        'high_risk_projects': [p['project_id'] for p in PROJECTS if p['timeline_risk'] == 'High'],
        'synthetic': True
    }

class MutationRequest(BaseModel):
    ulpin_demo: str
    survey_number: str
    new_holder: str
    possession_date: str

@app.post('/api/v1/mutation')
def mutation(req: MutationRequest):
    return {
        'source': 'MOCK_KARNATAKA_LAND_RECORDS',
        'status': 'ACKNOWLEDGED',
        'mutation_reference': f'MOCK-MUT-2026-{random.randint(1000,9999)}',
        'survey_number': req.survey_number,
        'ulpin_demo': req.ulpin_demo,
        'message': 'Synthetic mutation request accepted for demonstration.',
        'synthetic': True
    }
