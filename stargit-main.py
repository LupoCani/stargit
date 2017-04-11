import os
import re
import subprocess
import tkinter as tk
from os.path import join as pj

class Repo:
    path = ''
    
    def format_output(self, string_in):
        return str(eval(str(str_in)[1:]))[:-1]
    def run_cmd(self, cmd):
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW  # tell windows to use wShowWindow options
        si.wShowWindow = subprocess.SW_HIDE  # ShowWindow option - only one that sounded useful

        result = subprocess.Popen(['git', *cmd], cwd=self.path, stdout = subprocess.PIPE, stderr = subprocess.PIPE, startupinfo=si)
        return {'out': format_output(result.stdout.read()), 'err': format_output(result.stderr.read())}
    def set_origin(self, url):
        run_cmd(("remote add origin " + url).split())
        
    def __init__(self, get_path, origin = None):
        self.path = get_path
        run_cmd(['init'])
        if origin:
            set_origin(str(origin))
    
    def get_branches(self):
        cmd = ['branch']
        op = run_cmd(cmd)
        branchlist = op.out.split("\n")
        namelist = []
        current = -1
        for i in branchlist:
            strings = branchlist[i].split()
            if len(strings.get(-1, "")) > 0:
                namelist.append(strings[-1])
                if strings[0] == "*":
                    current = len(namelist)-1
        return namelist, current
    def get_cur_branch(self):
        branch_info = get_branches()
        return branch_info[0][branch_info[1]]
    
    def do_fetch(self):
        run_cmd(['fetch'])
        return 0
    
    def do_push(self, remote = ''):
        cmd = 'push --porcelain ' + remote + ' ' + get_cur_branch()
        cmd = cmd.split()
        
        op = run_cmd(cmd)
        if len(op.out) == 0:
            return -1
        if re.match(r"\[rejected\] \(fetch first\)", op.out):
            return 1
        if re.match(r"\[up to date\]", op.out):
            return 2
        if re.match(r"[^\]\)]\nDone", op.out):
            return 0

        return -1
    
    def do_commit(self):
        if len(run_cmd('status -z'.split()).out) == 0:
            return 1
            
        cmd = 'add . --all'
        cmd = cmd.split()
        run_cmd(cmd)

        cmd = 'commit -m updated'
        return 0

    def do_checkout(self, branch):
        cmd = ['checkout', str(branch)]

def assure_location(path, name):
    if not os.path.isfolder(pj(path, name)):
        os.mkdir(pj(path, name))

def setup_branches(path, url):
    master = Repo(pj(path, 'master'))
    master.do_fetch()
    branches = master.get_branches()[0]

    for i in branches:
        name = branches[i]
        assure_location(path, name)
        repo = Repo(pj(path, name), origin=url)
        repo.do_checkout(name)
