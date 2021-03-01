#!python3
# Run all the doctests in this folder

import glob, importlib, os, sys

for file in glob.iglob("*.py"):
    if "run_all" in file:
        continue
    print("\n\nProcessing "+file)
    # print(sys.executable+" "+file)
    os.system('"'+sys.executable+'"'+" "+file+" quiet")
    # importlib.import_module(file.replace(".py",""))

