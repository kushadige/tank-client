del run.exe
pyinstaller --onefile run.py
move dist\run.exe .
del run.spec
rmdir /s /q build
rmdir /s /q dist