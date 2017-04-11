import git
import os
#from os.path import join as pj

def repo_ft(tuple_in):
    return git.Repo(os.path.join(*tuple_in))

def assure_origin(path, url):
    repo = repo_ft(path)
    origin = repo.remotes.get('origin', False) or repo.create_remote('origin', remote)

def destroy_origin(path):
    repo = repo_ft(path)
    for remote in repo.remotes:
        repo.remove_remote(remote)

def get_branch_current(path):
    repo = repo_ft(path)

    tag = ""
    try:
        tag = repo.active_branch.name
    except:
        for tag_pot in repo.heads:
            if repo.active_branch == repo.heads[tag_pot]:
                tag = tag_pot
    return tag

flagbook_push = {
    512: 0,     #Success
    1032: 1,    #Failure: Somebody else got there first
    512: 0}     #Success: Nothing to update                

def try_push(path, url):
    repo = repo_ft(path)
    branch_name = get_branch_current(spath, name)
    origin = assure_origin(path, url)
    
    push_info = origin.push(branch_name)
    flag = push_info[0].flags
    code = flagbook_push.get(flag, -1)
    destroy_origin(path)
    return code

def list_files(path)
    dirpath = os.path.join(*path)
    file_list = onlyfiles =
    [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f)) and not (f.startswith(".git/") or f.startswith(".git\\"))]
    return file_list

def do_commit(path):
    repo = repo_ft(path)
    files = list_files(path)

    repo.index.add(files)
    repo.index.commit("modified")


assert False

rpath = "https://LupoCani:******@github.com/LupoCani/stargit-exp-store.git"
dpath = "temp_stage"

try:
    repo = git.Repo(dpath)
except Exception as e:
    print(e)
    repo = git.Repo.clone_from(rpath, dpath)

repo.heads.master.checkout()

origin = repo.remotes.origin or repo.create_remote('origin', rpath)

handle = open(dpath + "/AVIDLYREADME", "w")
handle.write("Lorem ipsum")
handle.close()

author = git.Actor("LupoCani", "gunnar.wickbom@gmail.com")

print(repo.index.add(onlyfiles))

repo.index.commit("EMPTY")#, committer=author, author=author)

#assert False
info = origin.push()[0]

if (info.flags == 1032):
    print("splitting")
    new_branch = repo.create_head('diverge')
    new_branch.set_commit(repo.active_branch.commit)
    repo.active_branch.set_commit('HEAD~1')
    repo.heads['diverge'].checkout()
    origin.push("diverge")

print("Still Alive!")
