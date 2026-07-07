import uuid
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine, get_db
from .seed import seed_if_empty

app = FastAPI(title="Güven Sigorta API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------
@app.get("/api/customers", response_model=List[schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).order_by(models.Customer.created_at.desc()).all()


@app.post("/api/customers", response_model=schemas.Customer, status_code=201)
def create_customer(payload: schemas.CustomerCreate, db: Session = Depends(get_db)):
    customer = models.Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@app.get("/api/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.get(models.Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    return customer


@app.put("/api/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: str, payload: schemas.CustomerUpdate, db: Session = Depends(get_db)
):
    customer = db.get(models.Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    for key, value in payload.model_dump().items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


@app.delete("/api/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.get(models.Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    db.delete(customer)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Policies
# ---------------------------------------------------------------------------
@app.get("/api/policies", response_model=List[schemas.PolicyWithCustomer])
def list_policies(
    customer_id: str | None = Query(default=None), db: Session = Depends(get_db)
):
    q = db.query(models.Policy)
    if customer_id:
        q = q.filter(models.Policy.customer_id == customer_id)
    return q.order_by(models.Policy.created_at.desc()).all()


@app.post("/api/policies", response_model=schemas.Policy, status_code=201)
def create_policy(payload: schemas.PolicyCreate, db: Session = Depends(get_db)):
    customer = db.get(models.Customer, payload.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    policy = models.Policy(**payload.model_dump())
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


@app.get("/api/policies/{policy_id}", response_model=schemas.PolicyWithCustomer)
def get_policy(policy_id: str, db: Session = Depends(get_db)):
    policy = db.get(models.Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Poliçe bulunamadı")
    return policy


@app.put("/api/policies/{policy_id}", response_model=schemas.Policy)
def update_policy(
    policy_id: str, payload: schemas.PolicyUpdate, db: Session = Depends(get_db)
):
    policy = db.get(models.Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Poliçe bulunamadı")
    for key, value in payload.model_dump().items():
        setattr(policy, key, value)
    db.commit()
    db.refresh(policy)
    return policy


@app.delete("/api/policies/{policy_id}", status_code=204)
def delete_policy(policy_id: str, db: Session = Depends(get_db)):
    policy = db.get(models.Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Poliçe bulunamadı")
    db.delete(policy)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Claims
# ---------------------------------------------------------------------------
@app.get("/api/claims", response_model=List[schemas.ClaimWithPolicy])
def list_claims(
    policy_id: str | None = Query(default=None), db: Session = Depends(get_db)
):
    q = db.query(models.Claim)
    if policy_id:
        q = q.filter(models.Claim.policy_id == policy_id)
    return q.order_by(models.Claim.created_at.desc()).all()


@app.post("/api/claims", response_model=schemas.Claim, status_code=201)
def create_claim(payload: schemas.ClaimCreate, db: Session = Depends(get_db)):
    policy = db.get(models.Policy, payload.policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Poliçe bulunamadı")
    claim = models.Claim(
        claim_number=f"CLM-{uuid.uuid4().hex[:8].upper()}", **payload.model_dump()
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


@app.get("/api/claims/{claim_id}", response_model=schemas.ClaimWithPolicy)
def get_claim(claim_id: str, db: Session = Depends(get_db)):
    claim = db.get(models.Claim, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Hasar talebi bulunamadı")
    return claim


@app.put("/api/claims/{claim_id}", response_model=schemas.Claim)
def update_claim(
    claim_id: str, payload: schemas.ClaimUpdate, db: Session = Depends(get_db)
):
    claim = db.get(models.Claim, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Hasar talebi bulunamadı")
    for key, value in payload.model_dump().items():
        setattr(claim, key, value)
    db.commit()
    db.refresh(claim)
    return claim


@app.delete("/api/claims/{claim_id}", status_code=204)
def delete_claim(claim_id: str, db: Session = Depends(get_db)):
    claim = db.get(models.Claim, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Hasar talebi bulunamadı")
    db.delete(claim)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@app.get("/api/stats/dashboard", response_model=schemas.DashboardStats)
def dashboard_stats(db: Session = Depends(get_db)):
    total_customers = db.query(models.Customer).count()
    total_policies = db.query(models.Policy).count()
    active_policies = (
        db.query(models.Policy)
        .filter(models.Policy.status == models.PolicyStatus.AKTIF)
        .count()
    )
    total_claims = db.query(models.Claim).count()
    pending_claims = (
        db.query(models.Claim)
        .filter(models.Claim.status == models.ClaimStatus.BEKLEMEDE)
        .count()
    )
    total_premium = db.query(func.coalesce(func.sum(models.Policy.premium), 0.0)).scalar()
    total_claim_amount = db.query(
        func.coalesce(func.sum(models.Claim.amount), 0.0)
    ).scalar()

    policies_by_type = dict(
        db.query(models.Policy.type, func.count(models.Policy.id))
        .group_by(models.Policy.type)
        .all()
    )
    claims_by_status = dict(
        db.query(models.Claim.status, func.count(models.Claim.id))
        .group_by(models.Claim.status)
        .all()
    )

    return schemas.DashboardStats(
        total_customers=total_customers,
        total_policies=total_policies,
        active_policies=active_policies,
        total_claims=total_claims,
        pending_claims=pending_claims,
        total_premium=total_premium,
        total_claim_amount=total_claim_amount,
        policies_by_type={k.value: v for k, v in policies_by_type.items()},
        claims_by_status={k.value: v for k, v in claims_by_status.items()},
    )


# ---------------------------------------------------------------------------
# Frontend static files (only present in the combined single-image build,
# see root Dockerfile). Mounted last so it never shadows the /api/* and
# /health routes above. Falls back to index.html for unknown paths so
# Vue Router's history mode works on hard page loads/refreshes.
# ---------------------------------------------------------------------------
STATIC_DIR = Path(__file__).parent / "static"

if STATIC_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str):
        candidate = STATIC_DIR / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(STATIC_DIR / "index.html")

