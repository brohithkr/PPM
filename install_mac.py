#  NOTE: install works for MAC (and probably LINUX)
#  NOTE: must be installed manually for WINDOWS, however install_win.py should be written soonish

#  install script for ppm
#  load all resources and move into root directory

import os
import sys

#  first of all check if git is installed
#  run git to test if its installed, and add >/dev/null to supress a console output from the command
check = os.system("git >/dev/null")

if check != 256:    #  running the git command successfully will return code 256
    #  warn user
    if input("Warning!\n\tGit isn't installed! Functionality will be restricted.\n\tDownload Git from https://git-scm.com/download/mac for full functionality.\n\tDownload git installer now?\n\tYes: Y, No: N  > ").lower() == "y":
        os.system("open https://sourceforge.net/projects/git-osx-installer/files/git-2.14.1-intel-universal-mavericks.dmg/download?use_mirror=autoselect")
    print("Continuing...")
rsrc = {}

#  load the licenses
with open("src/rsrc/Apache.txt") as file:
    rsrc["apache"] = file.read()
with open("src/rsrc/MIT.txt") as file:
    rsrc["mit"] = file.read()
with open("src/rsrc/GPL3.txt") as file:
    rsrc["gpl"] = file.read()

#  load the main script
with open("src/bin/main.py") as file:
    rsrc["main"] = file.read()

#  find the home directory
from os.path import expanduser
home = expanduser("~")

new_dir_bin = os.path.join(home, "ppm/bin")
new_dir_rsrc = os.path.join(home, "ppm/rsrc")

#  create the necessary folders
if os.path.isdir(new_dir_bin) == False:
    os.makedirs(new_dir_bin)
if os.path.isdir(new_dir_bin) == False:
    os.makedirs(new_dir_rsrc)

#  populate them with files
with open(os.path.join(new_dir_bin, "main.py"), "w") as file:
    file.write(rsrc["main"])

with open(os.path.join(new_dir_rsrc, "Apache.txt"), "w") as file:
    file.write(rsrc["apache"])
with open(os.path.join(new_dir_rsrc, "MIT.txt"), "w") as file:
    file.write(rsrc["mit"])
with open(os.path.join(new_dir_rsrc, "GPL3.txt"), "w") as file:
    file.write(rsrc["gpl"])

#  create an alias for the python3 main.py command

#  open .bash_profile to write, therefore creating it if it doesn't exist
with open(os.path.join(home, ".bash_profile"), "r+") as file:
    bash_profile = file.read()
    path = os.path.join(home, "ppm/bin/main.py")

    if "alias ppm='python3 {}'".format(path) not in bash_profile:    #  see if the alias has already been added
        #  create the alias for running ppm
        file.write("{}\n{}".format(bash_profile, "alias ppm='python3 {}'".format(path)))

#  refresh the bash shell environment for changes to take effect
os.system("source ~/.bash_profile")

#  print success message + PPM menu
print("Success!\nRestart the shell to access the ppm command.")
