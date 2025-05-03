@echo off
git rm -r --cached .
git add .
git commit -m "Limpiar cache de Git y aplicar Nuevos Cambios && Herramientas de Desarrollo"
git push
pause