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
    
    def get_branches(self):
        cmd = ['branch']
        op = run_cmd(cmd)
        linelist = op.out.split("\n")
        branchlist = []
        current = -1
        for line in linelist:
            strings = line.split()
            if len(strings.get(0, "")) > 0:
                if strings[0] == "*":
                    current = len(namelist)
                    strings = strings[1:]
                info = []
                info['nm'] = strings[0]
                info['sh'] = strings[1]
                info['cm'] = strings[-1]
                info['rt'] = None

                if re.search(r'\[\.\]'):
                    info['rt'] = re.sub(r'.*/', r'', strings[2][1:-1])
                    
                branchlist.append(info)
        return branchlist, current
    def get_cur_branch(self):
        branches, current = get_branches()
        return branches[current]
    
    def do_fetch(self, branch = None, had = False):
        cmd = ['fetch', 'origin']
        if branch:
            cmd.append(branch)
        elif had:
            cmd.append(get_cur_branch().rt)
        run_cmd(cmd)
        return 0
    
    def do_push(self, remote = ''):
        cmd = 'push --porcelain ' + remote + ' ' + get_cur_branch().nm
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

    def do_checkout(self, branch, new = False, track = False):
        cmd = ['checkout']
        if new:
            cmd.append('-b')
            
        cmd.append(str(branch))
        
        if new and track:
            cmd.append('origin/' + branch)

        run_cmd(cmd)
        
    def __init__(self, get_path, origin):
        self.path = get_path
        run_cmd(['init'])
        if origin:
            set_origin(str(origin))

def assure_location(path, name):
    if not os.path.isfolder(pj(path, name)):
        os.mkdir(pj(path, name))

def setup_branches(path, url):
    master = Repo(pj(path, 'master'))
    
    folders = [ name for name in os.listdir(path) if os.path.isdir(pj(path, name)) and name != 'master' ]
    repos = []
    rts = []
    rts_owned = []

    for f in folders:
        repo = Repo(pj(path, f))
        #Add checks for empty/corrupt repo!
        repos.append(repo)
        rts_owned.append(repo.get_cur_branch().rt)
    
    master.do_fetch()
    branches = master.get_branches()

    rts = [branch.rt for branch in branches]

    for rt in rts:
        if rt in rts_owned:
            continue
        fpath = pj(path, rt)
        os.mkdir(fpath)
        repo = Repo(fpath, origin = url)
        repo.append(repo)
        repo.do_fetch()
        repo.do_checkout(rt, new = True, track = True)
        rts_owned.append(rt)
