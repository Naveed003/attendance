import base64
import pyperclip

import subprocess


def copy2clip(txt):
    cmd = 'echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)


with open("temp.png", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
    my_string = str(my_string)

with open("hello.txt","x") as f:
    f.write(my_string)
