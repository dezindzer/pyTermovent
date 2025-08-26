# -*- coding: utf-8 -*-
from pyrevit import script, forms, extensions
from pyrevit import updater

# Name of your extension
extension_name = "pyTermovent"

# Find the extension
ext = next((e for e in extensions.get_extensions() if e.name == extension_name), None)

if ext:
    updater.update_extension(ext.path)
    forms.alert(f"Extension '{extension_name}' updated!", title="Update Complete")
else:
    forms.alert(f"Extension '{extension_name}' not found.", title="Error")
