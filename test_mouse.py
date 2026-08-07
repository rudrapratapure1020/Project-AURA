from tools.mouse_tool import move_mouse, double_click
import time

print("Move your mouse to a safe target...")
time.sleep(3)

move_mouse(500, 300)

print("Double-clicking in 2 seconds...")
time.sleep(2)

double_click()