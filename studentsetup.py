import sys
import cx_Freeze
from cx_Freeze import *
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

shortcut_table = [
    ("DesktopShortcut", # Shortcut 
     "DesktopFolder", # Directory_
     "StudentResultSystem", # Name
     "TARGETDIR", # Component_
     "[TARGETDIR]\StudentResultSystem.exe", # Target
     None, # Arguments
     None, # Description
     None, # Hotkey
     None, # Icon
     None, # IconIndex
     None, # ShowCmd
     "TARGETDIR", # WkDir
    )
]
 
msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {'data': msi_data}
cx_Freeze.setup(
    version="0.1",
    description="Student Result Management System",
    author="SP SC",
    name="Student Result Management System",
    options={'build_exe': {"packages":["tkinter","mysql.connector"],'include_files':["icon.ico"]},"bdist_msi": bdist_msi_options },
    executables=[cx_Freeze.Executable("StudentResultSystem.py",base=base,icon='icon.ico')]
)
