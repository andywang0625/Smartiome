from os.path import dirname, basename, isfile
from os import listdir

raw_modules = listdir("app/plugins")
modules = []
for module in raw_modules:
    if "__" in module:
        continue
    modules.append(module.replace(".py", ""))
print(modules)
__all__ = modules
