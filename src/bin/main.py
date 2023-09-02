import sys
import os
from datetime import datetime
import getpass
import subprocess
import toml
import json

want_venv = True
venv_name = ".venv"
venv_pip = f"{venv_name}/bin/pip"


def add(args):
    check_git()
    user_name = getpass.getuser()
    #  gets the users email from git, then converts the output to string and removes new lines
    user_email = (
        subprocess.run(
            ["git", "config", "--global", "user.email"], stdout=subprocess.PIPE
        )
        .stdout.decode("ascii")
        .replace("\n", "")
    )

    #  add a specific file (created by the new() function) to the current directory

    if not args["pass_args"]:  #  some quick checks
        sys.exit("No arguments specified.")

    curr_path = args["curr_path"]

    if len(args["pass_args"]) > 1:
        file_type, file_arg = args["pass_args"][0], args["pass_args"][1]
    else:
        file_type, file_arg = args["pass_args"][0], None

    if (
        file_type == "--license"
    ):  #  can create 3 types of license, with user details added
        if file_arg == None:
            contents = "Copyright (c) {} {} All Rights Reserved."

        elif file_arg.lower() == "mit":
            with open("../rsrc/MIT.txt") as file:
                contents = file.read().format(datetime.now().year, user_name)

        elif file_arg.lower() == "apache":
            with open("../rsrc/Apache.txt") as file:
                contents = file.read().replace("%%YEAR%%", str(datetime.now().year))
                contents = contents.replace("%%COPYRIGHT_HOLDER%%", user_name)

        elif file_arg.lower() == "gpl":
            with open("../rsrc/GPL3.txt") as file:
                contents = file.read()

        with open(
            os.path.join(curr_path, "LICENSE.txt"), "w"
        ) as file:  #  will overwrite any current License.txt in the directory
            file.write(contents)

    elif (
        file_type == "--setup"
    ):  #  creates a setup.py file with added project information
        #  gets the name of the folder the project is held within. e.g.: the projects name
        project_name = os.path.basename(os.getcwd())

        contents = "from setuptools import setup, find_packages\nsetup(name='{}', author='{}', author_email='{}', version='0.1', packages = find_packages(),)".format(
            project_name, user_name, user_email
        )

        with open(
            os.path.join(curr_path, "setup.py"), "w"
        ) as file:  #  will overwrite any current setup.py in the directory
            file.write(contents)


def new(args):
    check_git()
    #  setup files for creation

    if len(args["pass_args"]) > 1:
        project_type, project_name = args["pass_args"][0], args["pass_args"][1]
    else:
        project_type, project_name = "--bin", args["pass_args"][0]

    user_name = getpass.getuser()
    #  gets the users email from git, then converts the output to string and removes new lines
    user_email = (
        subprocess.run(
            ["git", "config", "--global", "user.email"], stdout=subprocess.PIPE
        )
        .stdout.decode("ascii")
        .replace("\n", "")
    )

    curr_path = args["curr_path"]
    new_dir = os.path.join(curr_path, project_name)

    if os.path.exists(
        new_dir
    ):  #  check that we won't be overwriting a project of the same name
        sys.exit("A project of that name already exists!")

    if project_type != "--bin" and project_type != "--lib":
        sys.exit("Invalid project type.")

    rsrc = {}

    rsrc["LICENSE"] = "Copyright (c) {} {} All Rights Reserved.".format(
        datetime.now().year, user_name
    )
    rsrc["README"] = "# {}".format(project_name)
    rsrc["main"] = "#!/usr/bin/python3\nprint('Hello World!')"

    #  create project in current directory

    #  also creates all directories inbetween
    new_dir_src = os.path.join(new_dir, "src")
    os.makedirs(new_dir_src)

    #  now populate project with files

    if project_type == "--lib":
        rsrc[
            "setup"
        ] = "from setuptools import setup, find_packages\nsetup(name='{}', author='{}', author_email='{}', version='0.1', packages = find_packages(),)".format(
            project_name, user_name, user_email
        )
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

    pip_dict = {
        "package": {"name": project_name, "author": user_name, "version": "0.1"},
        "requirements": {},
    }
    with open(os.path.join(new_dir, "pip.toml"), "w") as file:
        toml.dump(pip_dict, file)


def install_from_toml(path):
    with open(path, "r") as file:
        deps = toml.load(file)["requirements"]
        for package, version in deps.items():
            res = subprocess.run(
                [venv_pip if want_venv else "pip", "install", f"{package}=={version}"],
                stdout=subprocess.PIPE,
            ).stdout.decode("ascii")
            print(res)


def install(args):
    check_git()
    curr_path = args["curr_path"]

    os.chdir(curr_path)
    if not os.path.isdir(os.path.join(curr_path, venv_name)):
        os.system(f"python3 -m venv {venv_name}")

    if len(args["pass_args"]) == 0:
        print("Installing requirements...")
        install_from_toml(os.path.join(curr_path, "pip.toml"))
        print("All requirements installed")
        return

    package = args["pass_args"][0]
    command = f"{'pip3' if not want_venv else venv_pip} install {package}"

    pip_dict = {}
    with open(os.path.join(curr_path, "pip.toml"), "r") as file:
        pip_dict = toml.load(file)

    try:
        os.system(command)
        with open(os.path.join(curr_path, "pip.toml"), "w") as file:
            pip_dict["requirements"][
                package
            ] = f"{get_data(package, curr_path)['Version']}"
            toml.dump(pip_dict, file)
    except Exception as e:
        with open(os.path.join(curr_path, "pip.toml"), "w") as file:
            toml.dump(pip_dict, file)
        print("error", e)
        sys.exit("Failed to install package.")


def run(args):
    curr_path = args["curr_path"]

    if len(args["pass_args"]) > 0:  #  if file to run passed, run that
        run = os.path.join(curr_path, args["pass_args"][0])
    else:
        py_files = []
        for file in os.listdir(os.path.join(curr_path,"src")):  #  collect all python files in scope
            if file.endswith(".py"):
                py_files.append(file)
        if "main.py" in py_files:  #  if one is called main.py, run it
            run = os.path.join(os.path.join(curr_path,"src"), "main.py")
        else:  #  otherwise panic
            sys.exit("""No python filename passed or "main.py" file detected.""")

    command = "python3 {}".format(run)
    try:
        os.system(command)
    except:
        sys.exit("Failed to install package.")


def check_git():
    #  check git is installed, only run by commands that require git to succeed

    #  run git to test if its installed, and add >/dev/null to supress a console output from the command
    check = os.system("git >/dev/null")

    if check != 256:  #  running the git command successfully will return code 256
        sys.exit("Please install git before using this function!")


def get_data(package, curr_path):
    os.chdir(curr_path)
    raw_data = (
        subprocess.run(
            [venv_pip if want_venv else "pip", "show", package], stdout=subprocess.PIPE
        )
        .stdout.decode("ascii")
        .split("\n")
    )
    data = {}
    for i in raw_data[:-1]:
        key, value = i.split(": ", 2)
        data[key] = value

    return data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = {"pass_args": sys.argv[2:], "curr_path": os.getcwd()}
        #  NOTE: all arguments passed to functions are passed as a single dict.

        command = "{}({})".format(sys.argv[1], args)
        eval(command)

    else:
        print(
            """
Python Package Manager:

 - New project -
 $ ppm new [project name]

 - Install library or module -
 $ ppm install [project name / github url]

 - Run the python program -
 $ ppm run
        """
        )
