import subprocess
import io
import re

def format_n(str_in):
    return eval(str(str_in)[1:])[:-1]

si = subprocess.STARTUPINFO()
si.dwFlags = subprocess.STARTF_USESHOWWINDOW  # tell windows to use wShowWindow options
si.wShowWindow = subprocess.SW_HIDE  # ShowWindow option - only one that sounded useful

while True:
    directory = input("Enter directory:\n")

    if directory[1:2] != ":":
        break

    print("------------------")
    
    while True:
        cmd_in = input("==> ")
        if (cmd_in.startswith("exit")):
            break
        
        cmd = cmd_in.split()
        
        result = subprocess.Popen(cmd, cwd=directory, stdout = subprocess.PIPE, stderr = subprocess.PIPE, startupinfo=si)
        
        print("-------")
        print("Result: " + str(result))
        print("-")
        print(format_n(result.stdout.read()))
        print("-")
        print(format_n(result.stderr.read()))
        print("-------")
