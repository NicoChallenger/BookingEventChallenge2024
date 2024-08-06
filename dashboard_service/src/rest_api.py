from datetime import date
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from src import crud, enums, service
from src.database import get_db


app = FastAPI()


@app.get("/dashboard", response_model=dict[date, int], summary="Retrieve the dashboard data")
def get_dashboard(
    hotel_id: int,
    period: enums.DashboardPeriod,
    year: int,
    db: Session = Depends(get_db),  # dependency injection
):
    events = crud.get_booking_events_for_year(db, hotel_id=hotel_id, year=year)
    if period == enums.DashboardPeriod.MONTH:
        return service.group_events_by_month(events=events, year=year)
    elif period == enums.DashboardPeriod.DAY:
        return service.group_events_by_day(events=events, year=year)
