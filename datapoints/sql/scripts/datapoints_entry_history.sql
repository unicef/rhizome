CREATE TABLE "datapoints_historicaldatapointentry" (
	    "id" integer NOT NULL,
	    "indicator_id" integer,
	    "region_id" integer,
	    "campaign_id" integer,
	    "value" double precision NOT NULL,
	    "note" varchar(255),
	    "changed_by_id" integer,
	    "created_at" timestamp with time zone NOT NULL,
	    "source_datapoint_id" integer,
	    "history_id" serial NOT NULL PRIMARY KEY,
	    "history_date" timestamp with time zone NOT NULL,
	    "history_user_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
	    "history_type" varchar(1) NOT NULL
)
;

GRANT ALL PRIVILEGES ON datapoints_historicaldatapointentry TO djangoapp;
GRANT USAGE, SELECT ON SEQUENCE datapoints_historicaldatapointentry_history_id_seq TO djangoapp;