rmdir /s /q build
rmdir /s /q dist
del main.exe
del main.spec
pyinstaller --onefile main.py
del main.spec
move dist\main.exe .