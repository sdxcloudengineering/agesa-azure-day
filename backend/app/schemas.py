from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .models import ClaimStatus, PolicyStatus, PolicyType


# ---------- Customer ----------
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    tc_no: str
    email: str
    phone: str
    city: str
    birth_date: date


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


# ---------- Policy ----------
class PolicyBase(BaseModel):
    policy_number: str
    customer_id: str
    type: PolicyType
    status: PolicyStatus = PolicyStatus.AKTIF
    premium: float
    coverage_amount: float
    start_date: date
    end_date: date


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(PolicyBase):
    pass


class Policy(PolicyBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


class PolicyWithCustomer(Policy):
    customer: Optional[Customer] = None


# ---------- Claim ----------
class ClaimBase(BaseModel):
    policy_id: str
    description: str
    amount: float
    status: ClaimStatus = ClaimStatus.BEKLEMEDE
    incident_date: date


class ClaimCreate(ClaimBase):
    pass


class ClaimUpdate(ClaimBase):
    pass


class Claim(ClaimBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    claim_number: str
    created_at: datetime


class ClaimWithPolicy(Claim):
    policy: Optional[Policy] = None


# ---------- Dashboard ----------
class DashboardStats(BaseModel):
    total_customers: int
    total_policies: int
    active_policies: int
    total_claims: int
    pending_claims: int
    total_premium: float
    total_claim_amount: float
    policies_by_type: dict[str, int]
    claims_by_status: dict[str, int]
