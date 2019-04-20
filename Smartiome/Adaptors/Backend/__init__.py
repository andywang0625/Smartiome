from os.path import dirname, basename, isfile
from os import listdir

raw_modules = listdir("Smartiome/Adaptors/Backend")
modules = []
for module in raw_modules:
    if "__" in module:
        continue
    if ".py" not in module:
        continue
    modules.append(module.replace(".py", ""))
print("Backends: "+str(modules))
__all__ = modules
