from git import Repo
import os
import io
import shutil
import tempfile

IGNORE_PATTERNS = ('.git',"LICENSE")
MASTER_BRANCH = "master"
DEVELOP_BRANCH = "develop"
ORIGIN = "origin"

# Create a directory to stash the flattened folders
temp_dir = tempfile.mkdtemp()

repo_dir = os.getcwd()
repo = Repo(repo_dir)

origin = repo.remote(ORIGIN)
# print origin.git.branches

# print repo.git.branch("-r")

for branch in repo.git.branch("-r").split("\n"):
    name = branch.split("/")[-1]
    print name
    if name != MASTER_BRANCH and name != DEVELOP_BRANCH:
        repo.git.push(ORIGIN, ":" + name)


# repo.git.branch("-r")

# branch = repo.get_branch("origin/1-Exercise")

# repo.git.push("origin",":2-Exercise")

