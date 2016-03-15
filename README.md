# History Flattening

Online courses often involve students following along in the step-by-step development process of an app. It is often useful to supply students with a zip containing many folders with snapshots of the app at different points in time. It is even more useful to supply pairs of folders, one for the starting point of an exercise, and one for the solution to the exercise.

The difficulty arises in maintaining consistency across those folders when a change must be made to the app. This script and associated workflow allows an instructor to make updates to their app and automatically generate consistent snapshot folders.

You'll need [GitPython](https://github.com/gitpython-developers/GitPython) to run:

    pip install gitpython

## Usage

First, we need two branches, henceforth referred to as `student` and `develop`. The `develop` branch should contain one commit for each snapshot you want students to see. This can be constructed with the help of:

    git rebase -i -root

Note that since the commit names will be transformed into both branch names and folder names, you must be sure to name your commits in a way that will safely translate. The script will remove all character that are not alphanumeric, periods, and dashes. It will also truncate names to 100 characters.

Next, you'll need a new `student` branch that is an orphan, that is, it has no history. This can be created using

    git checkout --orphan student

You can now run `flatten.py`. If you run it from your repository root directory and use the branch names `student` and `develop`, and have a remote named `origin`, you don't need any command line arguments.

It will first delete all local branches except `student` and `develop`. It will then create a branch for each parent commit of `develop` (using a cleaned version of the commit message as a branch name). Next, it will checkout and clean each branch it just created, and copy the working tree to a temporary directory (in a subdirectory with the same name as the branch).

It will then check out `student`, and copy the temporary directory to the working tree.

Reviewing and committing the changes to `student` is left up to the user. As is pushing the generated branches. This can be done using

    git push origin --all --prune

## Making Changes

So let's say that you've created your whole app with its beautiful clean history, and now you discover a mistake that you made waaaaaay back at the start. If you wanted to fix it in every folder, you'd have a horrible copy paste job on your hands. Unless, of course, you use this script.

So first thing, make the change and clean up the history again. You can do this using an interactive rebase. First you need to check out the `develop` branch and run

    git rebase -i -root

That will take you to a file containing a list of every parent commit of the `develop` branch, going back to the start of time. You can mark any commit that needs changing by replacing `pick` with `edit`. Then save and close the file.

You will then be taken back in time to right after the first commit you marked `edit`. Make any changes you need, then run

    git add -u
    git commit --amend

This will take you to the normal commit file. It's important that you keep the same commit name. Finally, run

    git rebase --continue

This will take you to the next commit you marked `edit`, or, if there are no more left, will dump you back at `develop`. Now your history is clean again, and you can checkout `student`, and re-run the script.
