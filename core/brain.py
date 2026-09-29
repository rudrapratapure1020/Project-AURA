import json
from openai import OpenAI


MODEL = "llama3.2:3b"

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",
)


SYSTEM_PROMPT = """
You are AURA, a local AI desktop automation agent.

You control a Windows computer through registered tools.

AVAILABLE TOOLS:

1. open_app
Description: Open a Windows application.
Arguments:
{
    "app_name": "string"
}

2. search_google
Description: Search Google in the currently active browser.
Arguments:
{
    "query": "string"
}

3. type_text
Description: Type text using the keyboard.
Arguments:
{
    "text": "string"
}

4. copy_text
Description: Copy text to clipboard.
Arguments:
{
    "text": "string"
}

5. paste
Description: Paste clipboard contents.
Arguments: {}

6. move_mouse
Description: Move mouse to screen coordinates.
Arguments:
{
    "x": integer,
    "y": integer
}

7. screenshot
Description: Take a screenshot.
Arguments: {}

8. left_click
Description: Perform a left click.
Arguments: {}

9. right_click
Description: Perform a right click.
Arguments: {}

10. double_click
Description: Perform a double click.
Arguments: {}

11. read_clipboard
Description: Read clipboard contents.
Arguments: {}

12. close_window
Description: Close the active window.
Arguments: {}

13. close_app
Description: Close a Windows application.
Arguments:
{
    "app_name": "string"
}


RULES:

1. Understand the user's goal.
2. Select the required tools.
3. Keep tools in the correct order.
4. Use only the available tools.
5. Never invent a tool.
6. Return ONLY valid JSON.
7. Return this exact structure:

{
    "actions": [
        {
            "tool": "tool_name",
            "arguments": {}
        }
    ]
}

Example:

User:
Open Chrome and search for Python AI tutorials.

Response:

{
    "actions": [
        {
            "tool": "open_app",
            "arguments": {
                "app_name": "Chrome"
            }
        },
        {
            "tool": "search_google",
            "arguments": {
                "query": "Python AI tutorials"
            }
        }
    ]
}
"""


def understand(command, context=None):

    context_info = ""

    if context:
        state = context.get_state()

        context_info = f"""
CURRENT AURA STATE:

Current application:
{state["current_app"]}

Current window:
{state["current_window"]}

Last command:
{state["last_command"]}

Last result:
{state["last_result"]}

Recent history:
{state["history"][-5:]}
"""

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

        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No valid JSON found")

        content = content[start:end + 1]

        return json.loads(content)

    except Exception as e:

        print(f"AURA local AI brain error: {e}")

        return None