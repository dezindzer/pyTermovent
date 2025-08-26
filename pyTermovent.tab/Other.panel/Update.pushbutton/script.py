# -*- coding: utf-8 -*-
from pyrevit import forms, extensions, updater

# Name of your extension
extension_name = "pyTermovent"

# Find the extension
ext = None
for e in extensions.get_extensions():
    if e.name == extension_name:
        ext = e
        break

#pyRevit uses IronPython 2.7
if ext:
    updater.update_extension(ext)
    forms.alert("Extension '{}' updated!".format(extension_name), title="Update Complete")
else:
    forms.alert("Extension '{}' not found.".format(extension_name), title="Error")
    
#pyRevit uses IronPython 3
# if ext:
#     updater.update_extension(ext)  # pass the extension object
#     forms.alert(f"Extension '{extension_name}' updated!", title="Update Complete")
# else:
#     forms.alert(f"Extension '{extension_name}' not found.", title="Error")