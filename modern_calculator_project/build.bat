@echo off
echo ========================================
echo    Building Modern Calculator App
echo ========================================
echo.

echo [1/4] Cleaning up old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ModernCalculator.spec del ModernCalculator.spec

echo [2/4] Checking for icon file...
set "ICON_ARG="
if exist calculator.ico (
    echo Icon file found: calculator.ico
    set "ICON_ARG=--icon=calculator.ico"
) else (
    echo No icon file found. Building without icon...
)

echo [3/4] Building executable with PyInstaller (via python -m PyInstaller)...
python -m PyInstaller --onefile ^
            --windowed ^
            --name "ModernCalculator" ^
            %ICON_ARG% ^
            --clean ^
            --noconfirm ^
            modern_calculator.py

echo [4/4] Build complete!
echo.
echo ========================================
echo    YOUR APPLICATION IS READY!
echo ========================================
echo.
echo 📁 Location: dist\ModernCalculator.exe
echo 📦 Size: (check file size)
echo.
echo 🚀 To run: Double-click "ModernCalculator.exe"
echo.
echo 📋 What to do next:
echo   1. Test the app
echo   2. Share the .exe file
echo   3. Post on LinkedIn with #CodingSamurai
echo.
pause