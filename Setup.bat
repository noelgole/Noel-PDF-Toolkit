@echo off
REM ====================================================================================
REM  Noel's PDF Toolkit Bootstrap
REM  Installs Chocolatey, Python 3.10, Ghostscript, and Python packages for rebuilding.
REM  MUST be run as Administrator.
REM ====================================================================================

:: Check for admin rights
net session >nul 2>&1
if errorlevel 1 (
  echo ************************************************************
  echo *  ERROR: You must run this script as Administrator.     *
  echo ************************************************************
  pause
  exit /b 1
)

:: 1) Install Chocolatey
echo ============================================================
echo Installing Chocolatey…
echo ============================================================
powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass ^
  -Command "Set-ExecutionPolicy Bypass -Scope Process; ^
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; ^
            iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
if %errorlevel% neq 0 (
  echo Chocolatey installation failed.
  pause
  exit /b 1
)

:: Make sure choco is on the PATH
set "PATH=%ALLUSERSPROFILE%\chocolatey\bin;%PATH%"

:: 2) Install Python 3.10
echo ============================================================
echo Installing Python 3.10 via Chocolatey…
echo ============================================================
choco install python --version 3.10.10 -y --no-progress
if %errorlevel% neq 0 (
  echo Python installation failed.
  pause
  exit /b 1
)

:: 3) Install Ghostscript
echo ============================================================
echo Installing Ghostscript via Chocolatey…
echo ============================================================
choco install ghostscript -y --no-progress
if %errorlevel% neq 0 (
  echo Ghostscript installation failed.
  pause
  exit /b 1
)

:: 4) Refresh environment variables (so python & gswin64c are on the PATH right away)
if exist "%ALLUSERSPROFILE%\chocolatey\bin\refreshenv.cmd" (
  call "%ALLUSERSPROFILE%\chocolatey\bin\refreshenv.cmd"
)

:: 5) Upgrade pip & install Python build deps (for rebuilding your EXE)
echo ============================================================
echo Installing Python packages (PyPDF2, reportlab, Pillow, pyinstaller)…
echo ============================================================
python -m pip install --upgrade pip
python -m pip install PyPDF2 reportlab pillow pyinstaller

echo.
echo ============================================================
echo ✅  Bootstrap complete!
echo.
echo Please close and reopen any Command Prompts or PowerShell windows
echo so the updated PATH (python, gswin64c) takes effect.
echo Then you can rebuild your EXE or run Noel's PDF Toolkit directly.
echo ============================================================
pause
