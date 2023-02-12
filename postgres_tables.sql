CREATE DATABASE records_db;

DROP TABLE records_input_json;
CREATE TABLE IF NOT EXISTS records_input_json (
   run_id INT,
   payload JSON,
   created_on TIMESTAMP
);

DROP TABLE records_output_json;
CREATE TABLE IF NOT EXISTS records_output_json (
   run_id INT,
   payload JSON,
   created_on TIMESTAMP
);