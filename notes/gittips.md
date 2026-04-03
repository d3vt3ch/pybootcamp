# Collection of github command & Tips

## Simplified version to start from main Pull an create new branch

```bash
git status
git checkout main
git pull origin main
git checkout -b day3
```


## How to update last commit and merge the current branch to main

day3 → commit → push → main → pull → merge → push

```bash
git add .
git commit -m "complete day3 work"
git push -u origin day3

git checkout main
git branch

git pull origin main
git merge day3

git push origin main

```



## Explaination for check , pull and create branch new branch to work with.

How to check any pending 
then pull from main
then create branch day 3/4/5

```bash
git status
👉 Must be clean (no pending changes)

What your commands do

git checkout main
👉 Switch to main branch

git pull
👉 Get latest updates from GitHub

git checkout -b day3
👉 Create new branch day3 from updated main
```


## How to update 
```bash
git add .
git commit -m "the work i just done"
git push
```




## Create .gitignore
👉 “Git, ignore all these files forever”

```bash
touch .gitignore
git add .gitignore
git commit -m "add .gitignore"
```

When merge becomes messy (conflicts)
Difference between merge vs rebase
Proper real-world workflow (very useful for your bootcamp)
VS Code UI way to resolve conflicts (very easy)
Difference between merge conflict vs rebase conflict
Real workflow used in companies
rebase workflow (clean history, used by senior devs)
🔥 How big teams avoid conflicts almost completely
🔥 GitHub + VS Code integration (super fast workflow)