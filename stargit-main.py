import os
import re
import subprocess
import tkinter as tk
import uuid
import time
from os.path import join as pj

try:
    import _thread as thread
except ImportError:
    import _dummy_thread as thread
    
def say_hi():
        print("hi there, everyone!")

s1 = ''#u'\u2022' + ' '
s2 = u'\u251c' + ' '
s3 = u'\u2514' + ' '

gui_lock = thread.allocate_lock()
gui_pipe = {
    '_DONE': False,
    'l_sel': None
    }

def OnSelect(event):
    widget = event.widget
    value = widget.curselection()[0]
    print(str(value))
    with gui_lock:
        gui_pipe['l_sel'] = value

class Application(tk.Frame):
    def createWidgets(self):
        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = say_hi

        self.hi_there.pack({"side": "left"})

        listbox = tk.Listbox(self, width=20, height=5, font=('consolas', 10))
        listbox.bind('<<ListboxSelect>>', OnSelect)
        listbox.pack({"side": "left"})
        listbox.insert(tk.END, s1 + "Test")
        listbox.insert(tk.END, s2 + "Lorem")
        listbox.insert(tk.END, s2 + "Ipsum")
        listbox.insert(tk.END, s3 + "abcdefghijklmnopqrstuvxyzåäö-abcdefghijklmnopqrstuvxyzåäö-")
        listbox.insert(tk.END, s1 + "Sit")
        listbox.insert(tk.END, s1 + "Amet")
        print(str(listbox.delete(3)))
        listbox.insert(3, s3 + "Dolor")

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
def ident_neterr(string_in):
    if re_search('unable to access', str(string_in)):
        return True
    return False

def get_idstring(fake_input = None):
    return ''.join(string(uuid.uuid4()).split('-'))

class Repo:
    path = ''
    
    def format_output(self, string_in):
        return str(eval(str(str_in)[1:]))[:-1]
    
    def run_cmd(self, cmd, output = {}):
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW  # tell windows to use wShowWindow options
        si.wShowWindow = subprocess.SW_HIDE  # ShowWindow option - only one that sounded useful

        result = subprocess.Popen(['git', *cmd], cwd=self.path, stdout = subprocess.PIPE, stderr = subprocess.PIPE, startupinfo=si)
        output['out'] = format_output(result.stdout.read())
        output['err'] = format_output(result.stderr.read())
        return output
    
    def set_shipyard(self, url):
        self.run_cmd(("remote add shipyard " + url).split())

    def get_remotes(self):
        return None

    def branch_rm(self, branch):
        cmd = ['branch', '-d', branch]
        self.run_cmd(cmd)

    def get_branches(self):
        cmd = ['branch']
        op = self.run_cmd(cmd)
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
    def get_rem_branches(self, remote = 'shipyard'):
        cmd = ['ls-remote', '-h',remote]
        op = {}
        self.run_cmd(cmd, op)
        if ident_neterr(op.err):
            return 101, []
        return 0, [rem.split('/')[-1] for rem in op.out.split('\n')]
        
        
    def get_cur_branch(self):
        branches, current = self.get_branches()
        return branches.get(current, None)
    
    def do_fetch(self, branch = None, _all = False):
        cmd = ['fetch', 'shipyard']
        
        if branch:
            cmd.append(branch)
        elif not _all:
            cmd.append(get_cur_branch().rt)
        op = {}    
        self.run_cmd(cmd, op)
        if ident_neterr(op.err):
            return 101
        return 0
    
    def do_push(self, remote = False, upstream = True):
        cmd = ['push', '--porcelain']
        if upstream:
            cmd.append('-u')
        if remote == False:
            remote = 'shipyard'
        cmd.append(remote)
        cmd.append(get_cur_branch().nm)
        
        op = self.run_cmd(cmd)
        if ident_neterr(op.err):
            return 101
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
            
        cmd = 'add . --all'.split()
        self.run_cmd(cmd)

        cmd = 'commit -m updated'.split()
        self.run_cmd(cmd)
        return 0

    def do_checkout(self, branch, new = False, track = False, orphan = False):
        cmd = ['checkout']
        new = new or orphan
        track = track and not orphan
        if new and orphan:
            cmd.append('--orphan')
        elif new:
            cmd.append('-b')

        branch = str(branch)
        cmd.append(branch)
        
        if new and track:
            cmd.append('shipyard/' + branch)

        self.run_cmd(cmd)
        if orphan:
            self.run_cmd(['rm', '-rf'])
    
    def __init__(self, path, shipyard):
        self.path = path
        self.run_cmd(['init'])
        if shipyard:
            self.set_shipyard(str(shipyard))

def list_dir(path):
    return [item for item in os.listdir(path) if os.path.isdir(pj(path, item))]

def assure_location(path, name):
    if not os.path.isfolder(pj(path, name)):
        os.mkdir(pj(path, name))

def inc(num = -1):
    return num + 1

def assure_unique(name, namelist, modify = inc):
    counter = modify()
    while True:
        counter = modify(counter)
        new_name = name + str(counter)
        if not new_name in namelist:
            break;
    return new_name

def setup_repo(path, url, branch, new = False):
    f_list = list_dir(path)
    f_name = assure_unique('repo_', f_list)
    
    fpath = pj(path, name)
    os.mkdir(fpath)
    repo = Repo(fpath, shipyard = url)
    repo.append(repo)
    if new:
        repo.do_checkout(branch, orphan = True)
    else:
        repo.do_fetch(branch = branch)
        repo.do_checkout(branch, new = True, track = True)
    
def split_repo(core_repo, repo, path):
    cur_branch = repo.get_cur_branch()
    url = repo.get_remotes()[0].url
    cur_name = cur_branch.nm
    base_name = cur_name.split('#')[0]
    
    new_name = '#'.join(base_name, get_idstring())
    
    repo.do_checkout(new_name, new = True)
    
    setup_repo(path, url, cur_name)

def try_update(repo, path):
    repo.do_push()

def setup_folders(path, url):
    master = Repo(pj(path, 'master'))
    
    folders = [ name for name in list_dir(path) if name != 'master' ]
    repos = []
    rts = []
    rts_owned = []

    for f in folders:
        repo = Repo(pj(path, f))
        #Add checks for empty/corrupt repo!
        repos.append(repo)
        rts_owned.append(repo.get_cur_branch().rt)
    
    master.do_fetch(_all = True)
    branches = master.get_branches()
    err_get, rem_branches = master.get_rem_branches()

    assert not err_get

    rts = [rem_branch.rt for rem_branch in rem_branches]

    for rt in rts:
        if rt in rts_owned:
            continue
        setup_repo(path, url, rt)
        rts_owned.append(rt)

def window_func():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    with gui_lock:
        gui_pipe['_DONE'] = True
    root.destroy()
    return None

window_thread = thread.start_new_thread(window_func, ())
RUNNING = True
while RUNNING:
    with gui_lock:
        print(gui_pipe['l_sel'])
        RUNNING = not gui_pipe['_DONE']
        time.sleep(1)

print('QUIT')
    
