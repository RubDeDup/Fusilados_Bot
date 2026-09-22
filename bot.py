import subprocess

# Start de scripts met exact dezelfde kleine/hoofdletters als in je bestandenlijst
planning_process = subprocess.Popen(["python", "planning_Porto.py"])
aanwezigheden_process = subprocess.Popen(["python", "aanwezigheden.py"])
clear_process = subprocess.Popen(["python", "clear.py"])

# Zorg dat het hoofdscript blijft draaien
planning_process.wait()
aanwezigheden_process.wait()
clear_process.wait()
