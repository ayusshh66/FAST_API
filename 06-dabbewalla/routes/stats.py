
from datetime import datetime, date, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func

from models import orderStatus, Order
from database import get_session

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("/daily")
def daily_summary(
    summary_date: date | None = Query(
        None,
        description="Date for summary (YYYY-MM-DD)"
    ),
    session: Session = Depends(get_session)
):

    # Use today's date if none was provided
    if summary_date is None:
        summary_date = date.today()

    # Beginning of selected day (UTC)
    start = datetime.combine(
        summary_date,
        datetime.min.time(),
        tzinfo=timezone.utc
    )

    # Beginning of the next day (UTC)
    end = start + timedelta(days=1)

    summary = {}
    total = 0

    for status in orderStatus:

        count = session.exec(
            select(func.count(Order.id)).where(
                Order.created_at >= start,
                Order.created_at < end,
                Order.status == status
            )
        ).one()

        summary[status.value] = count

        total += count

    return {
        "date": summary_date,
        "total_orders": total,
        "summary": summary
    }
