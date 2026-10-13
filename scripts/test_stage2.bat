@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0.."
python scripts\make_vfs.py

echo ===== 1. --vfs and --script =====
python -m src.emulator --vfs vfs\minimal.zip --script scripts\startup\basic.emu
echo exit code: %errorlevel%

echo ===== 2. only --script =====
python -m src.emulator --script scripts\startup\basic.emu
echo exit code: %errorlevel%

echo ===== 3. only --vfs =====
echo exit | python -m src.emulator --vfs vfs\minimal.zip
echo exit code: %errorlevel%

echo ===== 4. no parameters =====
echo exit | python -m src.emulator
echo exit code: %errorlevel%

echo ===== 5. script file does not exist =====
python -m src.emulator --script scripts\startup\missing.emu
echo exit code: %errorlevel%
