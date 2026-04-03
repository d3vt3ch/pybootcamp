
# Simplified version for creating a branch

```bash
git status
git checkout main
git pull origin main
git checkout -b day3
```

# Simplified version for push , update , and merge into main.

```bash
git status 
git add . 
git commit -m "done for day 3" git push

git checkout main 
git pull origin main
git merge day3
git push origin main
```

# Expaination

## for check , pull and create branch new branch to work with.


then pull from main
then create branch day 3/4/5

```bash
git status                      # How to check any pending 👉 Must be clean (no pending changes)
git checkout main               #👉 Switch to main branch
git pull                        #👉 Get latest updates from GitHub
git checkout -b day3            #👉 Create new branch day3 from updated main
```
## to merge branch with main

work on branch → commit → push → switch to main → merge → push
```bash
git checkout main       #Switch to main branch
git pull origin main    #Pull latest version of main (important habit)
git merge day3          #Merge day3 into main “Take everything from day3 and combine into main”
git push origin main    #Push updated main to GitHub

```



