# Give Your AI Agent a Phone Number
### SMS Channel Setup Guide

This guide walks you through connecting a phone number to any AI agent in your org chart so you can text it commands and get responses back.

By the end, you'll be able to text your agent things like:
- "Draft an email to my client about tomorrow's meeting"
- "Add oat milk to the grocery list"
- "What's on my calendar today?"

**Time:** About 60–90 minutes the first time. Much faster for each agent after that.  
**Cost:** ~$1.15/month per phone number (Twilio) + $7/month for your server (Render Starter) + small Anthropic API usage fees (fractions of a cent per message)

---

## How It Works

```
You text your agent's number
        ↓
Twilio receives it and forwards it to your server
        ↓
Your server identifies which agent owns that number
        ↓
Claude responds as that agent
        ↓
You get a text back
```

One server handles all your agents. Adding a new agent just means buying a new phone number and adding a few lines to a config file.

---

## What You'll Need

- A **GitHub account** (free) — stores your code
- A **Render account** (free to start, $7/mo recommended for production) — runs your server
- A **Twilio account** — provides phone numbers (~$1.15/mo per number)
- An **Anthropic API key** — powers your agents (pay-as-you-go, very cheap for SMS)
- A **Privacy Policy page** — required for Twilio A2P registration (a simple page on your website works)

---

## Step 1 — Create a GitHub Account

1. Go to **github.com** and click **Sign up**
2. Choose a username
3. Verify your email
4. Choose the **Free** plan

---

## Step 2 — Install Git on Your Computer

1. Open **Terminal** (Mac: press `Cmd + Space`, type "Terminal")
2. Type `git --version` and press Enter
3. If you see a version number, you're set. If not, follow the prompt to install developer tools.

---

## Step 3 — Get the Agent SMS Server Code

Clone the template repository to your computer:

```
git clone https://github.com/mary-mecham/agent-sms-server.git
cd agent-sms-server
```

This downloads all the server code you need. You won't need to write any code — just edit the config file in the next step.

---

## Step 4 — Configure Your Agents

Open **agents_config.py** in any text editor. This is the only file you'll regularly edit.

For each agent you want to connect, add an entry:

```python
"+1YOURNUMBER": {
    "name": "AgentName",
    "system_prompt": """You are [Agent Name], [role] for [Business Owner Name].

Your job is to help with [key responsibilities].

You can help with things like:
- [Task type 1]
- [Task type 2]
- [Task type 3]

Guidelines:
- You're responding via SMS, so keep replies concise and clear
- Always confirm what action you took
- If you need more information, ask one clear question
- Never make up information — ask if you don't know"""
}
```

**Writing a good system prompt:**
- Be specific about the agent's role and what they can help with
- Mention key people, tools, or context the agent should know about
- Keep the tone appropriate for how you want to interact with them
- You can always update this later — just edit the file and push to GitHub

---

## Step 5 — Push to Your Own GitHub Repository

Create a new **private** repository on github.com called `agent-sms-server`, then connect it:

```
git remote set-url origin https://github.com/YOURUSERNAME/agent-sms-server.git
git push -u origin main
```

If asked for a password, use a Personal Access Token (not your GitHub password):
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token → check **repo** → copy it

**Tip:** If you run into auth issues, install the GitHub CLI:
```
brew install gh
gh auth login
```
Then push normally.

---

## Step 6 — Deploy to Render

1. Go to **render.com** and sign up with GitHub
2. Click **New → Web Service**
3. Select your `agent-sms-server` repository
4. Render will detect Python automatically. Fill in:
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free (for testing) or Starter at $7/mo (recommended for production — prevents spin-down delays)
5. Under **Environment Variables**, add:
   - Name: `ANTHROPIC_API_KEY`
   - Value: your Anthropic API key (from console.anthropic.com → API Keys)
6. Click **Deploy Web Service**

**Wait 2–3 minutes** for the build to complete. When it says "Live," copy your Render URL (e.g. `https://agent-sms-server.onrender.com`).

**Test it:** Open your Render URL in a browser. You should see a JSON message listing your connected agents.

**Note on the Free tier:** Free Render instances spin down after 15 minutes of inactivity, which means the first text after a quiet period can take 30–60 seconds to get a response (and may time out). For reliable SMS, use the Starter plan ($7/mo) or set up UptimeRobot (free) to ping your URL every 5 minutes.

---

## Step 7 — Get Twilio Phone Numbers

1. Go to **twilio.com** and create an account
2. Verify your phone number
3. Go to **Phone Numbers → Manage → Buy a number**
4. Buy one number per agent (~$1.15/month each)

Save each number — you'll need them in the next step.

---

## Step 8 — Add Phone Numbers to Your Config

Open `agents_config.py` and replace the placeholder numbers with your real Twilio numbers (format: `+1XXXXXXXXXX`).

Push the update:
```
git add agents_config.py
git commit -m "Add Twilio phone numbers"
git push
```

Render will redeploy automatically within 30 seconds.

---

## Step 9 — Connect Twilio to Your Server

For **each** phone number:
1. In Twilio, go to **Phone Numbers → Manage → Active Numbers**
2. Click the number
3. Scroll to **Messaging Configuration**
4. Set "A message comes in" to:
   - **Webhook**
   - URL: `https://YOUR-RENDER-URL.onrender.com/webhook`
   - Method: **HTTP POST**
5. Click **Save configuration**

---

## Step 10 — Complete A2P 10DLC Registration

US carriers require all businesses sending SMS from local phone numbers to register. This prevents your messages from being blocked or filtered.

**What you'll need before you start:**
- Legal business name
- EIN (Employer Identification Number)
- Business address
- Website URL
- **Privacy Policy URL** — you must have a live privacy policy page on your website. This is required by carriers and your registration will be rejected without it. A simple page is fine (many website builders have a template).
- Brief description of your messaging use case

**In Twilio, go to Messaging → Regulatory Compliance → A2P 10DLC → Onboarding**

**Step 1 — Register your brand** (~$4.50 one-time fee, approved within hours)
- Company type: Private
- Brand type: Low-Volume Standard (for most businesses)
- Fill in your business details and EIN

**Step 2 — Register a campaign** (~$15 one-time vetting fee + $1.50–$10/month)
- Use case: Mixed (covers task management, notifications, and responses)
- Campaign description: Describe your internal agent messaging use case
- Sample messages: Provide 5 realistic examples of what your agent will send
- Opt-in method: Describe that the business owner initiates contact by texting the number themselves
- Privacy Policy URL: paste the URL to your privacy policy page

**Opt-in language that works well:**
> "The sole user of this messaging campaign is the business owner. The business owner opts in by personally configuring and purchasing the dedicated phone number for internal business use. The owner initiates each conversation by texting the number themselves, which constitutes explicit opt-in consent. All messages are exchanged exclusively between the business owner and their own internal business management system. No third parties send or receive messages. No marketing messages are sent."

**Step 3 — Add phone numbers to your campaign**
- Go to the Linked Messaging Service → Sender Pool → Add Senders
- Add all numbers you want to use

**Approval timeline:** Brand registration is typically instant. Campaign approval takes 2–5 business days (sometimes up to 2–3 weeks). You'll receive an email when approved.

---

## Step 11 — Test It

Once your campaign is approved, text your agent's number from your phone. You should receive a response within 5–10 seconds.

If something doesn't work, check:
1. **Render logs** — shows whether the message was received and what response was generated
2. **Twilio Message Logs** — shows whether the SMS was delivered (Messaging → Try it out → Messaging Logs)

---

## Adding More Agents Later

1. Buy a new Twilio number
2. Add a new entry to `agents_config.py`
3. Push to GitHub (Render redeploys automatically)
4. Set the webhook in Twilio for the new number
5. Add the number to your A2P campaign's Sender Pool

---

## Common Issues

**No response at all:**
- Check Render logs for errors
- Verify the Twilio webhook URL is correct (no missing `/webhook` at the end)
- Make sure `ANTHROPIC_API_KEY` is set in Render environment variables

**"This number isn't connected to an agent yet":**
- The phone number in `agents_config.py` doesn't match the Twilio number exactly — check the `+1` format

**Message received but not delivered to your phone:**
- A2P 10DLC registration is pending or not completed — this is the most common cause
- Check Twilio Message Logs for delivery errors

**Campaign rejected during A2P registration:**
- Make sure your opt-in text explains that the business owner self-initiates by texting the number
- Make sure your Privacy Policy URL is filled in and the page is live
- Use the "Fix Campaign" button in Twilio to resubmit — you won't be charged the vetting fee again

**Slow responses (30–60 seconds):**
- Your Render free instance spun down — upgrade to Starter ($7/mo) or set up UptimeRobot

**"Credit balance too low" error in Render logs:**
- Add credits to your Anthropic account at console.anthropic.com → Billing
