# This tells PyInstaller to grab everything inside the llama_cpp package
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('llama_cpp')