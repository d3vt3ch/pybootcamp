# VS Code Setup & Shortcuts

---
# Day X - Topic

## 📌 Concept
## ⚙️ Commands
## ✅ Steps
## 💡 Tips
## ❌ Mistakes
## ✅ Summary

---

## ⚠️ Issue: Cannot run `code --version`

### 📌 Problem
The `code` command is not recognized in terminal.

### ✅ Solution

Be a responsible coder
about database handling and security
for any data


1. Open Visual Studio Code  
2. Press `Cmd (⌘) + Shift + P`  
3. Search for:  
   `Shell Command: Install 'code' command in PATH`  
4. Click and install  

### 💡 Tip
Restart your terminal after installation.

---

## 💻 How to Comment Code in Bulk

### ✅ Steps

1. Highlight the code  
2. Press `Cmd (⌘) + /`  

### 💡 Tip
- Works for most languages in VS Code  
- Use again to **uncomment**

### 💡 to pull from main and create branch 
```bash
git checkout main
git pull
git checkout -b day3
```

git status
👉 Must be clean (no pending changes)

What your commands do

git checkout main
👉 Switch to main branch

git pull
👉 Get latest updates from GitHub

git checkout -b day3
👉 Create new branch day3 from updated main

git checkout main
git pull origin main
git checkout -b day3

 Keyword   | Meaning          |
| --------- | ---------------- |
| `try`     | Try this code    |
| `except`  | If error happens |
| `else`    | If no error      |
| `finally` | Always run       |

```python
try:
    # risky code
except:
    # handle error
else:
    # runs if NO error
finally:
    # always runs
```
