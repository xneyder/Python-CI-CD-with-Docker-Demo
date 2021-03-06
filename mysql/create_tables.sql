CREATE DATABASE CISCO_PCRF;
USE CISCO_PCRF;

CREATE TABLE CISCO_PCRF_CPU (
PMM_DATETIME DATETIME,
NE_NAME varchar(55),
CPU_ID  int,
STEAL  int,
IDLE double,
CPU_USER double,
_SYSTEM double,
WAIT double
);

CREATE UNIQUE INDEX CISCO_PCRF_CPU_IDX1 on 
CISCO_PCRF_CPU (PMM_DATETIME,NE_NAME,CPU_ID) ;

