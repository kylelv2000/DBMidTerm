USE CovidData;
INSERT INTO Hospital
	SELECT ID, 'USA' AS ISO, STATE AS State, CITY AS City, NAME AS Name, 0 AS N_Patients, '123456' AS Password FROM HospitalsData;