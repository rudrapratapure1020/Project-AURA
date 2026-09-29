from tools.clipboard_tool import copy_text, get_clipboard, paste_text
from tools.mouse_tool import left_click, right_click, double_click, move_mouse
from tools.screenshot_tool import take_screenshot
from tools.keyboard_tool import type_text
from tools.browser import search_google
from tools.app_launcher import open_app
from tools.window_tool import close_window, close_app
from core.observer import observe_app


def handle_open(app_name, context=None):
    success = open_app(app_name)

    if not success:
        return {
            "success": False,
            "message": f"Could not open {app_name}"
        }

    window = observe_app(app_name)

    if context and window:
        context.set_window(app_name, window)

    return {
        "success": True,
        "message": f"{app_name} opened successfully",
        "window": window
    }


def handle_search(query):
    result = search_google(query)

    return {
        "success": True,
        "message": f"Search completed for: {query}",
        "result": result
    }


def handle_type(text):
    result = type_text(text)

    return {
        "success": bool(result),
        "message": "Text typed successfully"
    }


def handle_copy(text):
    copy_text(text)

    return {
        "success": True,
        "message": "Text copied to clipboard"
    }


def handle_paste():
    result = paste_text()

    return {
        "success": bool(result),
        "message": "Clipboard pasted"
    }


def handle_move_mouse(x, y):
    move_mouse(x, y)

    return {
        "success": True,
        "message": f"Mouse moved to ({x}, {y})"
    }


def handle_screenshot():
    path = "screenshot.png"
    result = take_screenshot(path)

    return {
        "success": bool(result),
        "message": f"Screenshot saved to {path}"
    }


def handle_close_app(app_name):
    result = close_app(app_name)

    return {
        "success": bool(result),
        "message": f"{app_name} closed"
    }


# ============================================================
# AURA TOOL REGISTRY
# ============================================================

TOOLS = {
    "open_app": {
        "function": handle_open,
        "description": "Open a Windows application.",
        "parameters": {
            "app_name": "string"
        }
    },

    "search_google": {
        "function": handle_search,
        "description": "Search Google in the currently active browser.",
        "parameters": {
            "query": "string"
        }
    },

    "type_text": {
        "function": handle_type,
        "description": "Type text using the keyboard.",
        "parameters": {
            "text": "string"
        }
    },

    "copy_text": {
        "function": handle_copy,
        "description": "Copy text to the clipboard.",
        "parameters": {
            "text": "string"
        }
    },

    "paste": {
        "function": handle_paste,
        "description": "Paste the current clipboard contents.",
        "parameters": {}
    },

    "move_mouse": {
        "function": handle_move_mouse,
        "description": "Move the mouse to screen coordinates.",
        "parameters": {
            "x": "integer",
            "y": "integer"
        }
    },

    "screenshot": {
        "function": handle_screenshot,
        "description": "Capture a screenshot of the screen.",
        "parameters": {}
    },

    "left_click": {
        "function": left_click,
        "description": "Perform a left mouse click.",
        "parameters": {}
    },

    "right_click": {
        "function": right_click,
        "description": "Perform a right mouse click.",
        "parameters": {}
    },

    "double_click": {
        "function": double_click,
        "description": "Perform a double mouse click.",
        "parameters": {}
    },

    "read_clipboard": {
        "function": lambda: {
            "success": True,
            "clipboard": get_clipboard()
        },
        "description": "Read the current clipboard contents.",
        "parameters": {}
    },

    "close_window": {
        "function": close_window,
        "description": "Close the currently active window.",
        "parameters": {}
    },

    "close_app": {
        "function": handle_close_app,
        "description": "Close a Windows application.",
        "parameters": {
            "app_name": "string"
        }
    }
}


def get_tool(name):
    """Return a registered AURA tool."""
    return TOOLS.get(name)


def list_tools():
    """Return the available tool names."""
    return list(TOOLS.keys())