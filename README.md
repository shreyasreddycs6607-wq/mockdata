# BhoomiMitra Mock API Dataset

Synthetic data generated from the workflow/data requirements in the supplied project notes.

Files:
- bhoomimitra_mock_data.json — complete seed dataset
- projects.csv — project-level dashboard/MIS data
- parcels.csv — core parcel registry + GIS/cadastral fields
- interested_persons.csv — owner/co-owner/tenant-style relationships
- affected_families.csv — R&R-oriented family records
- payments.csv — compensation assessed vs paid + mock PFMS refs
- objections.csv — objections/grievances demo records
- mock_api.py — FastAPI stub exposing the integration endpoints

Run:
    pip install fastapi uvicorn
    uvicorn mock_api:app --reload --port 8000

Demo endpoints:
    GET  /health
    GET  /api/v1/land-records/45%2F2A
    GET  /api/v1/cadastral/45%2F2A
    GET  /api/v1/projects/LA-KA-2026-001
    GET  /api/v1/dashboard
    POST /api/v1/mutation

Frontend demo flow:
1. User enters a survey number.
2. Frontend calls /api/v1/land-records/{survey_number}.
3. Populate owner, village, area, RTC and mutation fields.
4. Call /api/v1/cadastral/{survey_number}.
5. Draw official vs field-verified polygon on the map.
6. After possession, POST /api/v1/mutation.
7. Refresh dashboard to show the project roll-up.

IMPORTANT:
This dataset is entirely fictional. It is for prototype/demo testing only and must not be presented as live government records.
