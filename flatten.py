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

# Stash any changes (like to the flattening script)
repo.git.stash()
repo.git.checkout(DEVELOP_BRANCH)

# Delete all branches except master and develop
for branch in repo.branches:
    if branch.name != MASTER_BRANCH and branch.name != DEVELOP_BRANCH:
        repo.delete_head(branch)


# Get all parent commits of the tip of develop
start, max_count = 0, 100
revs = repo.git.rev_list(DEVELOP_BRANCH).split("\n")
for rev in revs:
    commit = repo.commit(rev)
    message = commit.message.strip()

    # Create a new branch with the same name as the commit
    new_branch = repo.create_head(message)
    new_branch.set_commit(commit)

    # Checkout and clean that branch
    new_branch.checkout()
    repo.git.clean("-fd")

    origin.push(new_branch)

    # Copy the state of the repository to temp dir
    target_dir = os.path.join(temp_dir,new_branch.name)
    shutil.copytree(repo_dir, target_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))


repo.git.checkout(MASTER_BRANCH)

# Copy all repo snapshots back to master
for branch in repo.branches:
    if branch.name != MASTER_BRANCH and branch.name != DEVELOP_BRANCH:
        source_dir = os.path.join(temp_dir,branch.name)
        target_dir = os.path.join(repo_dir,branch.name)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)

# Clean up our temp directory
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)



# Res
repo.git.stash("pop")

