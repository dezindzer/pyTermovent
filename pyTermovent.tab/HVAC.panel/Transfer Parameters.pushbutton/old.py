# ###########################################################################################
# -*- coding: utf-8 -*-
# import sys, clr, Autodesk, os, re, json, System # type: ignore
# from collections import Counter
# # import pyrevit libraries
# from pyrevit import revit, DB, script, forms
# from pyrevit.revit import doc
# # import Autodesk libraries
# from Autodesk.Revit.DB import *
# from Autodesk.Revit.DB import Color, FilteredElementCollector, AssemblyType, BuiltInParameter ,BuiltInCategory, ElementId, AssemblyDetailViewOrientation, XYZ
# #import Autodesk.Revit.DB as DB
# from Autodesk.Revit.UI import *
# from Autodesk.Revit.UI import UIApplication, RibbonPanel, RibbonItem, ColorSelectionDialog
# from Autodesk.Revit.UI.Selection import *
# from pyrevit.compat import PY3
# from pyrevit import forms, HOST_APP
# from pyrevit.forms import WarningBar
# from pyrevit.framework import List
# from itertools import izip
#from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, Separator, CheckBox

# app = HOST_APP.app
# uiapp = UIApplication(app)
# ui = uiapp.ActiveUIDocument
# doc = revit.doc

# # clr.AddReference('RevitAPIUI')
# # uidoc=__revit__.ActiveUIDocument # type: ignore
# # doc=__revit__.ActiveUIDocument.Document # type: ignore
# ###########################################################################################
# def Canceled():
#     forms.alert('User canceled the operation', title="Canceled", exitscript=True)

# def get_name(element, title_on_sheet=False):
#     if isinstance(element, DB.View):
#         view_name = None
#         if title_on_sheet:
#             titleos_param = element.Parameter[DB.BuiltInParameter.VIEW_DESCRIPTION]
#             view_name = titleos_param.AsString()
#         if view_name:
#             return view_name
#         else:
#             if HOST_APP.is_newer_than("2019", or_equal=True):
#                 return element.Name
#             else:
#                 return element.ViewName
#     if PY3:
#         return element.Name
#     else:
#         return Element.Name.GetValue(element)

# ###########################################################################################