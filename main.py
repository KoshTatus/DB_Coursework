from fastapi import FastAPI

from routers.tables_router import router as tables_router
from routers.athlete_router import router as athlete_router
from routers.country_router import router as country_router
from routers.events_router import router as event_router
from routers.sports_router import router as sport_router
from routers.olympic_router import router as olympic_router
from routers.medals_router import router as medal_router

app = FastAPI(
    title="Olympics",
)

app.include_router(athlete_router)
app.include_router(country_router)
app.include_router(event_router)
app.include_router(sport_router)
app.include_router(olympic_router)
app.include_router(medal_router)
app.include_router(tables_router)
