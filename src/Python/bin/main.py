import sys
import os
from datetime import datetime
import getpass


def new(args):

    #  setup files for creation

    if len(args["pass_args"]) > 1:
        project_type, project_name = args["pass_args"][0], args["pass_args"][1]
    else:
        project_type, project_name = "--bin", args["pass_args"][0]

    user_name = getpass.getuser()

    curr_path = args["curr_path"]
    new_dir = os.path.join(curr_path, project_name)

    if os.path.exists(new_dir):    #  check that we won't be overwriting a project of the same name
        sys.exit("A project of that name already exists!")

    if project_type != "--bin" and project_type != "--lib":
        sys.exit("Invalid project type.")

    rsrc = {}

    rsrc["LICENSE"] = "Copyright (c) {} {} All Rights Reserved.".format(datetime.now().year, user_name)
    rsrc["README"] = "# {}".format(project_name)
    rsrc["main"] = "#!/usr/bin/python3\nprint('Hello World!')"

    #  create project in current directory

    #  also creates all directories inbetween
    new_dir_src = os.path.join(new_dir, project_name)
    os.makedirs(new_dir_src)

    #  now populate project with files

    if project_type == "--lib":
        rsrc["setup"] = "from setuptools import setup, find_packages\nsetup(name='{}', author='{}', version='0.1', packages = find_packages(),)".format(project_name, user_name)
        rsrc["init"] = "from main import *".format()

        with open(os.path.join(new_dir, "setup.py"), "w") as file:
            file.write(rsrc["setup"])

        with open(os.path.join(new_dir_src, "__init__.py"), "w") as file:
            file.write(rsrc["init"])

    with open(os.path.join(new_dir, "LICENSE.txt"), "w") as file:
        file.write(rsrc["LICENSE"])
    with open(os.path.join(new_dir, "README.md"), "w") as file:
        file.write(rsrc["README"])

    with open(os.path.join(new_dir_src, "main.py"), "w") as file:
        file.write(rsrc["main"])

    #  print completed message
    if project_type == "--bin":
        print("\tCreated binary '{}' project".format(project_name))
    elif project_type == "--lib":
        print("\tCreated library '{}' project".format(project_name))


def install(args):
    package = args["pass_args"][0]
    command = "pip3 install {}".format(package)
    try:
        os.system(command)
    except:
        sys.exit("Failed to install package.")


def run(args):
    curr_path = args["curr_path"]

    if len(args["pass_args"]) > 0:    #  if file to run passed, run that
        run = os.path.join(curr_path, args["pass_args"][0])
    else:
        py_files = []
        for file in os.listdir(curr_path):    #  collect all python files in scope
            if file.endswith(".py"):
                py_files.append(file)
        if "main.py" in py_files:    #  if one is called main.py, run it
            run = os.path.join(curr_path, "main.py")
        else:    #  otherwise panic
            sys.exit("""No python filename passed or "main.py" file detected.""")

    command = "python3 {}".format(run)
    try:
        os.system(command)
    except:
        sys.exit("Failed to install package.")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        args = {"pass_args":sys.argv[2:], "curr_path":os.getcwd()}

        #  NOTE: all arguments passed to functions are passed as a single dict.

        command = "{}({})".format(sys.argv[1], args)
        eval(command)

    else:
        print("""
Python Package Manager:

 - New project -
 $ ppm new [project name]

 - Install library or module -
 $ ppm install [project name / github url]

 - Run the python program -
 $ ppm run
        """)
