@echo off
setlocal enableextensions
set OLDHOME_FOLDER=%~dp0
set INPATH=%~dp1
set INFILE=%~nx1
set INFILEBASE=%~n1

rem ---------------------------------------------------
set _date=%DATE:/=-%
set _time=%TIME::=%
set _time=%_time: =0%
rem ---------------------------------------------------
rem ---------------------------------------------------
set _decades=%_date:~-2%
set _years=%_date:~-4%
set _months=%_date:~3,2%
set _days=%_date:~0,2%
rem ---------------------------------------------------
set _hours=%_time:~0,2%
set _minutes=%_time:~2,2%
set _seconds=%_time:~4,2%
rem ---------------------------------------------------
set TIMEBLOCK=%_years%-%_months%-%_days%_%_hours%-%_minutes%-%_seconds%
Echo ################# Current time is %TIMEBLOCK%
Echo.
Echo.
Echo.
Echo -------------------------------------------- BASIC VENV SETUP --------------------------------------------
Echo.
Echo.
Echo ################# changing directory to %OLDHOME_FOLDER%
cd %OLDHOME_FOLDER%
Echo.
Echo ################# removing old venv folder
RD /S /Q ..\.venv
echo.

Echo ################# creating new venv folder
mkdir ..\.venv
echo.
Echo ################# calling venv module to initialize new venv
python -m venv ..\.venv
echo.

Echo ################# changing directory to ..\.venv
cd ..\.venv
echo.
Echo ################# activating venv for package installation
call .\Scripts\activate.bat
echo.

Echo ################# upgrading pip to get rid of stupid warning
call %OLDHOME_FOLDER%get-pip.py
echo.
echo.
echo.
Echo -------------------------------------------- INSTALLING PACKAGES --------------------------------------------
echo.
echo.
Echo +++++++++++++++++++++++++++++ Standard Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing Setuptools
call pip install setuptools
echo.
rem Echo ################# Installing pywin32
rem call pip install pywin32
rem echo.
Echo ################# Installing python-dotenv
call pip install python-dotenv
echo.
Echo ################# Installing flit
call pip install --force-reinstall --no-cache-dir flit
echo.
echo.
Echo +++++++++++++++++++++++++++++ Qt Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing PyQt5
call pip install PyQt5
echo.
Echo ################# Installing pyopengl
call pip install pyopengl
echo.
Echo ################# Installing PyQt3D
call pip install PyQt3D
echo.
Echo ################# Installing PyQtChart
call pip install PyQtChart
echo.
Echo ################# Installing PyQtDataVisualization
call pip install PyQtDataVisualization
echo.
Echo ################# Installing PyQtWebEngine
call pip install PyQtWebEngine
echo.
Echo ################# Installing pyqtgraph
call pip install pyqtgraph
echo.
Echo ################# Installing QScintilla
call pip install QScintilla
echo.

echo.

Echo +++++++++++++++++++++++++++++ Packages From Github +++++++++++++++++++++++++++++
echo.
Echo ################# Installing git+https://github.com/overfl0/Armaclass.git
call pip install git+https://github.com/overfl0/Armaclass.git
echo.


echo.

rem Echo +++++++++++++++++++++++++++++ Misc Packages +++++++++++++++++++++++++++++
rem echo.
rem Echo ################# Installing pyperclip
rem call pip install pyperclip
rem echo.
Echo ################# Installing jinja2
call pip install jinja2
echo.
Echo ################# Installing bs4
call pip install bs4
echo.
Echo ################# Installing requests
call pip install requests
echo.
Echo ################# Installing PyGithub
call pip install PyGithub
echo.
Echo ################# Installing fuzzywuzzy
call pip install fuzzywuzzy
echo.
rem Echo ################# Installing fuzzysearch
rem call pip install fuzzysearch
rem echo.
Echo ################# Installing python-Levenshtein
call pip install python-Levenshtein
echo.
rem Echo ################# Installing jsonpickle
rem call pip install jsonpickle
rem echo.
rem Echo ################# Installing discord.py
rem call pip install discord.py
rem echo.
Echo ################# Installing regex
call pip install regex
echo.
Echo ################# Installing marshmallow
call pip install marshmallow
echo.
Echo ################# Installing click
call pip install click
echo.
Echo ################# Installing checksumdir
call pip install checksumdir
echo.
Echo ################# Installing natsort
call pip install natsort
echo.
Echo ################# Installing parse
call pip install parse
echo.

echo.
Echo +++++++++++++++++++++++++++++ Gid Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils
pushd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils
call pip install -e .
popd
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
pushd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
call pip install -e .
popd
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidlogger_rep

call pip install gidlogger

echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper
pushd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper
call pip install -e .
popd
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models
pushd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models
call pip install -e .
popd
echo.
echo.

Echo ################# changing directory to %OLDHOME_FOLDER%
cd %OLDHOME_FOLDER%
echo.
Echo ################# writing ..\requirements_dev.txt
echo ########################################################## created at --^> %TIMEBLOCK% ##########################################################> ..\requirements_dev.txt
call pip freeze >> ..\requirements_dev.txt
echo.
echo.
echo.
Echo +++++++++++++++++++++++++++++ Test Packages +++++++++++++++++++++++++++++
echo.

Echo ################# Installing pytest-qt
call pip install pytest-qt
echo.
Echo ################# Installing pytest
call pip install pytest
echo.

echo.
Echo +++++++++++++++++++++++++++++ Dev Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing wheel
call pip install --no-cache-dir wheel
echo.
Echo ################# Installing pyinstaller
call pip install --force-reinstall --no-cache-dir pyinstaller
echo.
Echo ################# Installing pep517
call pip install --no-cache-dir pep517
echo.

Echo ################# Installing pyqt5-tools==5.15.1.1.7.5
call pip install --pre pyqt5-tools==5.15.1.1.7.5
echo.
Echo ################# Installing PyQt5-stubs
call pip install PyQt5-stubs
echo.
Echo ################# Installing sip
call pip install sip
echo.
Echo ################# Installing PyQt-builder
call pip install PyQt-builder
echo.
Echo ################# Installing pyqtdeploy
call pip install pyqtdeploy
echo.
rem Echo ################# Installing nuitka
rem call pip install nuitka
rem echo.
rem Echo ################# Installing memory-profiler
rem call pip install memory-profiler
rem echo.
rem Echo ################# Installing matplotlib
rem call pip install matplotlib
rem echo.
rem Echo ################# Installing import-profiler
rem call pip install import-profiler
rem echo.
rem Echo ################# Installing objectgraph
rem call pip install objectgraph
rem echo.
rem Echo ################# Installing pipreqs
rem call pip install pipreqs
rem echo.
rem Echo ################# Installing pydeps
rem call pip install pydeps
rem echo.
rem Echo ################# Installing bootstrap-discord-bot
rem call pip install bootstrap-discord-bot
rem echo.
rem echo.

echo -------------------calling pyqt5toolsinstalluic.exe-----------------------------
call ..\.venv\Scripts\pyqt5toolsinstalluic.exe
echo.
rem echo.

echo.
Echo ################# converting ..\requirements_dev.txt to ..\requirements.txt by calling %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
call %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
echo.
Echo INSTALL THE PACKAGE ITSELF AS -dev PACKAGE SO I DONT HAVE TO DEAL WITH RELATIVE PATHS
cd ..\
rem call pip install -e ..
call flit install -s
echo.
echo.
echo ###############################################################################################################
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ---------------------------------------------------------------------------------------------------------------
echo                                                     FINISHED
echo ---------------------------------------------------------------------------------------------------------------
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ###############################################################################################################
