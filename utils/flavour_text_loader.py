import sys
import importlib.util
import os

flavour_directory = "flavour_text"
flavour_modules = {}

for filename in os.listdir(flavour_directory):
    if filename.endswith(".py"):
        kind = filename[:-3]
        flavour_path = sys.path[0] + f"/{flavour_directory}/{filename}"
        spec = importlib.util.spec_from_file_location(f"{flavour_directory}.{kind}", flavour_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        globals()[kind] = mod
        flavour_modules[f"{kind}_text"] = mod  # Optional: store in a dict for easy access