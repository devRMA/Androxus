-- create database if not exists androxus;

SELECT 'CREATE DATABASE androxus'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'androxus');