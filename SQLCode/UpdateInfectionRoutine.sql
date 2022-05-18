IF EXISTS (SELECT * FROM msdb.dbo.sysjobs WHERE "name" = N'Update Infection Routine')
BEGIN
	EXEC msdb.dbo.sp_delete_job @job_name = N'Update Infection Routine'
END

IF EXISTS (SELECT * FROM msdb.dbo.sysschedules WHERE "name" = N'Update Infection Schedule')
BEGIN
	EXEC msdb.dbo.sp_delete_schedule @schedule_name = N'Update Infection Schedule'
END

EXEC msdb.dbo.sp_add_job 
    @job_name = N'Update Infection Routine',     
    @enabled = 1,   
    @description = N'Update the Infection table every day'; 

EXEC msdb.dbo.sp_add_jobstep  
    @job_name = N'Update Infection Routine',   
    @step_name = N'Run Procedure',   
    @subsystem = N'TSQL',   
    @command = 'EXEC UpdateInfection';

EXEC msdb.dbo.sp_add_schedule  
    @schedule_name = N'Update Infection Schedule',   
    @freq_type = 4,  -- daily start
    @freq_interval = 1,
    @active_start_time = '235959' ;   -- start time 23:59:59

EXEC msdb.dbo.sp_attach_schedule  
    @job_name = N'Update Infection Routine',  
    @schedule_name = N'Update Infection Schedule';

EXEC msdb.dbo.sp_add_jobserver  
    @job_name = N'Update Infection Routine',  
    @server_name = @@servername ;
