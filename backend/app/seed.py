import random
from datetime import date, timedelta

from sqlalchemy.orm import Session

from . import models

FIRST_NAMES = [
    "Ahmet", "Ayşe", "Mehmet", "Fatma", "Mustafa", "Zeynep", "Emre",
    "Elif", "Can", "Deniz", "Burak", "Selin", "Kerem", "Aylin",
]
LAST_NAMES = [
    "Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Yıldız", "Aydın",
    "Öztürk", "Arslan", "Doğan", "Kılıç", "Aslan",
]
CITIES = [
    "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Kocaeli",
]


def _random_tc() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(11))


def _random_phone() -> str:
    return "5" + "".join(str(random.randint(0, 9)) for _ in range(9))


def seed_if_empty(db: Session) -> None:
    if db.query(models.Customer).count() > 0:
        return

    customers = []
    for i in range(12):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        customer = models.Customer(
            first_name=first,
            last_name=last,
            tc_no=_random_tc(),
            email=f"{first.lower()}.{last.lower()}{i}@example.com",
            phone=_random_phone(),
            city=random.choice(CITIES),
            birth_date=date(
                random.randint(1955, 2000), random.randint(1, 12), random.randint(1, 28)
            ),
        )
        db.add(customer)
        customers.append(customer)
    db.flush()

    policy_types = list(models.PolicyType)
    policies = []
    policy_seq = 0
    for i, customer in enumerate(customers):
        for _ in range(random.randint(1, 2)):
            start = date.today() - timedelta(days=random.randint(30, 400))
            policy_seq += 1
            policy = models.Policy(
                policy_number=f"POL-{2024000 + policy_seq}",
                customer_id=customer.id,
                type=random.choice(policy_types),
                status=random.choice(
                    [models.PolicyStatus.AKTIF, models.PolicyStatus.AKTIF, models.PolicyStatus.SUSPENDED]
                ),
                premium=round(random.uniform(800, 12000), 2),
                coverage_amount=round(random.uniform(20000, 500000), 2),
                start_date=start,
                end_date=start + timedelta(days=365),
            )
            db.add(policy)
            policies.append(policy)
    db.flush()

    claim_statuses = list(models.ClaimStatus)
    descriptions = [
        "Trafik kazası sonrası hasar",
        "Cam kırılması",
        "Su baskını hasarı",
        "Hastane tedavi masrafı",
        "Ameliyat masrafı",
        "Hırsızlık sonrası kayıp",
        "Yangın hasarı",
        "Diş tedavisi",
    ]
    for i, policy in enumerate(random.sample(policies, k=min(10, len(policies)))):
        claim = models.Claim(
            claim_number=f"CLM-{5000 + i}",
            policy_id=policy.id,
            description=random.choice(descriptions),
            amount=round(random.uniform(500, 50000), 2),
            status=random.choice(claim_statuses),
            incident_date=policy.start_date + timedelta(days=random.randint(1, 300)),
        )
        db.add(claim)

    db.commit()
