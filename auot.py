#!/usr/bin/env python3
import tkinter, tkinter.messagebox
import os

REDIST_FILE_URL = "https://download.microsoft.com/download/9/3/F/93FCF1E7-E6A4-478B-96E7-D4B285925B00/vc_redist.x64.exe"
REDIST_FILE_NAME = REDIST_FILE_URL.split("/")[-1]
CABINET_FILE = "a10"
DLL_FILE = "ucrtbase.dll"
SYSTEM32_SUB_PATH = "steam/steamapps/compatdata/1466860/pfx/drive_c/windows/system32"
TMP_PATH = "/tmp"

def messagebox(title, text):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title, text)
    root.destroy()

def errorbox(title, text):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(title, text)
    root.destroy()

def getAndCheckSystemFolder():
    global SYSTEM32_SUB_PATH
    path = os.path.join(os.environ['HOME'], '.steam')
    if not os.path.isdir(path):
        errorbox("No Steam Folder", f"Steam path does not exist: {path}")
        return
    path = os.path.join(path, SYSTEM32_SUB_PATH)
    if not os.path.isdir(path):
        errorbox("No System32 Folder", f"Can't find system folder. Is the game installed with proton?")
        return
    return path

def downloadFile(url, dest_path):
    os.system(f'wget -c --read-timeout=5 --tries=0 "{url}" -P "{dest_path}"')

def extractFile(folder_path, exe_name, cabinet_name):
    os.system(f'cabextract "{os.path.join(folder_path, exe_name)}" -d "{folder_path}"')
    os.system(f'cabextract "{os.path.join(folder_path, cabinet_name)}" -d "{folder_path}"')

def areFilesSame(path_1, path_2, file_name):
    sum_1 = os.popen(f'md5sum "{os.path.join(path_1, file_name)}"').read().split()[0]
    sum_2 = os.popen(f'md5sum "{os.path.join(path_2, file_name)}"').read().split()[0]
    return sum_1 in sum_2

def replaceFile(source_path, dest_path, file_name):
    os.popen(f'cp "{os.path.join(source_path, file_name)}" "{os.path.join(dest_path, file_name)}"').read()

system32_path = getAndCheckSystemFolder()
downloadFile(REDIST_FILE_URL, TMP_PATH)
extractFile(TMP_PATH, REDIST_FILE_NAME, CABINET_FILE)

if areFilesSame(TMP_PATH, system32_path, DLL_FILE):
    messagebox("Already up to date", "File is already patched!")
else:
    replaceFile(TMP_PATH, system32_path, DLL_FILE)
    messagebox("Patched", "File got Patched!")
