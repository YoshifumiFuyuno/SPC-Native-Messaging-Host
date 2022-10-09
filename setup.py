#!/usr/bin/env python3

import os
import sys
import json

__file__ = os.path.abspath(__file__) # Not required in Python 3.9 or later
manifest = {
	"name": "spcnmh",
	"description": "spcnmh",
	"type": "stdio"
}
allowed = {"allowed_origins": ["chrome-extension://hlikagndoiibjkblhopoajeonpkfgiko/"], "allowed_extensions": ["{d4c9d93a-c00c-49da-b57e-424c20160155}"]}
linuxPaths = {"allowed_origins": "~/.config/google-chrome/NativeMessagingHosts", "allowed_extensions": "~/.mozilla/native-messaging-hosts/"}
macPaths = {"allowed_origins": "~/Library/Application Support/Google/Chrome/NativeMessagingHosts", "allowed_extensions": "~/Library/Application Support/Mozilla/NativeMessagingHosts"}
regKeys = {"allowed_origins": r"HKCU\SOFTWARE\Google\Chrome\NativeMessagingHosts", "allowed_extensions": r"HKCU\SOFTWARE\Mozilla\NativeMessagingHosts"}

def uninstall():
	def uninstallUnix(paths):
		for path in paths.values():
			os.remove(os.path.join(os.path.expanduser(path), "spcnmh.json"))

	if sys.platform == "win32":
		for key in regKeys.values():
			os.system(fr"REG DELETE {key}\spcnmh /f")
		instPath = os.path.expandvars(r"%APPDATA%\spcnmh")
		if os.path.exists(instPath):
			import shutil
			shutil.rmtree(instPath)
	elif sys.platform == "linux":
		uninstallUnix(linuxPaths)
	elif sys.platform == "darwin":
		uninstallUnix(macPaths)
	else:
		sys.exit(1)

def install():
	def installUnix(paths):
		manifest["path"] = os.path.join(dirPath, "spcnmh.py")
		os.system(f'chmod +x "{manifest["path"]}"')
		for manifestKey, path in paths.items():
			manifestCopy = manifest.copy()
			manifestCopy[manifestKey] = allowed[manifestKey]
			path = os.path.expanduser(path)
			os.makedirs(path, exist_ok=True)
			with open(os.path.join(path, "spcnmh.json"), "w", encoding="utf-8") as f:
				json.dump(manifestCopy, f, ensure_ascii=False, indent=2)

	def installWin():
		instPath = dirPath
		if "__compiled__" in globals():
			import shutil
			instPath = os.path.expandvars(r"%APPDATA%\spcnmh")
			os.makedirs(instPath, exist_ok=True)
			manifest["path"] = os.path.join(instPath, "spcnmh.exe")
			shutil.copy(os.path.join(dirPath, "spcnmh.exe"), manifest["path"])
		else:
			manifest["path"] = os.path.join(instPath, "spcnmh.bat")
			with open(manifest["path"], 'w') as f:
				f.write(r'@python -u "%~dp0\spcnmh.py" %*')

		for manifestKey, regKey in regKeys.items():
			manifestCopy = manifest.copy()
			manifestCopy[manifestKey] = allowed[manifestKey]
			manifestPath = os.path.join(instPath, f"spcnmh_{manifestKey}.json")
			with open(manifestPath, "w", encoding="utf-8") as f:
				json.dump(manifestCopy, f, ensure_ascii=False, indent=2)
			os.system(fr'REG ADD {regKey}\spcnmh /ve /t REG_SZ /d "{manifestPath}" /f')

	dirPath = os.path.dirname(__file__)
	if sys.platform == "win32":
		installWin()
	elif sys.platform == "linux":
		installUnix(linuxPaths)
	elif sys.platform == "darwin":
		installUnix(macPaths)
	else:
		sys.exit(1)

if sys.version_info[0:2] < (3, 8):
	sys.stderr.write("Python 3.8 or later required\n")
	sys.exit(1)

s = input("1. Install (or update)\n2. Uninstall\n[1/2]?:")
if s == "1":
	install()
	print("Done")
elif s == "2":
	uninstall()
	print("Done")
else:
	print("Exit")
