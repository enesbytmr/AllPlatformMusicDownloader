from datetime import datetime, timedelta
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import stripe

from .auth.router import get_current_user
from .auth import models
from .auth.database import get_db

stripe.api_key = os.getenv("STRIPE_API_KEY", "")

PLANS = {
    "free": {"limit": 10, "period": "day", "price_id": "price_free"},
    "starter": {"limit": 200, "period": "month", "price_id": "price_starter"},
    "pro": {"limit": 1000, "period": "month", "price_id": "price_pro"},
}

router = APIRouter(prefix="/billing")


def _should_reset(user: models.User, period: str) -> bool:
    if user.quota_reset is None:
        return True
    now = datetime.utcnow()
    if period == "day":
        return now - user.quota_reset >= timedelta(days=1)
    return now - user.quota_reset >= timedelta(days=30)


def check_quota(user: models.User, db: Session, amount: int = 1) -> None:
    plan = PLANS.get(user.subscription, PLANS["free"])
    if _should_reset(user, plan["period"]):
        user.usage = 0
        user.quota_reset = datetime.utcnow()
    if user.usage + amount > plan["limit"]:
        raise HTTPException(status_code=402, detail="Quota exceeded")
    user.usage += amount
    db.add(user)
    db.commit()


def create_checkout_session(plan: str, user: models.User) -> str:
    price_id = PLANS[plan]["price_id"]
    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        customer_email=user.email,
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return session.url


@router.get("/plans")
def list_plans():
    return PLANS


@router.post("/upgrade")
def upgrade_plan(
    plan: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if plan not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")
    try:
        url = create_checkout_session(plan, current_user)
    except Exception as exc:  # pragma: no cover - network call
        raise HTTPException(status_code=400, detail=str(exc))
    current_user.subscription = plan
    current_user.usage = 0
    current_user.quota_reset = datetime.utcnow()
    db.add(current_user)
    db.commit()
    return {"checkout_url": url}
