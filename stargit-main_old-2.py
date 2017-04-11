import git

rpath = "https://LupoCani:******@github.com/LupoCani/stargit-exp-store.git"
dpath = "temp_stage"

#resp = git.Repo.clone_from(rpath, dpath)

try:
    resp = git.Repo(dpath)
except Exception as e:
    print(e)
    resp = git.Repo.clone_from(rpath, dpath)

rsp = resp.git

#rsp.checkout("--orphan", "new_branch_7")
#rsp.rm("-rf", ".")

rsp.checkout("master")
#rsp.fetch()
#rsp.reset("FETCH_HEAD", "--hard")

#wait = input("PRESS ENTER TO CONTINUE.")

#try:
#    origin = resp.remotes.origin
#except:
#    origin = resp.create_remote('origin', rpath)

origin = resp.remotes.origin or resp.create_remote('origin', rpath)

handle = open(dpath + "/DONTREADME", "w")
handle.write("Hello world new!")
handle.close()

rsp.add(".")
try:
    rsp.commit("-m", "EMPTY_9")
except:
    None
    
#rsp.push(rpath)#, "new_branch_7")

info = origin.push()[0]

if (info.flags == 1032):
    print("splitting")
    new_branch = resp.create_head('diverge')
    new_branch.set_commit(resp.active_branch.commit)
    resp.active_branch.set_commit('HEAD~1')
    resp.head.reference = new_branch
    #origin.push("--set-upstream")[0]
    rsp.push("--set-upstream", rpath, 'diverge')
    

print("Still Alive!")
