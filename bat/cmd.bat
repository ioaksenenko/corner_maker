@echo off
for /F "usebackq delims=" %%M in (`hostname`) do runas /profile /user:%%M\����������� cmd
pause