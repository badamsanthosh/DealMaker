-- SCHEMA: home_loans
DROP SCHEMA home_loans CASCADE;
CREATE SCHEMA home_loans
    AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA home_loans TO dealmax;

-- SCHEMA: lending
DROP SCHEMA lending CASCADE;
CREATE SCHEMA lending
    AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA lending TO dealmax;

-- SCHEMA: meta
DROP SCHEMA meta CASCADE;
CREATE SCHEMA meta
    AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA meta TO dealmax;

-- SCHEMA: public
DROP SCHEMA public;
CREATE SCHEMA public
    AUTHORIZATION dealmax;
COMMENT ON SCHEMA public
    IS 'standard public schema';
GRANT ALL ON SCHEMA public TO dealmax;
GRANT ALL ON SCHEMA public TO PUBLIC;

-- SCHEMA: third_party
DROP SCHEMA third_party CASCADE;
CREATE SCHEMA third_party
    AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA third_party TO dealmax;

-- SCHEMA: User Management
DROP SCHEMA user_mgmt CASCADE;
CREATE SCHEMA user_mgmt
    AUTHORIZATION dealmax;
GRANT ALL ON SCHEMA user_mgmt TO dealmax;
