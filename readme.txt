Installation instruction:

1. To install python:
	- to open file ./exe/python-3.6.3-amd64.exe
2. To unzip ./zip/poppler-0.68.0.zip into "C:\Program Files".
3. Add path "C:\Program Files\poppler-0.68.0\bin" into environment variable PATH
	- to open comand line
	- to enter command "setx /M PATH "%PATH%;C:\Program Files\poppler-0.68.0\bin""
4. To install requirements (for developers only):
	- to open command line (push "win+r", type the command "cmd" and push "enter")
	- typr the comand "python -m pip install --upgrade pip"
	- type the comand "pip install -r req.txt"

Exploitation instruction:

The program can process dpf-files and png-files.

1. Run comand line and go to current directory (for example, if your package is on your Desctop than run cmd and type "cd Desktop\corner_maker" to go to by current directory).
2. Activate virtual environment: type the comant ".\venv\Scripts\activate.bat".

To process pdf-file:
1. To put input pdf to directory .\pdf\input.
2. Type the command "python main.py -pdf".
3. Pick up processed pdf-file from the directory .\pdf\output.

To process png-file:
1. To put input images to directory .\png\input.
2. Type the command "python main.py -png".
3. Pick up processed immage files from the directory .\png\output.