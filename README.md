# History Flattening



Online courses often involve students following along in the step-by-step development process of an app. It is often useful to supply students with a zip containing many folders with snapshots of the app at different points in time. It is even more useful to supply pairs of folders, one for the starting point of an exercise, and one for the solution to the exercise.

The difficulty arises in maintaining consistency across those folders when a change must be made to the app. This script and associated workflow allows an instructor to make updates to their app, and automatically generate

## Usage

First, create a develop branch containing one commit for each snapshot you want students to see. This can be constructed with the help of:

    git rebase -i -root

When you've created this clean history, checkout master, and run flatten.py from the root.


