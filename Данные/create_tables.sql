CREATE TABLE IF NOT EXISTS "Athletes" (
	"athlete_id" serial NOT NULL UNIQUE,
	"first_name" varchar(255) NOT NULL,
	"last_name" varchar(255) NOT NULL,
	"date_of_birth" date NOT NULL,
	"gender" varchar(255) NOT NULL,
	"country_id" bigint NOT NULL,
	PRIMARY KEY ("athlete_id")
);

CREATE TABLE IF NOT EXISTS "Sport" (
	"sport_id" serial NOT NULL UNIQUE,
	"sport_name" varchar(255) NOT NULL UNIQUE,
	"category" varchar(255) NOT NULL,
	PRIMARY KEY ("sport_id")
);

CREATE TABLE IF NOT EXISTS "Events" (
	"event_id" serial NOT NULL UNIQUE,
	"event_name" varchar(255) NOT NULL,
	"sport_id" bigint NOT NULL,
	"event_date" date NOT NULL,
	"olympics_id" bigint NOT NULL,
	PRIMARY KEY ("event_id")
);

CREATE TABLE IF NOT EXISTS "Countries" (
	"country_id" serial NOT NULL UNIQUE,
	"country_name" varchar(255) NOT NULL UNIQUE,
	"continent" varchar(255) NOT NULL,
	PRIMARY KEY ("country_id")
);

CREATE TABLE IF NOT EXISTS "Medals" (
	"medal_id" serial NOT NULL UNIQUE,
	"event_id" bigint NOT NULL,
	"athlete_id" bigint NOT NULL,
	"medal_type" varchar(255) NOT NULL,
	PRIMARY KEY ("medal_id")
);

CREATE TABLE IF NOT EXISTS "Olympics" (
	"olympics_id" serial NOT NULL UNIQUE,
	"year" date NOT NULL,
	"location" varchar(255) NOT NULL,
	"season" varchar(255) NOT NULL,
	PRIMARY KEY ("olympics_id")
);

ALTER TABLE "Athletes" ADD CONSTRAINT "Athletes_fk5" FOREIGN KEY ("country_id") REFERENCES "Countries"("country_id");

ALTER TABLE "Events" ADD CONSTRAINT "Events_fk2" FOREIGN KEY ("sport_id") REFERENCES "Sport"("sport_id");

ALTER TABLE "Events" ADD CONSTRAINT "Events_fk4" FOREIGN KEY ("olympics_id") REFERENCES "Olympics"("olympics_id");

ALTER TABLE "Medals" ADD CONSTRAINT "Medals_fk1" FOREIGN KEY ("event_id") REFERENCES "Events"("event_id");

ALTER TABLE "Medals" ADD CONSTRAINT "Medals_fk2" FOREIGN KEY ("athlete_id") REFERENCES "Athletes"("athlete_id");
