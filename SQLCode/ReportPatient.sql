USE CovidData;
GO

DROP PROC IF EXISTS ReportPatient;
GO

CREATE PROC ReportPatient(@Hospital# varchar(32), @Password varchar(64), @ID varchar(32), @Status char(16)) AS
BEGIN
	IF @Password = <> (SELECT Password FROM Hospital WHERE Hospital# = @Hospital#)
		RETURN
	IF @Status = 'In Hospital'
		INSERT INTO Patients VALUES
		(@ID, @Hospital#, @Status, (SELECT GETDATE()), NULL)
	ELSE
		UPDATE Patients
		SET "Status" = @Status, "Date Leave" = (SELECT GETDATE())
		WHERE ID = @ID AND Hospital# = @Hospital# AND "Status" = 'In Hospital'
END;