@echo off
git rm -r --cached .
git add .
git commit -m "Limpiar cache de Git y aplicar .gitignore"
git push
pause