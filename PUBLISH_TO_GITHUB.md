# How to Publish This as a Public GitHub Template

Follow these steps once to create the public repo your beta clients will clone from.

---

## Step 1 — Create the Public Repo on GitHub

1. Go to **github.com** and sign in
2. Click the **+** in the top right → **New repository**
3. Fill in:
   - **Repository name:** `agent-sms-server`
   - **Description:** `Give your AI agents their own phone numbers`
   - **Visibility:** ✅ Public
   - **Initialize with README:** ❌ No (we have one already)
4. Click **Create repository**
5. Copy the repo URL — it will look like:
   `https://github.com/YOUR-USERNAME/agent-sms-server.git`

---

## Step 2 — Connect and Push from Terminal

Open Terminal, navigate to this folder, and run:

```bash
cd "/Users/tars/Documents/Claude/Projects/AI Agents/agent-sms-server"

# Point the repo to your new GitHub URL
git remote set-url origin https://github.com/YOUR-USERNAME/agent-sms-server.git

# Stage all the cleaned-up files
git add .
git commit -m "Clean public template — ready for beta clients"

# Push to GitHub
git push -u origin main
```

If prompted for a password, use a **Personal Access Token** (not your GitHub password):
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token → check **repo** → copy it → paste as your password

---

## Step 3 — Update the Clone URL in SETUP_GUIDE.md

Once the repo is live, update Step 3 in SETUP_GUIDE.md:

Replace:
```
https://github.com/mybusinessgenie-ai/agent-sms-server.git
```

With your actual URL:
```
https://github.com/YOUR-USERNAME/agent-sms-server.git
```

Then push the update:
```bash
git add SETUP_GUIDE.md
git commit -m "Update clone URL"
git push
```

---

## Step 4 — Share with Beta Clients

Send your beta client the link to your repo's SETUP_GUIDE.md. They'll open it on GitHub and follow the steps from there.

Direct link format:
```
https://github.com/YOUR-USERNAME/agent-sms-server/blob/main/SETUP_GUIDE.md
```

---

## After Publishing — Keeping Your Personal Config Safe

Your personal `agents_config.py` (with your real phone numbers and agent details) should **never** be committed to the public repo.

Add this to your `.gitignore` if you want to work from the same folder:
```
agents_config.py
```

Or keep a private copy and only edit locally, never pushing the real config.

---

## Delete This File Before Pushing

This file (`PUBLISH_TO_GITHUB.md`) is for your reference only. Delete it before pushing, or add it to `.gitignore`.
