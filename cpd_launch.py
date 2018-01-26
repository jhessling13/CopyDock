# Main launcher for CopyDock
# to compile to exe, run 'pyinstaller.exe --onefile --windowed .\cpd_launch.py'
from cpdock_b import dockWindow

maindock = dockWindow()
maindock.drawWindow()
