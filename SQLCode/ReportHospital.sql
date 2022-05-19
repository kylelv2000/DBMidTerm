USE CovidData;
GO

DROP PROC IF EXISTS ReportHospital;
GO

CREATE PROC ReportHospital(@Hospital# varchar(32), @Password varchar(64)) AS
BEGIN
    IF NOT EXISTS (SELECT * FROM Hospital WHERE Hospital# = @Hospital# AND Password = @Password)
        RETURN 1
    DECLARE @LastReport datetime
    SET @LastReport = (SELECT LastReport FROM Hospital WHERE Hospital# = @Hospital#)

    DECLARE @NewCases integer
    SET @NewCases = (SELECT COUNT(*) FROM Patients WHERE Hospital# = @Hospital# 
                        AND DATEDIFF(SECOND, @LastReport, "Date Admitted") >= 0)
    
    DECLARE @NewDeaths integer
    SET @NewDeaths = (SELECT COUNT(*) FROM Patients WHERE Hospital# = @Hospital# 
                      AND "Status" = 'Dead'
                      AND DATEDIFF(SECOND, @LastReport, "Date Leave") >= 0)

    DECLARE @NewRecovered integer
    SET @NewRecovered = (SELECT COUNT(*) FROM Patients WHERE Hospital# = @Hospital# 
                         AND "Status" = 'Recovered'
                         AND DATEDIFF(SECOND, @LastReport, "Date Leave") >= 0)
    
    INSERT INTO Updates VALUES
        (GETDATE(), @Hospital#, @NewCases, @NewDeaths, @NewRecovered)
    UPDATE Hospital
    SET LastReport = GETDATE()
    WHERE Hospital# = @Hospital#
    RETURN 0
END;