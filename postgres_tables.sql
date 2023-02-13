CREATE DATABASE records_db;

DROP TABLE IF EXISTS run;
CREATE TABLE IF NOT EXISTS run (
	id INT,
	created_on TIMESTAMP,
	PRIMARY KEY(id)
	);

DROP TABLE IF EXISTS records_input_json;
CREATE TABLE IF NOT EXISTS records_input_json (
   id INT,
   run_id INT,
   payload JSON,
   PRIMARY KEY(id),
   FOREIGN KEY(run_id)
   REFERENCES run(id)
);

DROP TABLE IF EXISTS records_output_json;
CREATE TABLE IF NOT EXISTS records_output_json (
   id INT,
   payload JSON,
   run_id INT,
   PRIMARY KEY(id),
   FOREIGN KEY(run_id)
   REFERENCES run(id)
);


