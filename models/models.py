from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DATE, Enum

metadata = MetaData()

athletes = Table(
    "athletes",
    metadata,
    Column("athlete_id", Integer, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("date_of_birth", DATE, nullable=False),
    Column("gender", Enum("M", "F", name="gender_types"), nullable=False),
    Column("country_id", Integer, ForeignKey("countries.country_id"))
)

countries = Table(
    "countries",
    metadata,
    Column("country_id", Integer, primary_key=True),
    Column("country_name", String, nullable=False),
    Column("continent", String, nullable=False)
)

medals = Table(
    "medals",
    metadata,
    Column("medal_id", Integer, primary_key=True),
    Column("event_id", Integer, ForeignKey("events.event_id"), nullable=False),
    Column("athlete_id", Integer, ForeignKey("athletes.athlete_id")),
    Column("medal_type", Enum("gold", "silver", "bronze", name="medal_types"), nullable=False)
)

olympics = Table(
    "olympics",
    metadata,
    Column("olympic_id", Integer, primary_key=True),
    Column("year", DATE, nullable=False),
    Column("location", String, nullable=False),
    Column("season", Enum("winter", "summer", name="season_types"), nullable=False)
)

events = Table(
    "events",
    metadata,
    Column("event_id", Integer, primary_key=True),
    Column("event_name", String, nullable=False),
    Column("sport_id", Integer, ForeignKey("sports.sport_id"), nullable=False),
    Column("event_date", DATE, nullable=False),
    Column("olympic_id", Integer, ForeignKey("olympics.olympic_id"))
)

sports = Table(
    "sports",
    metadata,
    Column("sport_id", Integer, primary_key=True),
    Column("sport_name", String, nullable=False),
    Column("category", Enum("winter", "summer", name="season_type"), nullable=False)
)
