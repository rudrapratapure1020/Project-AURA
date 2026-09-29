from core.command_registry import get_tool


def execute_tool(tool_name, arguments=None, context=None):

    tool = get_tool(tool_name)

    if not tool:
        print(f"Unknown AURA tool: {tool_name}")
        return {
            "success": False,
            "message": f"Unknown tool: {tool_name}"
        }

    function = tool["function"]
    arguments = arguments or {}

    try:
        # Pass context only to tools that need it
        if tool_name == "open_app":
            result = function(
                arguments.get("app_name", ""),
                context
            )
        else:
            result = function(**arguments)

        if result is None:
            result = {
                "success": True,
                "message": f"{tool_name} completed"
            }

        if context:
            context.record_command(
                tool_name,
                result
            )

        return result

    except Exception as e:

        print(f"TOOL ERROR [{tool_name}]: {e}")

        result = {
            "success": False,
            "message": str(e)
        }

        if context:
            context.record_command(
                tool_name,
                result
            )

        return result