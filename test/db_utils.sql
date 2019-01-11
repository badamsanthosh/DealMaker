-- Create the user:
CREATE USER dealmax WITH PASSWORD 'deal@123';
ALTER USER dealmax CREATEDB;


-- Clean the existing Setup:
DROP DATABASE dealmax;

-- Create Database : dealmax
CREATE DATABASE dealmax
WITH
    OWNER = dealmax
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
GRANT ALL ON DATABASE dealmax TO dealmax;
GRANT TEMPORARY, CONNECT ON DATABASE dealmax TO PUBLIC;
GRANT ALL ON DATABASE dealmax TO dealmax;


-- Create Schema & Grant Permissions
CREATE SCHEMA IF NOT EXISTS home_loans AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA home_loans TO dealmax;

CREATE SCHEMA IF NOT EXISTS lending AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA lending TO dealmax;

CREATE SCHEMA IF NOT EXISTS meta AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA meta TO dealmax;

CREATE SCHEMA IF NOT EXISTS user_mgmt AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA user_mgmt TO dealmax;

CREATE SCHEMA IF NOT EXISTS third_party AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA third_party TO dealmax;


