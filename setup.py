from cx_Freeze import setup, Executable

# exclude unneeded packages. More could be added. Has to be changed for
# other programs.
build_exe_options = {"excludes": ["tkinter"],
                     "optimize": 1}

setup(name="HW Tracking Tool",
      version="0.1",
      description="HW Tracking tool for Vector Devices",
      options={"build_exe": build_exe_options},
      executables=[Executable("Hardware_Tracking.py")])
