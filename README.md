# History Flattening



Online courses often involve students following along in the step-by-step development process of an app. It is often useful to supply students with a zip containing many folders with snapshots of the app at different points in time. It is even more useful to supply pairs of folders, one for the starting point of an exercise, and one for the solution to the exercise.

The difficulty arises in maintaining consistency across those folders when a change must be made to the app. This script and associated workflow allows an instructor to make updates to their app, and automatically generate

## Usage

First, create a `develop` branch containing one commit for each snapshot you want students to see. This can be constructed with the help of:

    git rebase -i -root

Note that since the commit names will be transformed into both branch names and folder names, you must be sure to name your commits in a way that will safely translate. To be safest, use only alphanumeric characters and dashes. The script will try to

When you've created this clean history, checkout master, and run flatten.py from the root. It will first delete all the branches except `master` from `origin` (probably you GitHub repo). Next, it will check out each parent commit of `develop` in turn, clean the working tree, and save the contents of that tree to a temporary directory with the same name as the commit message.

It will also create a new branch at that commit, also with the same name as the commit message, and push that branch to origin.

Finally, it will checkout master, and copy in all those temporary directories. Reviewing and committing the changes to master is left up to the user.

## Making Changes

So let's say that you've created your whole app with its beautiful clean history, and now you discover a mistake that you made waaaaaay back at the start. If you wanted to fix it in every folder, you'd have a horrible copy paste job on your hands. Unless, of course, you use this script.

So first thing, make the change and clean up the history again. You can do this using an interactive rebase. First you need to check out the develop branch and run

    git rebase -i -root

That will take you to a file containing a list of every parent commit of the develop branch, going back to the start of time. You can mark any commit that needs changing by replacing `pick` with `edit`. Then save and close the file.

You will then be taken back in time to right after the first commit you marked `edit`. Make any changes you need, then run

    git add -u
    git commit --amend

This will take you to the normal commit file. It's important that you keep the same commit name. Finally, run

    git rebase --continue

This will take you to the next commit you marked `edit`, or, if there are no more left, will dump you back at `develop`. Now your history is clean again, and you can checkout master, and re-run the script.
