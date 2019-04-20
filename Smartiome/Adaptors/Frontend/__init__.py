from os.path import dirname, basename, isfile
from os import listdir

raw_modules = listdir("Smartiome/Adaptors/Frontend")
modules = []
for module in raw_modules:
    if "__" in module:
        continue
    if ".py" not in module:
        continue
    modules.append(module.replace(".py", ""))
print("Frontends: "+str(modules))
__all__ = modules
