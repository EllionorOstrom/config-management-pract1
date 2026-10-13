@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0.."
python scripts\make_vfs.py

echo ===== 1. minimal VFS =====
echo vfs-info | python -m src.emulator --vfs vfs\minimal.zip
echo ===== 2. several files (text, empty, binary) =====
echo vfs-info | python -m src.emulator --vfs vfs\several.zip
echo ===== 3. three and more levels =====
echo vfs-info | python -m src.emulator --vfs vfs\deep.zip
echo ===== 4. VFS file does not exist =====
python -m src.emulator --vfs vfs\missing.zip
echo exit code: %errorlevel%
echo ===== 5. file is not a ZIP archive =====
python -m src.emulator --vfs vfs\broken.zip
echo exit code: %errorlevel%
echo ===== 6. all commands via start script =====
python -m src.emulator --vfs vfs\deep.zip --script scripts\startup\all_commands.emu
echo exit code: %errorlevel%
