# main.py
# ─────────────────────────────────────────────────────────────────────────────
# SMS Agent Webhook Server
#
# How it works:
#   1. Someone texts one of your Twilio numbers
#   2. Twilio sends that text to this server (at /webhook)
#   3. This server looks up which agent owns that phone number
#   4. It sends the message to Claude with that agent's instructions
#   5. Claude replies, and we send that reply back as an SMS
#
# You should not need to edit this file. All agent configuration lives in
# agents_config.py.
# ─────────────────────────────────────────────────────────────────────────────

import os
from fastapi import FastAPI, Form, Response
from anthropic import Anthropic
from agents_config import AGENTS

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI()

# Anthropic client — reads your API key from the ANTHROPIC_API_KEY environment variable
claude = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# ── Main webhook endpoint ──────────────────────────────────────────────────────

@app.post("/webhook")
async def receive_sms(
    From: str = Form(...),   # The phone number that sent the text (you)
    To: str = Form(...),     # The Twilio number that received it (which agent)
    Body: str = Form(...)    # The actual text message
):
    """
    Twilio calls this endpoint every time someone texts one of your numbers.
    We figure out which agent owns that number, ask Claude, and reply.
    """

    # Look up the agent for this Twilio number
    agent = AGENTS.get(To)

    if not agent:
        # This number isn't in agents_config.py yet
        return sms_reply(f"This number isn't connected to an agent yet. Add it to agents_config.py.")

    print(f"[{agent['name']}] Message from {From}: {Body}")

    # Send the message to Claude with this agent's system prompt
    response = claude.messages.create(
        model="claude-opus-4-6",
        max_tokens=500,           # Keep replies SMS-friendly
        system=agent["system_prompt"],
        messages=[
            {"role": "user", "content": Body}
        ]
    )

    reply = response.content[0].text
    print(f"[{agent['name']}] Reply: {reply}")

    return sms_reply(reply)


# ── Health check ───────────────────────────────────────────────────────────────

@app.get("/")
async def health_check():
    """
    Visit your Railway URL in a browser and you'll see this.
    It confirms your server is running.
    """
    agent_names = [config["name"] for config in AGENTS.values()]
    return {
        "status": "running",
        "agents": agent_names,
        "message": f"{len(agent_names)} agent(s) connected: {', '.join(agent_names)}"
    }


# ── Helper ─────────────────────────────────────────────────────────────────────

def sms_reply(message: str) -> Response:
    """
    Twilio expects replies in a specific XML format called TwiML.
    This function wraps any text in that format.
    """
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>"""
    return Response(content=twiml, media_type="text/xml")


# ── Local development ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    # Run locally with: python main.py
    # Render uses the Procfile instead, but this lets you test locally too
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
