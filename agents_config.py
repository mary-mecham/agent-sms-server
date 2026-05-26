# agents_config.py
# ─────────────────────────────────────────────────────────────────────────────
# This is the only file you'll normally need to edit.
# Each entry in AGENTS maps a Twilio phone number to an AI agent.
# To add a new agent: buy a Twilio number, paste it as a key, write a prompt.
# ─────────────────────────────────────────────────────────────────────────────

AGENTS = {

    # ── EXAMPLE AGENT — Replace this with your own ───────────────────────────
    # Delete this block and add your own agents below.
    "+1XXXXXXXXXX": {
        "name": "AgentName",
        "allowed_numbers": ["+1YOURCELLPHONE"],  # Only these numbers can text this agent
        "system_prompt": """You are [Agent Name], [role] for [Your Name].

Your job is to help with [key responsibilities].

You can help with things like:
- [Task type 1]
- [Task type 2]
- [Task type 3]

Guidelines:
- You're responding via SMS, so keep replies concise and clear
- Always confirm what action you took (e.g. "Done — added that to your list")
- If you need a detail to complete a task, ask one clear question
- If you can't take an action directly, tell the user exactly what you did instead
- Never make up information — ask if you don't know"""
    },

    # ── ADD MORE AGENTS BELOW ─────────────────────────────────────────────────
    # Copy and paste this block for each new agent:
    #
    # "+1PHONENUMBER": {
    #     "name": "AgentName",
    #     "allowed_numbers": ["+1YOURCELLPHONE"],  # Add multiple numbers if needed: ["+1111", "+1222"]
    #     "system_prompt": """You are [Name], [role description].
    #
    # Your job is to...
    # """
    # },

}
