@echo off
echo This will install all dependencies listed in requirements.txt
pause
REM Try pip directly first
where pip >nul 2>nul
if errorlevel 1 (
    REM pip not found, try py -m pip
    where py >nul 2>nul
    if errorlevel 1 (
        REM py not found, try python -m pip
        where python >nul 2>nul
        if errorlevel 1 (
            echo Neither pip, py, nor python was found in PATH. Please install Python and pip.
        ) else (
            python -m pip install -r requirements.txt
        )
    ) else (
        py -m pip install -r requirements.txt
    )
) else (
    pip install -r requirements.txt
)
pause