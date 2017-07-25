import subprocess
import pyautogui, time

subprocess.Popen("C:\\Windows\System32\\notepad.exe")

time.sleep(5)
pyautogui.click()

pyautogui.typewrite("Hello world!")

pyautogui.keyDown('shift')
pyautogui.press('4')
pyautogui.keyUp('shift')

