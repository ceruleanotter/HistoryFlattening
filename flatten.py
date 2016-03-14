from git import Repo
import os
import io
import shutil
import sys
import getopt
import tempfile
import argparse

IGNORE_PATTERNS = ('.git')
SAFE_CHARS = ["-", "_", "."]
MAX_LENGTH = 100

STUDENT_BRANCH = "master"
DEVELOP_BRANCH = "develop"
ORIGIN = "origin"

# Create a directory to stash the flattened folders

class Flattener:

    def __init__(
        self,
        repo_dir,
        student_branch,
        develop_branch,
        remote
        ):

        if repo_dir is None:
            repo_dir = os.getcwd()
        self.repo_dir = repo_dir

        self.repo = Repo(self.repo_dir)
        self.remote = self.repo.remote(remote)
        self.student = student_branch
        self.develop = develop_branch


    def flatten(self):
        self.remove_local_branches()
        self.create_local_branches()


        try:
            temp_dir = tempfile.mkdtemp()
            print "Stashing"
            self.repo.git.stash()
            current_branch = self.repo.active_branch

            self.copy_snapshots_to_temp_dir(temp_dir)
            self.copy_snapshots_to_student_branch(temp_dir)
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            self.repo.git.checkout(current_branch)
            print "Popping"
            if self.repo.git.stash("list"):
                self.repo.git.stash("pop")

        self.remove_remote_branches()
        # update_remote_branches(repo, master, remote)



    def remove_local_branches(self):
        for branch in self.repo.branches:
            if branch.name != self.student and branch.name != self.develop:
                print "Removing local branch:", branch.name
                self.repo.git.branch(branch.name, "-D")


    def create_local_branches(self):
        for rev in self.repo.git.rev_list(self.develop).split("\n"):
            commit = self.repo.commit(rev)
            branch_name = self.clean_commit_message(commit.message)

            print "Creating local branch:", branch_name
            new_branch = self.repo.create_head(branch_name)
            new_branch.set_commit(rev)

    def clean_commit_message(self, message):
        first_line = message.split("\n")[0]
        safe_message = "".join(c for c in message if c.isalnum() or c in SAFE_CHARS).strip()
        return safe_message[:MAX_LENGTH] if len(safe_message) > MAX_LENGTH else safe_message

    def copy_snapshots_to_temp_dir(self, temp_dir):

        for branch in self.repo.branches:
            if branch.name != self.student and branch.name != self.develop:
                branch.checkout()
                print "Saving snapshot of:", branch.name
                self.repo.git.clean("-fd")
                target_dir = os.path.join(temp_dir,branch.name)
                shutil.copytree(self.repo_dir, target_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))


    def copy_snapshots_to_student_branch(self, temp_dir):
        for branch in self.repo.branches:
            if branch.name != self.student and branch.name != self.develop:
                source_dir = os.path.join(temp_dir,branch.name)
                target_dir = os.path.join(self.repo_dir,branch.name)
                print "Copying snapshot of:", branch.name
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                shutil.copytree(source_dir, target_dir)

# # Clean up our temp directory

#     finally:
#         repo.git.checkout(MASTER_BRANCH)
#         print "Popping"
#         if repo.git.stash("list"):
#             repo.git.stash("pop")

    def remove_remote_branches(self):
    # Delete all remote branches except master
        for branch in self.repo.git.branch("-r").split("\n"):
            name = branch.split("/")[-1].strip()
            remote = branch.split("/")[0].strip()
            if name != self.student and remote == self.remote:
                print "Removing remote branch:", name
                self.repo.git.push(target_remote, ":" + name)


    def update_remote_branches(self):
        for branch in self.repo.branches:
            if branch.name != self.student:
                print "Pushing", branch.name
                self.remote.push(all=true)


# def push_develop
#     print "Pushing", DEVELOP_BRANCH
#     repo.git.push(origin, DEVELOP_BRANCH)


# def copy_snapshots_to_temp_dir(temp_dir):
#     try:
#         print "Stashing"
#         repo.git.stash()
#         for rev in repo.git.rev_list(DEVELOP_BRANCH).split("\n"):
#             commit = repo.commit(rev)
#             branch_name = clean_commit_message(commit.message)

#             print "Creating a branch for:", branch_name
#             new_branch = repo.create_head(branch_name)
#             new_branch.set_commit(rev)

#             # Checkout and clean that branch
#             new_branch.checkout()
#             repo.git.clean("-fd")

#             print "Pushing:", branch_name
#             origin.push(new_branch)

#             # Copy the state of the repository to temp dir
#             target_dir = os.path.join(temp_dir,new_branch.name)
#             shutil.copytree(repo_dir, target_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

#     finally:
#         repo.git.checkout(MASTER_BRANCH)
#         print "Popping"
#         if repo.git.stash("list"):
#             repo.git.stash("pop")




# def push_branches(devlop_branch):



# # Stash any changes (like to the flattening script)
# print "Stashing"
# repo.git.stash()
# repo.git.checkout(DEVELOP_BRANCH)

# # Get all parent commits of the tip of develop
# revs = repo.git.rev_list(DEVELOP_BRANCH).split("\n")
# for rev in revs:

#     commit = repo.commit(rev)

#     message = commit.message.split("\n")[0]

#     safe_message = "".join(c for c in message if c.isalnum() or c in SAFE_CHARS).strip()
#     branch_name = safe_message[:BRANCH_NAME_MAX_LENGTH] if len(safe_message) > BRANCH_NAME_MAX_LENGTH else safe_message

#     print "Creating a branch for:", branch_name

#     # Create a new branch with the same name as the commit
#     new_branch = repo.create_head(branch_name)
#     new_branch.set_commit(rev)

#     # Checkout and clean that branch
#     new_branch.checkout()
#     repo.git.clean("-fd")

#     print "Pushing:", branch_name
#     origin.push(new_branch)

#     # Copy the state of the repository to temp dir
#     target_dir = os.path.join(temp_dir,new_branch.name)
#     shutil.copytree(repo_dir, target_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))


# print "Checking out master and copying in the snapshots."
# repo.git.checkout(MASTER_BRANCH)

# # Copy all repo snapshots back to master
# for branch in repo.branches:
#     if branch.name != MASTER_BRANCH and branch.name != DEVELOP_BRANCH:
#         source_dir = os.path.join(temp_dir,branch.name)
#         target_dir = os.path.join(repo_dir,branch.name)
#         if os.path.exists(target_dir):
#             shutil.rmtree(target_dir)
#         shutil.copytree(source_dir, target_dir)

# # Clean up our temp directory


# # Res
# print "Popping"
# if repo.git.stash("list"):
#     repo.git.stash("pop")





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repodir')
    parser.add_argument('--student', default = STUDENT_BRANCH)
    parser.add_argument('--develop', default = DEVELOP_BRANCH)
    parser.add_argument('--remote', default = ORIGIN)

    parsed = parser.parse_args()

    flattener = Flattener(parsed.repodir,parsed.student, parsed.develop, parsed.remote)
    flattener.flatten()



    # parser.print_help()

    # if argv is None:
    #     argv = sys.argv
    # try:
    #     try:
    #         opts, args = getopt.getopt(argv[1:], "h", ["help"])
    #     except getopt.error, msg:
    #          raise Usage(msg)
    #     # more code, unchanged
    # except Usage, err:
    #     print >>sys.stderr, err.msg
    #     print >>sys.stderr, "for help use --help"
    #     return 2

if __name__ == "__main__":
    sys.exit(main())


