CREATE USER root WITH PASSWORD 'password';
CREATE DATABASE tails;
GRANT ALL ON DATABASE tails TO root;
ALTER USER root CREATEDB;
