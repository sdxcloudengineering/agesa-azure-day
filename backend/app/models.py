import enum
import uuid
from datetime import date, datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


class PolicyType(str, enum.Enum):
    SAGLIK = "saglik"
    HAYAT = "hayat"
    KASKO = "kasko"
    KONUT = "konut"


class PolicyStatus(str, enum.Enum):
    AKTIF = "aktif"
    SUSPENDED = "askida"
    IPTAL = "iptal"
    SUPHESIZ_BITTI = "sona_erdi"


class ClaimStatus(str, enum.Enum):
    BEKLEMEDE = "beklemede"
    INCELENIYOR = "inceleniyor"
    ONAYLANDI = "onaylandi"
    REDDEDILDI = "reddedildi"


def generate_id() -> str:
    return uuid.uuid4().hex[:10]


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=generate_id)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    tc_no = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    city = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    policies = relationship(
        "Policy", back_populates="customer", cascade="all, delete-orphan"
    )


class Policy(Base):
    __tablename__ = "policies"

    id = Column(String, primary_key=True, default=generate_id)
    policy_number = Column(String, unique=True, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    type = Column(Enum(PolicyType), nullable=False)
    status = Column(Enum(PolicyStatus), nullable=False, default=PolicyStatus.AKTIF)
    premium = Column(Float, nullable=False)
    coverage_amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="policies")
    claims = relationship(
        "Claim", back_populates="policy", cascade="all, delete-orphan"
    )


class Claim(Base):
    __tablename__ = "claims"

    id = Column(String, primary_key=True, default=generate_id)
    claim_number = Column(String, unique=True, nullable=False)
    policy_id = Column(String, ForeignKey("policies.id"), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(ClaimStatus), nullable=False, default=ClaimStatus.BEKLEMEDE)
    incident_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    policy = relationship("Policy", back_populates="claims")
