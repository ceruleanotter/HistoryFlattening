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

print repo.remote(ORIGIN)
