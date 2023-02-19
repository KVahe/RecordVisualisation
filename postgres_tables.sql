CREATE DATABASE records_db;

DROP TABLE IF EXISTS run;
CREATE TABLE IF NOT EXISTS run (
	id SERIAL,
	created_on TIMESTAMP,
	PRIMARY KEY(id)
	);

DROP TABLE IF EXISTS records_input_json;
CREATE TABLE IF NOT EXISTS records_input_json (
   id SERIAL,
   run_id INT,
   payload JSON,
   PRIMARY KEY(id),
   FOREIGN KEY(run_id)
   REFERENCES run(id)
);

DROP TABLE IF EXISTS records_output_json;
CREATE TABLE IF NOT EXISTS records_output_json (
   id SERIAL,
   payload JSON,
   run_id INT,
   PRIMARY KEY(id),
   FOREIGN KEY(run_id)
   REFERENCES run(id)
);

DROP TABLE IF EXISTS gender_table;
CREATE TABLE gender_table (
	id SERIAL,
	name VARCHAR(99), 
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS record_table;
CREATE TABLE record_table (
	id SERIAL,
	name VARCHAR(99),
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS sport_table;
CREATE TABLE sport_table (
	id SERIAL,
	name VARCHAR(99),
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS record_measure;
CREATE TABLE record_measure(
	id SERIAL,
	gender_type INT,
	record_type INT,
	sport_type INT,
	measure FLOAT,
	PRIMARY KEY(id),
	FOREIGN KEY(record_type) REFERENCES record_table(id),
	FOREIGN KEY(gender) REFERENCES gender_table(id),
	FOREIGN KEY(sport_type) REFERENCES sport_table(id)
);
