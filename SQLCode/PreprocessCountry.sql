USE CovidData;
GO

WITH tmp1 AS
(
	SELECT iso_code, country, _2022_last_updated, REPLACE(area, 'sq_km', '') AS area 
	FROM "2022_population"
),
tmp2 AS
(
	SELECT iso_code, country, _2022_last_updated, REPLACE(area, ',', '') AS area 
	FROM tmp1
)
INSERT INTO Country
SELECT iso_code, country, _2022_last_updated, CAST(area AS int) AS area 
FROM tmp2
