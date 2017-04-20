import os
import re
import subprocess
import tkinter as tk
import uuid
import time
import json
import copy
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
    'l_sel': None,
    'l_ref': None,
    'btn_q': []
    }

def l_on_select(event):
    widget = event.widget
    value = widget.curselection()[0]
    print(str(value))
    with gui_lock:
        gui_pipe['l_sel'] = value
def b_p_

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
        listbox.bind('<<ListboxSelect>>', l_on_select)
        listbox.pack({"side": "left"})
        listbox.insert(tk.END, s1 + "Test")
        listbox.insert(tk.END, s2 + "Lorem")
        listbox.insert(tk.END, s2 + "Ipsum")
        listbox.insert(tk.END, s3 + "abcdefghijklmnopqrstuvxyzåäö-abcdefghijklmnopqrstuvxyzåäö-")
        listbox.insert(tk.END, s1 + "Sit")
        listbox.insert(tk.END, s1 + "Amet")
        print(str(listbox.delete(3)))
        listbox.insert(3, s3 + "Dolor")
        listbox.insert(20, s3 + "Grande")

        with gui_lock:
            gui_pipe['l_ref'] = listbox

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
        cmd = ['remote', '-v']
        op = self.run_cmd(cmd)
        rem_str_list = op.out.split('\n')
        rem_list = []
        for rem_str in rem_str_list:
            rem = rem_str.split()
            rem_list.append({
                'nm':  rem[0],
                'url': rem[1]
                })
        return rem_list
            

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
    def do_merge_safe(self):
        cmd = ['merge', '--ff-only']
        cur_branch = self.get_cur_branch()
        cmd.append('shipyard/' + cur_branch.rm)
        cmd.append(cur_branch.nm)

        op = self.run_cmd(cmd)
        if re.search('ast-forward', op.out):
            return 0
        if re.search('lready up-to-date', op.out):
            return 0
        if re.search('possible to fast-forwar', op.err):
            return 1
    
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
    return list(set([item for item in os.listdir(path) if os.path.isdir(pj(path, item))]))

def list_file(path):
    return list(set([item for item in os.listdir(path) if os.path.isfile(pj(path, item))]))

def list_all(path):
    return list(set([item for item in os.listdir(path) if os.path.exists(pj(path, item))]))

def assure_location(path, name):
    if not os.path.isdir(pj(path, name)):
        try:
            os.mkdir(pj(path, name))
        except:
            return False
    return True

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

def setup_repo(path, url, branch, local, orphan = False):
    f_list = list_dir(path)
    f_name = assure_unique('repo_', f_list)
    
    fpath = pj(path, name)
    os.mkdir(fpath)
    repo = Repo(fpath, shipyard = url)
    repo.set_shipyard(url)
    
    if orphan:
        repo.do_checkout(branch, orphan = True)
    else:
        if not local:
            repo.do_fetch(branch = branch)
        repo.do_checkout(branch, new = True, track = not local)
    return repo
    
def split_repo(repo, path):
    cur_branch = repo.get_cur_branch()
    url = repo.get_remotes()[0]['url']
    cur_name = cur_branch.nm
    base_name = cur_name.split('#')[0]
    
    new_name = '#'.join(base_name, get_idstring())
    
    repo.do_checkout(new_name, new = True)
    
    return setup_repo(path, url, cur_branch.rm, local = True)

def update_repo(repo):
    cur_branch = repo.get_cur_branch()
    rm = cur_branch.rm
    nm = cur_branch.nm
    
    repo.do_fetch(branch = rm)
    repo.do_merge_safe()
    push_err = repo.do_push()

    if push_err in [0, 2]:
        return 0
    if push_err in [1]:
        return 1
    if push_err in [-1]:
        return -1
    
    return -1
        
def manage_repos(repos, path, repo_list = None):
    if not repo_list:
        repo_list = repos
        
    new_repos = []
    
    for repo in repo_list:
        upd_err = update_repo(repo)
        
        if upd_err in [1]:
            new_repo = split_repo(repo, path)
            new_repos.append(new_repo)
            
            update_repo(new_repo)
            update_repo(repo)
    
    repos.extend(new_repos)

def update_folders(repos, path, core_dir_name, core_branch_name):
    master = Repo(pj(path, core_dir_name))
    url = master.get_remotes()[0]['url']
    
    folders = [ name for name in list_dir(path) if name != core_dir_name ]
    rts = []
    rts_owned = []
    r_paths = [repo.path for repo in repos]

    for f in folders:
        r_path = pj(path, f)
        if r_path in r_paths:
            repo = repos[repo_paths.index(r_path)]
        else
            repo = Repo()
            #Add checks for empty/corrupt repo!
            repos.append(repo)
            
        rts_owned.append(repo.get_cur_branch().rt)
    
    err_get, rem_branches = master.get_rem_branches()

    assert not err_get

    rts = [rem_branch.rt for rem_branch in rem_branches if rem_branch.rt != core_branch_name]

    for rt in rts:
        if rt in rts_owned:
            continue
        setup_repo(path, url, rt local = False)
        rts_owned.append(rt)

    manage_repos(repos, path)

def setup_master(path, url, core_dir_name, core_branch_name, new = False):
    r_path = pj(path, core_dir_name)
    m_repo = setup_repo(r_path, url, core_branch_name, local = not new)
    
def rm_any(path, cont_only == False):
    if not os.path.exists(path):
        return 1
    if os.path.isfile(path):
        os.remove(path)
        return 0
    
    for item in list_all(path):
        err = rm_any(pj(path, item))
        if err != 0:
            return err
        
    a_list = listdir(path)
    if a_list == None:
        if not cont_only:
            os.rmdir(path)
        return 0
    return 2

def open_data(d_name, f_name):
    
    d_path = str(d_name)
    f_path = pj(d_path, str(f_name))
    
    if not os.path.isfile(f_path):
        return 201, None
    
    with open(f_path, 'r') as f_data:
        try:
            data = json.load(f_data)
        except:
            return 202, None
            
    if not (type(data) is dict):
        return 203, None
    if not data.get('is_setup', False):
        return 204, None
    
    return 0, data

def setup_data(d_name, f_name, data):
    f_path = pj(d_name, f_name)
    if not assure_location(d_name):
        return 1
    
    with open(f_path, 'w') as f_data:
        json.dump(data, f_data)

def wipe_data():
    if os.path.exists(d_name):
        rm_any(d_name, cont_only = True)

def window_func():
    with gui_lock:
        app = gui_pipe['w_ref']
        
    app.mainloop()
    print('QUIT: Window')
    with gui_lock:
        gui_pipe['_DONE'] = True
        try:
            root.destroy()
        except:
            None
        #print("For real this time")
        return None

class Datafile:
    db_dict = {}
    ro = {}
    db_path = ""
    def __init__(self, db_path: str, new: bool = False, db_dict: dict):
        self.db_path = db_path
        if new:
            self.db_dict = db_dict
            self.update()
        else:
            with open(self.db_path, 'r') as db_file:
                self.db_dict = json.load(db_file)
    
    def update(self):
        with open(db_path, 'w') as db_file:
            json.dump(db_dict, db_file)
    
    def __enter__(self):
        return self.db_dict
    
    def __exit__(self):
        self.db_dict = copy.deepcopy(self.db_dict)
        self.ro = copy.deepcopy(self.db_dict)
        self.update()
    ## Thanks to http://effbot.org/zone/python-with-statement.htm

def set_win_mode(mode, s_mode, window):
    

data_dir_name = 'Stargit'
data_file_name = 'data.json'
data_path = pj(data_dir_name, data_file_name)
MODE = 0
SCREEN_MODE = -1
RUNNING = True

root = tk.Tk()
app = Application(master=root)
with gui_lock:
    gui_pipe['w_ref'] = app

err, data = open_data(data_dir_name, data_file_name)
if err == 0:
    db_main = Datafile(data_path)
    MODE = 1

if MODE == 1:
    if db_main.ro['has_repo']:
        MODE = 3
    if db_main.ro['has_remote']:
        MODE = 2

window_thread = thread.start_new_thread(window_func, ())
while RUNNING:
    time.sleep(0.05)
    with gui_lock:
        print(gui_pipe['l_sel'])
        if gui_pipe['_DONE']:
            RUNNING = False
    with db_main as db:
        if MODE == 0:
            set_win_mode(0, SCREEN_MODE, app)
            
    

print('QUIT: Main')
