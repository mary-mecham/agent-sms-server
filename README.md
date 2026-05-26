# Agent SMS Server

Give your AI agents their own phone numbers. Text them commands, get responses back.

Built to work with the **My Business Genie AI agent system** — one server handles all your agents. Adding a new agent is as simple as buying a Twilio number and adding a few lines to a config file.

## Quick Start

→ **[Read the full setup guide](SETUP_GUIDE.md)**

The guide covers everything from creating your GitHub and Render accounts through completing Twilio A2P registration. Budget 60–90 minutes for your first setup.

## What's in This Repo

| File | What it does |
|------|-------------|
| `main.py` | The webhook server — receives texts from Twilio, asks Claude, sends back a reply |
| `agents_config.py` | **The only file you'll edit** — maps phone numbers to agent profiles |
| `requirements.txt` | Python dependencies (installed automatically by Render) |
| `Procfile` | Tells Render how to start the server |
| `.env.example` | Template for your environment variables |
| `SETUP_GUIDE.md` | Full step-by-step setup instructions |

## Cost Summary

| Item | Cost |
|------|------|
| Twilio phone number | ~$1.15/month per agent |
| A2P Brand registration | ~$4.50 one-time |
| A2P Campaign vetting | ~$15 one-time |
| A2P Campaign monthly fee | ~$1.50–$10/month (shared across all numbers) |
| Render Starter server | $7/month (shared across all agents) |
| Anthropic API usage | ~$0.01–$0.05/month |
| **First agent total** | **~$10–$20/month ongoing** |
| **Each additional agent** | **~$1.15/month** |

## Requirements

- GitHub account (free)
- Render account ($7/mo Starter recommended)
- Twilio account
- Anthropic API key
- A live Privacy Policy page on your website (required for A2P registration)
