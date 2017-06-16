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
    import threading
except ImportError:
    import dummy_threading as threading
    
def say_hi():
        print("hi there, everyone!")

s1 = ''
s2 = u'\u251c' + ' '
s3 = u'\u2514' + ' '

gui_lock = threading.Lock()
gui_pipe = {
    '_DONE': False,
    'sel_listbox': None,
    'ref_app': None,
    'event_queue': [],

    'ship_list': []
    }

class Application(tk.Frame):
    def list_on_select(self, event):
        widget = event.widget
        value = widget.curselection()[0]
        print(str(value))
        self.lbl_title.config(text=widget.get(value))
        with gui_lock:
            gui_pipe['sel_listbox'] = value
            
    def force_select(self):
        self.listbox.select_clear(0, tk.END)
        self.listbox.select_set(2)
        self.listbox.activate(2)
        self.listbox.event_generate("<<ListboxSelect>>")
        
    def createWidgets(self):
        #self.QUIT = tk.Button(self)
        #self.QUIT["text"] = "QUIT"
        #self.QUIT["fg"]   = "red"
        #self.QUIT["command"] =  self.quit
        #self.QUIT.grid(row=0, column=1)

        #self.hi_there = tk.Button(self)
        #self.hi_there["text"] = "Hello",
        #self.hi_there["command"] = say_hi
        #self.hi_there.grid(row=1, column=1)
        
        self.listbox = tk.Listbox(self, width=40, height=15, font=('consolas', 10), selectmode=tk.SINGLE)
        self.listbox.bind('<<ListboxSelect>>', self.list_on_select)
        self.listbox.grid(row=0, column=0, rowspan=8, padx = 10, pady = 10)
        
        self.listbox.insert(tk.END, s1 + "Test")
        str(self.listbox.delete(20))
        self.listbox.insert(3, s3 + "Dolor")
        self.listbox.insert(20, s3 + "Grande")
        
        self.lbl_title = tk.Label(self, text = 'Ship Name')
        self.lbl_title.grid(row = 0, column = 1, columnspan = 2)
        
        self.btn_deploy = tk.Button(self, text = 'Deploy', command=self.force_select)
        self.btn_deploy.grid(row = 1, column = 1, sticky=tk.S+tk.W+tk.E)

        self.btn_retract = tk.Button(self, text = 'Retract')
        self.btn_retract.grid(row = 1, column = 2, sticky=tk.S+tk.W+tk.E)

        self.btn_pull = tk.Button(self, text = 'Pull')
        self.btn_pull.grid(row = 2, column = 1, sticky=tk.N+tk.W+tk.E)

        self.btn_discard = tk.Button(self, text = 'Discard')
        self.btn_discard.grid(row = 2, column = 2, sticky=tk.N+tk.W+tk.E)

        self.btn_sync = tk.Button(self, text = 'Sync')
        self.btn_sync.grid(row = 3, column = 1, columnspan=2, sticky=tk.N+tk.W+tk.E)

        self.cbx_auto = tk.Checkbutton(self, text = 'Autosync')
        self.cbx_auto.grid(row = 4, column = 1, columnspan=2, sticky=tk.W)

        #'All' versions
        self.btn_deploy_all = tk.Button(self, text = 'Deploy All')
        self.btn_deploy_all.grid(row = 5, column = 1, sticky=tk.S+tk.W+tk.E)

        self.btn_retract_all = tk.Button(self, text = 'Retract All')
        self.btn_retract_all.grid(row = 5, column = 2, sticky=tk.S+tk.W+tk.E)

        self.btn_pull_all = tk.Button(self, text = 'Pull All')
        self.btn_pull_all.grid(row = 6, column = 1, sticky=tk.N+tk.W+tk.E)

        self.btn_discard_all = tk.Button(self, text = 'Discard All')
        self.btn_discard_all.grid(row = 6, column = 2, sticky=tk.N+tk.W+tk.E)

        self.btn_sync_all = tk.Button(self, text = 'Sync All')
        self.btn_sync_all.grid(row = 7, column = 1, columnspan=2, sticky=tk.N+tk.W+tk.E)
        
        self.cbx_auto_all = tk.Checkbutton(self, text = 'Autosync all')
        self.cbx_auto_all.grid(row = 8, column = 1, columnspan=2, sticky=tk.W)

        with gui_lock:
            gui_pipe['ref_app'] = self

        self.listbox.select_set(1)
        self.listbox.activate(1)
        self.listbox.event_generate("<<ListboxSelect>>")
            
    def set_mode(self, mode):
        if mode == 0:
            #self.btn_deploy.config(state=tk.DISABLED)
            self.btn_retract.config(state=tk.DISABLED)
            self.btn_pull.config(state=tk.DISABLED)
            self.btn_discard.config(state=tk.DISABLED)
            self.btn_sync.config(state=tk.DISABLED)
            self.cbx_auto.config(state=tk.DISABLED)
            
            self.btn_deploy_all.config(state=tk.DISABLED)
            self.btn_retract_all.config(state=tk.DISABLED)
            self.btn_pull_all.config(state=tk.DISABLED)
            self.btn_discard_all.config(state=tk.DISABLED)
            self.btn_sync_all.config(state=tk.DISABLED)
            self.cbx_auto_all.config(state=tk.DISABLED)
        
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.created = False

#Thanks to http://effbot.org/tkinterbook/grid.htm
        
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
                'nm':  rem[0],  #Name
                'url': rem[1]   #URL
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
                    current = len(branchlist)   #The current size of the list, also the index of the next item to be appended, IE this one
                    strings = strings[1:]       #Remove asterisk
                info = []
                info['nm'] = strings[0]     #Branch name
                info['sh'] = strings[1]     #Hash
                info['cm'] = strings[-1]    #Commit?
                info['rt'] = None           #Remote

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
    ##Errors:
    #1: Branches diverged
    #0: Success
        
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
    ##Errors:
    #1: Branches diverged
    #2: No changes
    #101: Internet connection failed
    #-1: Unknown error
    #0: Sucess
    
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
    if push_err in [101]:
        return 101
    
    return -1
    ##Errors:
    #1: Branches diverged
    #101: Network error
    #-1: Unknown error
    #0: Success
    
def manage_repos(repos, path, repo_list = None):
    '''Updates repositories. Specify one or more repos in repo_list to update those specificallly, else, update all repos.'''
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
    
    folders = [ name for name in list_dir(path)
                if name != core_dir_name
                and os.path.isdir(pj(path, name))]
    rts = []
    rts_owned = []
    r_paths = [repo.path for repo in repos]

    for f in folders:
        r_path = pj(path, f)
        if r_path in r_paths:
            repo = repos[repo_paths.index(r_path)]
        else:
            repo = Repo(r_path)
            #Add checks for empty/corrupt repo!
            repos.append(repo)
            
        rts_owned.append(repo.get_cur_branch().rt)
    
    err_get, rem_branches = master.get_rem_branches()

    assert not err_get

    rts = [rem_branch.rt for rem_branch in rem_branches
           if rem_branch.rt != core_branch_name
           and not rem_branch.rt in rts_owned]

    for rt in rts:
        setup_repo(path, url, local = False)
        rts_owned.append(rt)

    manage_repos(repos, path)

def setup_master(path, url, core_dir_name, core_branch_name, new = False):
    r_path = pj(path, core_dir_name)
    m_repo = setup_repo(r_path, url, core_branch_name, local = not new)
    
def rm_any(path, cont_only = False):
    if not os.path.exists(path):
        return 1
    if os.path.isfile(path):
        try:
            os.remove(path)
        except:
            return 3
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

##Errors:
#201: file not found
#202: file contents corrupted
#203: file contents not dictionary
#204: data incomplete
#0: success

def setup_data(d_name, f_name, data):
    f_path = pj(d_name, f_name)
    if not assure_location(d_name):
        return 1

    try:
        with open(f_path, 'w') as f_data:
            json.dump(data, f_data)
    except:
        return 2
    return 0

##Errors:
#1: file already exists
#2: write failure
#0: sucess

def wipe_data():
    if os.path.exists(d_name):
        rm_any(d_name, cont_only = True)

class Window_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        
    def run(self):
        root = tk.Tk()
        app = Application(master=root)
        with gui_lock:
            gui_pipe['w_ref'] = app
        try:
            app.mainloop()
        except Exception as excep:
            print('-> Window exception: ' + str(excep))
        except:
            print('-> Unknown window exception.')
        finally:
            print('-> exiting winow')
            with gui_lock:
                gui_pipe['_DONE'] = True
                try:
                    root.destroy()
                except Exception as excep:
                    print('-> Root destruction exception: ' + str(excep))
                except:
                    print('-> Unknown root destruction exception.')
            print('QUIT: Window ')
            return None

class Datafile:
    ''' Tiny database system with 'with' hooks to ensure data is always witten to disk'''
    db_dict = {}
    ro = {}
    db_path = ""
    decoupled = False
    def __init__(self, db_path: str, new: bool = False, db_dict: dict = {}):
        self.db_path = str(db_path)
        if len(self.db_path) == 0:
            new = True
            self.decoupled = True
        if new:
            self.db_dict = db_dict
            self.update()
        else:
            with open(self.db_path, 'r') as db_file:
                self.db_dict = json.load(db_file)
    
    def update(self):
        if self.decoupled:
            return
        with open(db_path, 'w') as db_file:
            json.dump(db_dict, db_file)
            
    def couple(self, db_path):
        self.db_path = db_path
        self.decoupled = False
        self.update()
        
    def __enter__(self):
        return self.db_dict
    
    def __exit__(self, exception_type, exception_value, traceback):
        if exception_value != None:
            raise exception_value
        self.db_dict = copy.deepcopy(self.db_dict)
        self.ro = copy.deepcopy(self.db_dict)
        self.update()
    ## Thanks to http://effbot.org/zone/python-with-statement.htm

class Ship():
    def __init__(self, path):
        self.path = path
        self.repo = Repository(path)
        self.data = Datafile(path)

def compile_screen_data(ships, db):
    data_list = []
    for ship in ships:
        data = {}
        data['name'] = ship.data.ro['name']
        data['updated'] = ""
        data['deployed'] = ""

data_dir_name = 'Stargit'
repo_dir_name = pj(data_dir_name, 'repositories')
data_file_name = 'data.json'
data_path = pj(data_dir_name, data_file_name)
MODE = 0
MODE_ACTIVE = None
SCREEN_MODE = -1
RUNNING = True
repos = []



err, data = open_data(data_dir_name, data_file_name)
if err == 0:
    db_main = Datafile(data_path)
    MODE = 1
else:
    db_main = Datafile('')

print("DB_err: " + str(err))

if MODE == 1:
    if db_main.ro['has_repo']:
        MODE = 3
    if db_main.ro['has_remote']:
        MODE = 2

window_thread = Window_thread()
time.sleep(1)
with gui_lock:
    app = gui_pipe['w_ref']

while RUNNING:
    print("MODE: " + str(MODE))
    time.sleep(0.05)
    with gui_lock:
        print('l_sel: ' + str(gui_pipe['sel_listbox']))
        if gui_pipe['_DONE']:
            RUNNING = False
            
    with db_main as db:
        app.set_mode(MODE)
        if MODE == 0:
            pass
            MODE_ACTIVE = 0
        if MODE == 4:
            #if MODE_ACTIVE != MODE:
            #    repos = update_folders(repos, repo_dir_name, 'repo_main', 'stargit_master');
            with gui_lock:
                pass
                
    

print('QUIT: Main')
