/*==============================================================*/
/* DBMS name:      Sybase SQL Anywhere 10                       */
/* Created on:     2022/5/13 12:05:09                           */
/*==============================================================*/
USE master;
DROP DATABASE IF EXISTS CovidData;
CREATE DATABASE CovidData;
USE CovidData;

/*==============================================================*/
/* Table: Country                                               */
/*==============================================================*/
CREATE TABLE Country 
(
   ISO                  char(3)                        NOT NULL,
   Name                 varchar(64),
   Population           integer,
   Area                 float,
   CONSTRAINT PK_COUNTRY PRIMARY KEY (ISO)
);

/*==============================================================*/
/* Index: Country_Name                                          */
/*==============================================================*/
CREATE UNIQUE INDEX Country_Name ON Country (
Name ASC
);

/*==============================================================*/
/* Table: Hospital                                              */
/*==============================================================*/
CREATE TABLE Hospital 
(
   Hospital#            varchar(32)                      NOT NULL,
   ISO                  char(3),
   "State"              varchar(64),
   City                 varchar(64),
   Name                 varchar(256),
   N_Patients           integer,
   Password             varchar(64),
   CONSTRAINT PK_HOSPITAL PRIMARY KEY (Hospital#)
);

/*==============================================================*/
/* Index: "Hospital_Location_FK"                                */
/*==============================================================*/
CREATE INDEX "Hospital Location_FK" ON Hospital (
ISO ASC
);

/*==============================================================*/
/* Table: Infection                                             */
/*==============================================================*/
CREATE TABLE Infection 
(
   "Date"               date                           NOT NULL,
   ISO                  char(3)                        NOT NULL,
   "New Cases"          integer,
   "New Deaths"         integer,
   "New Recovery"       integer,
   "Total Cases"        integer,
   "Total Deaths"       integer,
   "Total Recovery"     integer,
   CONSTRAINT PK_INFECTION PRIMARY KEY ("Date", ISO)
);

/*==============================================================*/
/* Index: In_FK                                                 */
/*==============================================================*/
CREATE INDEX In_FK ON Infection (
ISO ASC
);

/*==============================================================*/
/* Table: Patients                                              */
/*==============================================================*/
CREATE TABLE Patients 
(
   ID                   varchar(32)                      NOT NULL,
   Hospital#            varchar(32),
   Status               char(16),
   "Date Admitted"      date,
   "Date Leave"         date,
   CONSTRAINT PK_PATIENTS PRIMARY KEY (ID),
   CONSTRAINT CHK_STATUS CHECK(Status IN ('In Hospital', 'Dead', 'Recovered'))
);

/*==============================================================*/
/* Index: Hospitalize_FK                                        */
/*==============================================================*/
CREATE INDEX Hospitalize_FK ON Patients (
Hospital# ASC
);

/*==============================================================*/
/* Table: Updates                                               */
/*==============================================================*/
CREATE TABLE Updates 
(
   "Date"               date                           NOT NULL,
   Hospital#            varchar(32)                    NOT NULL,
   Cases                integer,
   Deaths               integer,
   Recovery             integer,
   CONSTRAINT PK_UPDATES PRIMARY KEY ("Date", Hospital#)
);

ALTER TABLE Hospital
   ADD CONSTRAINT "FK_HOSPITAL_HOSPITAL _COUNTRY" FOREIGN KEY (ISO)
      REFERENCES Country (ISO)
      ON UPDATE CASCADE
      ON DELETE NO ACTION;

ALTER TABLE Infection
   ADD CONSTRAINT FK_INFECTIO_IN_COUNTRY FOREIGN KEY (ISO)
      REFERENCES Country (ISO)
      ON UPDATE CASCADE
      ON DELETE NO ACTION;

ALTER TABLE Patients
   ADD CONSTRAINT FK_PATIENTS_HOSPITALI_HOSPITAL FOREIGN KEY (Hospital#)
      REFERENCES Hospital (Hospital#)
      ON UPDATE CASCADE
      ON DELETE NO ACTION;

ALTER TABLE Updates
   ADD CONSTRAINT FK_UPDATES_REPORT_HOSPITAL FOREIGN KEY (Hospital#)
      REFERENCES Hospital (Hospital#)
      ON UPDATE CASCADE
      ON DELETE NO ACTION;
