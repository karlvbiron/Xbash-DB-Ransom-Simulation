-- Connect to the correct PDB
ALTER SESSION SET CONTAINER = MYDB;

-- Drop user if exists
BEGIN
    EXECUTE IMMEDIATE 'DROP USER MY_DATABASE CASCADE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -1918 THEN  -- ORA-01918: user does not exist
            RAISE;
        END IF;
END;
/

-- Create user and grant necessary privileges
CREATE USER MY_DATABASE IDENTIFIED BY "my_password"
    DEFAULT TABLESPACE USERS
    TEMPORARY TABLESPACE TEMP
    QUOTA UNLIMITED ON USERS;

-- Grant necessary privileges
GRANT CREATE SESSION TO MY_DATABASE;
GRANT CREATE TABLE TO MY_DATABASE;
GRANT CREATE SEQUENCE TO MY_DATABASE;
GRANT CREATE PROCEDURE TO MY_DATABASE;
GRANT CREATE TRIGGER TO MY_DATABASE;
GRANT CREATE VIEW TO MY_DATABASE;
GRANT UNLIMITED TABLESPACE TO MY_DATABASE;

-- Switch to the new user context
ALTER SESSION SET CURRENT_SCHEMA = MY_DATABASE;

-- Create table
CREATE TABLE my_table (
    firstName VARCHAR2(100),
    lastName VARCHAR2(100),
    email VARCHAR2(100),
    phoneNumber VARCHAR2(20)
);

-- Insert sample data
INSERT INTO my_table (firstName, lastName, email, phoneNumber) VALUES
('John', 'Doe', 'john@doe.com', '0123456789');
INSERT INTO my_table (firstName, lastName, email, phoneNumber) VALUES
('Jane', 'Doe', 'jane@doe.com', '9876543210');
INSERT INTO my_table (firstName, lastName, email, phoneNumber) VALUES
('James', 'Bond', 'james.bond@mi6.co.uk', '0612345678');

COMMIT;
