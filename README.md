# mytribe-backend
### Rules to be followed beafore pushing anything on this repo
```
1.] No direct push should be made unless very emergency case on the main, qa and dev branch
2.] Create ur own branch and push your changes with that branch and create pull request to dev branch

    Branch        | Info
    ------------- | -----------------------------
    main          | this is our production branch
    qa            | this is our testing branch
    dev           | this is our development branch

3.] Nothing should be direclty commited on these three branches as this will be live servers and changes made directly can result into failure if some buggy code is there
4.] Every PR made will be reviewed by each team member and then only PR will be approved and merged on 'dev' branch.
```
Please follow the above rule in order to maintain consistent code reviewing system and maintain proper flow of data in each branch

### Rules for Writing comments before pushing and before rasing PR
```
1.] When we commit chnages on our local branch "Mention what changes have u made in short" i.e comment should be one liner.
2.] When raising PR you need to follow,
        i.] What changes are made in detail
        ii.] State of code before changes were done
        iii.] Logic behind chnages made and code logic in brief
```
This will help code reviewers to manage and understand code easily and will maintain ur proof of work.
