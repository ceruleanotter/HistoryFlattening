from git import Repo
import os
import io
import shutil
import tempfile

IGNORE_PATTERNS = ('.git',"LICENSE")
SAFE_CHARS = ["-", "_", "."]
BRANCH_NAME_MAX_LENGTH = 100

MASTER_BRANCH = "master"
DEVELOP_BRANCH = "develop"
ORIGIN = "origin"

# Create a directory to stash the flattened folders
temp_dir = tempfile.mkdtemp()

repo_dir = os.getcwd()
repo = Repo(repo_dir)

origin = repo.remote(ORIGIN)



# Delete all remote branches except master and develop
for branch in repo.git.branch("-r").split("\n"):
    name = branch.split("/")[-1].strip()
    remote = branch.split("/")[0].strip()
    print branch, name, remote
    if name != MASTER_BRANCH and remote == ORIGIN:
        print "Removing remote branch:", name
        repo.git.push(ORIGIN, ":" + name)

repo.git.push(origin, DEVELOP_BRANCH)

for branch in repo.branches:
    if branch.name != MASTER_BRANCH and branch.name != DEVELOP_BRANCH:
        repo.git.branch(branch.name, "-D")

# Stash any changes (like to the flattening script)
print "Stashing"
repo.git.stash()
repo.git.checkout(DEVELOP_BRANCH)

# Get all parent commits of the tip of develop
revs = repo.git.rev_list(DEVELOP_BRANCH).split("\n")
for rev in revs:

    commit = repo.commit(rev)

    message = commit.message.split("\n")[0]

    safe_message = "".join(c for c in message if c.isalnum() or c in SAFE_CHARS).strip()
    branch_name = safe_message[:BRANCH_NAME_MAX_LENGTH] if len(safe_message) > BRANCH_NAME_MAX_LENGTH else safe_message

    print "Creating a branch for:", branch_name

    # Create a new branch with the same name as the commit
    new_branch = repo.create_head(branch_name)
    new_branch.set_commit(rev)

    # Checkout and clean that branch
    new_branch.checkout()
    repo.git.clean("-fd")

    print "Pushing:", branch_name
    origin.push(new_branch)

    # Copy the state of the repository to temp dir
    target_dir = os.path.join(temp_dir,new_branch.name)
    shutil.copytree(repo_dir, target_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))


print "Checking out master and copying in the snapshots"
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
print "Popping"
if repo.git.stash("list"):
    repo.git.stash("pop")



