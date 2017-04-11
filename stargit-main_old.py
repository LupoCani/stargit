from dulwich import porcelain as prc

#repo = prc.open_repo("temp_stage") or prc.init("temp_stage")
remote = b"https://github.com/LupoCani/stargit-exp-store.git"

repo = prc.clone(remote, target=b"temp_stage")
handle = open("temp_stage/DONTREADME", "w")
handle.write("Hello world!")
handle.close()

prc.add(repo, "DONTREADME")
prc.commit(repo, b"HW commit.")

remote = "https://github.com/LupoCani/stargit-exp-store.git"

prc.push(repo, "https://LupoCani:******@github.com/LupoCani/stargit-exp-store.git")
