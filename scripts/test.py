# Imports
import win32con
import ctypes, ctypes.wintypes
import sys

#
# Functions
#
def dispatch_hotkey(msg):
    mod = msg.lParam & 0b1111111111111111
    key = msg.lParam >> 16
    bit = bin(msg.lParam)[2:]
    print("\n*** Received hotkey message (wParam: %d, lParam: %d)" % (msg.wParam, msg.lParam))
    print("lParam bitmap: %s" % bit)
    print("lParam low-word (modifier): %d, high-word (key): %d" % (mod, key))
    print("-> Hotkey %s with modifier %s detected\n" % (keys[key], mods[mod]))

#
# Main
#

# Build translation maps (virtual key codes / modifiers to string)
# Note: exec() is a hack and should not be used in real programs!!
print("\n*** Building translation maps")
mods = {}
keys = {}
for item in dir(win32con):
    if item.startswith("MOD_"):
        exec("mods[item] = win32con." + item)
        exec("mods[win32con." + item + "] = '" + item + "'")
    if item.startswith("VK_"):
        exec("keys[item] = win32con." + item)
        exec("keys[win32con." + item + "] = '" + item + "'")

# Process command line
print("\n*** Processing command line")

mod = "MOD_WIN"
key = "VK_ESCAPE"
for param in sys.argv:
    if param.startswith("MOD_"):
        if param in mods: mod = param
        else: print("\nInvalid modifier specified (%s). Using default.\n-> Use '--list-mods' for a list of valid modifiers." % param)
    if param.startswith("VK_"):
        if param in keys: key = param
        else: print("\nInvalid key specified (%s). Using default.\n-> Use '--list-keys' for a list of valid keys." % param)

if "--list-mods" in sys.argv:
    print("\nAvailable modifiers:")
    for item in dir(win32con):
        if item.startswith("MOD_"): sys.stdout.write(item + ", ")
    print("\b\b ")

if "--list-keys" in sys.argv:
    print("\nAvailable keys:")
    for item in dir(win32con):
        if item.startswith("VK_"): sys.stdout.write(item + ", ")
    print("\b\b ")

# Register hotkey
print("\n*** Registering global hotkey (modifier: %s, key: %s)" % (mod, key))
ctypes.windll.user32.RegisterHotKey(None, 1, mods[mod], keys[key])

# Wait for hotkey to be triggered
print("\n*** Waiting for hotkey message...")
try:
    msg = ctypes.wintypes.MSG()
    while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
        if msg.message == win32con.WM_HOTKEY:
            dispatch_hotkey(msg)
            break
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))

# Unregister hotkey
finally:
    ctypes.windll.user32.UnregisterHotKey(None, 1)