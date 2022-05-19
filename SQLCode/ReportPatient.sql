USE CovidData;
GO

DROP PROC IF EXISTS ReportPatient;
GO

CREATE PROC ReportPatient(@Hospital# varchar(32), @Password varchar(64), @ID varchar(32), @Status char(16)) AS
BEGIN
	IF @Password <> (SELECT Password FROM Hospital WHERE Hospital# = @Hospital#)
		RETURN 1
	IF @Status = 'In Hospital'
		IF @ID IN (SELECT ID FROM Patients)
			RETURN 3
		ELSE
		BEGIN
			INSERT INTO Patients VALUES
			(@ID, @Hospital#, @Status, (SELECT GETDATE()), NULL)
			RETURN 0
		END
	ELSE
	BEGIN
		IF @Status NOT IN ('Dead', 'Recovered')
			RETURN 2
		IF NOT EXISTS(SELECT * FROM Patients WHERE ID = @ID AND Hospital# = @Hospital# AND "Status" = 'In Hospital')
			RETURN 4
		ELSE
		BEGIN
			UPDATE Patients
			SET "Status" = @Status, "Date Leave" = (SELECT GETDATE())
			WHERE ID = @ID AND Hospital# = @Hospital# AND "Status" = 'In Hospital'
			RETURN 0
		END
	END
END;