@rem taskarg: ${file}
@Echo off
set OLDHOME_FOLDER=%~dp0
pushd %OLDHOME_FOLDER%
call ..\.venv\Scripts\activate.bat

rem call memory_profiling_time.cmd %MAIN_SCRIPT_FILE%
call memory_profiling_time.cmd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistasi_ServerLog_Statistic\antistasi_serverlog_statistic\filtering\basic_overview.py
