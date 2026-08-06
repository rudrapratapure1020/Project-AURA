from core.router import handle_command

print("🤖 AURA Started!")
print("Type 'exit' to quit.\n")

while True:
    command = input("AURA > ")

    if command.lower() == "exit":
        print("👋 Goodbye!")
        break

    handle_command(command)