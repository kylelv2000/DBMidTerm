USE CovidData;
GO

INSERT INTO Infection
SELECT '2020-1-21', ISO, 0, 0, 0, 0, 0, 0
FROM Country;

WITH tmp AS
(
	SELECT ISO, "Date",
	SUM(Confirmed) AS "Total Cases", SUM(Deaths) AS "Total Deaths", SUM(Recovered) AS "Total Recovered"
	FROM covid_19_clean_complete, Country
	WHERE LOWER(Country_Region) = LOWER("Name")
	GROUP BY ISO, "Date"
)
INSERT INTO Infection
SELECT "Date", ISO,
	"Total Cases" - LAG("Total Cases", 1, 0) OVER (PARTITION BY ISO ORDER BY "Date") AS "New Cases",
	"Total Deaths" - LAG("Total Deaths", 1, 0) OVER (PARTITION BY ISO ORDER BY "Date") AS "New Deaths",
	"Total Recovered" - LAG("Total Recovered", 1, 0) OVER (PARTITION BY ISO ORDER BY "Date") AS "New Recovered",
	"Total Cases", "Total Deaths", "Total Recovered"
FROM tmp
ORDER BY ISO, "Date";