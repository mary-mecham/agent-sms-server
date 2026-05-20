# Agent SMS Server — Setup Guide

This guide walks you through deploying your SMS agent server from scratch. By the end, you'll be able to text a phone number and have Carmen (or Aria, or any agent) respond and take action.

**Time:** About 45–60 minutes the first time.  
**What you'll need:** A credit card for Twilio (~$1/mo per number) and your Anthropic API key.

---

## How This Works (Big Picture)

```
You text Carmen's number
      ↓
Twilio receives it and forwards it to your server
      ↓
Your server (running on Railway) asks Claude
      ↓
Claude responds as Carmen
      ↓
You get a text back
```

---

## Step 1 — Create a GitHub Account

GitHub is where your code lives. Railway (your server host) reads from GitHub to deploy.

1. Go to **github.com** and click **Sign up**
2. Choose a username (something professional — clients will see this)
3. Verify your email address
4. Choose the **Free** plan

That's it. You now have a GitHub account.

---

## Step 2 — Install Git on Your Mac

Git is the tool that sends your code from your computer up to GitHub.

1. Open **Terminal** (press `Cmd + Space`, type "Terminal", hit Enter)
2. Type this and press Enter:
   ```
   git --version
   ```
3. If you see a version number (like `git version 2.39.0`), you're already set — skip to Step 3.
4. If you see a prompt to install developer tools, click **Install** and wait for it to finish.

---

## Step 3 — Put Your Project on GitHub

1. In Terminal, navigate to your project folder:
   ```
   cd "/Users/tars/Documents/Claude/Projects/AI Agents/agent-sms-server"
   ```

2. Initialize it as a Git repository:
   ```
   git init
   git add .
   git commit -m "Initial commit — agent SMS server"
   ```

3. Go to **github.com**, click the **+** icon (top right) → **New repository**
4. Name it `agent-sms-server`
5. Keep it **Private**
6. Do NOT check "Add a README" (you already have files)
7. Click **Create repository**

8. GitHub will show you a page with commands. Copy and run the two lines that look like:
   ```
   git remote add origin https://github.com/YOURUSERNAME/agent-sms-server.git
   git push -u origin main
   ```

9. It will ask for your GitHub username and password. For the password, use a **Personal Access Token** (not your actual password):
   - Go to github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click **Generate new token (classic)**
   - Give it a name, set expiration to "No expiration", check the **repo** checkbox
   - Copy the token and paste it as your password

Your code is now on GitHub. ✅

---

## Step 4 — Deploy to Railway

Railway is where your server runs 24/7.

1. Go to **railway.app** and click **Login with GitHub**
2. Authorize Railway to access your GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select `agent-sms-server`
5. Railway will detect it's a Python project and start deploying automatically

**Add your API key:**
1. In your Railway project, click on your service
2. Click the **Variables** tab
3. Click **New Variable**
4. Name: `ANTHROPIC_API_KEY`
5. Value: your Anthropic API key (from console.anthropic.com → API Keys)
6. Click **Add**

Railway will automatically redeploy with the key added.

**Get your server URL:**
1. Click the **Settings** tab in your Railway service
2. Under **Domains**, click **Generate Domain**
3. You'll get a URL like `agent-sms-server-production.up.railway.app` — copy this

**Test it's working:**  
Open that URL in your browser. You should see:
```json
{"status": "running", "agents": ["Carmen", "Aria"], "message": "2 agent(s) connected: Carmen, Aria"}
```

Your server is live. ✅

---

## Step 5 — Get Twilio Phone Numbers

1. Go to **twilio.com** and create a free account
2. Verify your phone number during signup
3. Once in the dashboard, go to **Phone Numbers → Manage → Buy a number**
4. Search for numbers in your area code
5. Buy one number for Carmen (~$1.15/month)
6. Repeat to buy a second number for Aria

**Save these numbers** — you'll need them in the next step.

---

## Step 6 — Update agents_config.py With Your Real Numbers

1. Open the file `agents_config.py` in your project folder
2. Replace `+1CARMENNUMBER` with Carmen's actual Twilio number (e.g. `+18015550001`)
3. Replace `+1ARIANUMBER` with Aria's actual Twilio number
4. Save the file

Push the update to GitHub:
```
cd "/Users/tars/Documents/Claude/Projects/AI Agents/agent-sms-server"
git add agents_config.py
git commit -m "Add real Twilio phone numbers"
git push
```

Railway will automatically redeploy within about 30 seconds.

---

## Step 7 — Connect Twilio to Your Server

This tells Twilio to forward incoming texts to your Railway server.

For **each** Twilio number:
1. In Twilio, go to **Phone Numbers → Manage → Active Numbers**
2. Click on the phone number
3. Scroll to **Messaging Configuration**
4. Under "A message comes in", set:
   - **Webhook**
   - URL: `https://YOUR-RAILWAY-URL.up.railway.app/webhook`
   - Method: **HTTP POST**
5. Click **Save configuration**

Do this for both Carmen's number and Aria's number — they all point to the same URL.

---

## Step 8 — Test It

1. Text Carmen's Twilio number from your phone: `Email Eden's school and ask that she be excused today`
2. Within a few seconds, you should get a reply from Carmen

If it works — you're done! 🎉

---

## Troubleshooting

**No reply at all:**
- Check Railway logs (click your service → **Logs** tab) for error messages
- Make sure your Twilio webhook URL is exactly right (no trailing slash issues)
- Make sure your ANTHROPIC_API_KEY variable is set in Railway

**"This number isn't connected to an agent yet":**
- Double-check the phone number in `agents_config.py` matches the Twilio number exactly, including the +1

**"Authentication error" in Railway logs:**
- Your ANTHROPIC_API_KEY is wrong or missing — check it in Railway Variables

---

## Adding a New Agent Later

1. Buy a new Twilio number
2. Open `agents_config.py` and add a new block (copy the template at the bottom of the file)
3. Push to GitHub — Railway redeploys automatically
4. Set up the webhook in Twilio for the new number
5. Done

---

## For Your Clients

When you teach this to clients, the steps are exactly the same. The only things that change per client are:
- Their agent names and system prompts (in `agents_config.py`)
- Their Twilio phone numbers
- Their Anthropic API key

Everything else — Railway, GitHub, the server code — is identical. You can give clients a copy of this exact repo as a starting template.
