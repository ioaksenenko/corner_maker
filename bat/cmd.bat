@echo off
for /F "usebackq delims=" %%M in (`hostname`) do runas /profile /user:%%M\Администратор cmd
pause