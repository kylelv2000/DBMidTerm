USE CovidData;
GO

DROP TRIGGER IF EXISTS PatientInc;
GO

CREATE TRIGGER PatientInc
ON Patients
AFTER INSERT
AS
BEGIN
	UPDATE Hospital
	SET N_Patients = N_Patients + 1
	FROM inserted
	WHERE Hospital.Hospital# = inserted.Hospital#;
END
GO

DROP TRIGGER IF EXISTS PatientDec;
GO

CREATE TRIGGER PatientDec
ON Patients
AFTER UPDATE
AS
BEGIN
	UPDATE Hospital
	SET N_Patients = N_Patients - 1
	FROM inserted
	WHERE Hospital.Hospital# = inserted.Hospital#;
END
GO