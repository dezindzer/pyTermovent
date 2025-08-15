@echo off
color 60
title pyTermovent Installer
echo Installing pyTermovent

pyrevit extend ui pyTermovent "https://github.com/dezindzer/pyTermovent.git" --branch=main &cls

echo Installation done
timeout 3 
echo done