import json
from openai import OpenAI


MODEL = "llama3.2:3b"

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",
)


SYSTEM_PROMPT = """
You are AURA, a local AI desktop automation planner.

Your job is to convert the user's natural-language request
into a sequence of simple commands that AURA can execute.

SUPPORTED COMMANDS:

- open <application>
- search <query>
- type <text>
- copy <text>
- paste
- move mouse <x> <y>
- left click
- right click
- double click
- screenshot
- read clipboard
- close <application>
- close window

RULES:

1. Break complex requests into multiple actions.
2. Keep actions in the correct order.
3. Use ONLY the supported commands.
4. Do not invent commands.
5. Return ONLY valid JSON.
6. The JSON must have this exact structure:

{
    "actions": [
        {
            "command": "..."
        }
    ]
}
"""


def understand(command, context=None):

    # Get AURA's current state
    context_info = ""

    if context:
        state = context.get_state()

        context_info = f"""
CURRENT AURA STATE:

Current application: {state["current_app"]}
Current window: {state["current_window"]}
Last command: {state["last_command"]}
Last result: {state["last_result"]}
History: {state["history"]}
"""

    # Send both context + user request to the local LLM
    user_message = f"""
{context_info}

USER REQUEST:
{command}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Remove markdown code fences if the model adds them
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        # Extract JSON from the response
        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No valid JSON found in model response")

        content = content[start:end + 1]

        return json.loads(content)

    except Exception as e:
        print(f"AURA local AI brain error: {e}")
        return None