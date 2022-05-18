USE CovidData;
GO

DROP PROC IF EXISTS UpdateInfection;
GO

CREATE PROC UpdateInfection AS
BEGIN
	WITH tmp1 AS
	(
		SELECT GETDATE() AS "Date", ISO, 
			SUM(Cases) AS "New Cases", 
			SUM(Deaths) AS "New Deaths", 
			SUM("Recovered") AS "New Recovered" 
		FROM Updates, Hospital
		WHERE Updates.Hospital# = Hospital.Hospital#
			AND DATEDIFF(HOUR, Updates."Date", GETDATE()) BETWEEN 0 AND 23
		GROUP BY ISO
	),
	tmp2 AS
	(
		SELECT ISO, "Total Cases", "Total Deaths", "Total Recovered"
		FROM Infection
		WHERE Infection."Date" = 
			(SELECT DISTINCT MAX("Date") FROM Infection AS I WHERE I.ISO = Infection.ISO)
	)
	INSERT INTO Infection
	SELECT tmp1."Date", tmp1.ISO, "New Cases", "New Deaths", "New Recovered", 
		"Total Cases" + "New Cases" AS "Total Cases", 
		"Total Deaths" + "New Deaths" AS "Total Deaths", 
		"Total Recovered" + "New Recovered" AS "Total Recovered"
	FROM tmp1, tmp2
	WHERE tmp1.ISO = tmp2.ISO;
END