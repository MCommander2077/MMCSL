echo off&cls
pip install customtkinter
pip install mcrcon
pyinstaller --noconfirm --onefile --windowed --add-data "C:/Users/Administrator/AppData/Local/Programs/Python/Python311/Lib/site-packages/customtkinter;customtkinter/" --add-data "./players.py;." --version-file ./version.txt "./main.py"