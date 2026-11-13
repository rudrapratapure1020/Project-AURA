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

IMPORTANT RULES:
- Return ONLY valid JSON. Never include explanations or markdown.
- For a search request, return exactly one action using:
  "search <query>"
- Do not split search into open Google, type, or press enter.
- Use only commands supported by the application.

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
        print("\n--- RAW OLLAMA RESPONSE ---")
        print(repr(content))
        print("--- END RAW RESPONSE ---\n")

       
        # Extract valid JSON objects from the model response
        decoder = json.JSONDecoder()
        candidates = []

        for index, char in enumerate(content):
            if char == "{":
                try:
                    data, _ = decoder.raw_decode(content[index:])

                    if (
                        isinstance(data, dict)
                        and isinstance(data.get("actions"), list)
                    ):
                        candidates.append(data)

                except json.JSONDecodeError:
                    continue

        if not candidates:
            raise ValueError("No valid actions JSON found")

        # Use the final valid actions object
        data = candidates[-1]

        for action in data["actions"]:
            if (
                not isinstance(action, dict)
                or not isinstance(action.get("command"), str)
            ):
                raise ValueError("Invalid action format")

        return data


    except Exception as e:
        print(f"AURA local AI brain error: {e}")
        return None