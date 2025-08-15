@echo off
color 60
title TermoventHVAC Installer
echo Installing TermoventHVAC

pyrevit extend ui pyTermovent "https://github.com/dezindzer/TermoventHVAC.git" --branch=main &cls

echo Installation done
timeout 3 
echo done