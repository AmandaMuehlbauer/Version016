import subprocess

# Read the contents of requirements.txt
with open("requirements.txt", "r") as req_file:
    requirements = req_file.read().splitlines()

# Add each requirement using Poetry's poetry add command
for requirement in requirements:
    subprocess.run(["poetry", "add", requirement])