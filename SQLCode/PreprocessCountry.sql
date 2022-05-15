USE CovidData;
GO

SELECT iso_code, country, _2022_last_updated, REPLACE(area, 'sq_km', '') AS area INTO #tmp1 FROM "2022_population";
SELECT iso_code, country, _2022_last_updated, REPLACE(area, ',', '') AS area INTO #tmp2 FROM #tmp1;
SELECT iso_code, country, _2022_last_updated, CAST(area AS int) AS area INTO #tmp3 FROM #tmp2;
INSERT INTO Country SELECT * FROM #tmp3;
DROP TABLE #tmp1, #tmp2, #tmp3;
