import sys
from cx_Freeze import setup, Executable

setup(
    name = "generalstores",
    version = "3.1",
    description = "stock management system",
    executables = [Executable("run.py", base = "Win32GUI")])
