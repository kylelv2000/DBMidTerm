USE CovidData;
GO
IF EXISTS(SELECT 1 FROM sys.objects WHERE name = 'UpdatePatient')
    DROP PROC UpdatePatient;

GO
CREATE PROC UpdatePatient(@Hospital# varchar(32), @Password varchar(64), @ID varchar(32), @Date date, @Status char(16)) AS
BEGIN
	IF @Password = (SELECT Password FROM Hospital WHERE Hospital# = @Hospital#)
	BEGIN
		IF EXISTS (SELECT 1 FROM Patients WHERE ID = @ID AND Hospital# = @Hospital#)
			UPDATE Patients
			SET Status = @Status, "Date Leave" = @Date
			WHERE ID = @ID AND Hospital# = @Hospital#;
		ELSE
			INSERT INTO Patients VALUES
			(@ID, @Hospital#, @Status, @Date, NULL);
	END
END